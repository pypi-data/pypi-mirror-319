import pandas as pd
from urllib.parse import urlencode
from fudstop.apis.polygonio.mapping import option_condition_dict, OPTIONS_EXCHANGES
from datetime import datetime, timedelta, timezone
import pytz
import aiohttp
from fudstop.apis.helpers import get_human_readable_string
from typing import Optional
from fudstop.apis.webull.trade_models.stock_quote import MultiQuote
import asyncio
import httpx
from typing import List, Dict
import time
import logging
from fudstop.apis.polygonio.async_polygon_sdk import Polygon
from fudstop.apis.polygonio.models.option_models.universal_snapshot import UniversalOptionSnapshot
from fudstop.apis.webull.trade_models.analyst_ratings import Analysis
from fudstop.apis.webull.trade_models.stock_quote import MultiQuote
from fudstop.apis.webull.trade_models.capital_flow import CapitalFlow, CapitalFlowHistory
from fudstop.apis.webull.trade_models.deals import Deals
from fudstop.apis.webull.trade_models.cost_distribution import CostDistribution, NewCostDist
from fudstop.apis.webull.trade_models.etf_holdings import ETFHoldings
from fudstop.apis.webull.webull_ta import WebullTA
from fudstop.apis.webull.trade_models.institutional_holdings import InstitutionHolding, InstitutionStat
from fudstop.apis.webull.trade_models.financials import BalanceSheet, FinancialStatement, CashFlow
from fudstop.apis.webull.trade_models.news import NewsItem
from fudstop.apis.webull.trade_models.forecast_evaluator import ForecastEvaluator
from fudstop.apis.webull.trade_models.short_interest import ShortInterest
from fudstop.apis.webull.webull_option_screener import WebullOptionScreener
from fudstop.apis.webull.trade_models.volume_analysis import WebullVolAnalysis
from fudstop.apis.webull.trade_models.ticker_query import WebullStockData
from fudstop.apis.webull.trade_models.analyst_ratings import Analysis
from fudstop.apis.webull.trade_models.price_streamer import PriceStreamer
from fudstop.apis.webull.trade_models.company_brief import CompanyBrief, Executives, Sectors
from fudstop.apis.webull.trade_models.order_flow import OrderFlow
import asyncio
import aiohttp
import os
from dotenv import load_dotenv
poly = Polygon()
load_dotenv()
ta = WebullTA()
class UltimateSDK:
    def __init__(self):
    # ---------------------------------------------------------------
    # SINGLE-TICKER METHODS (as you already have them)
    # ---------------------------------------------------------------
        self.wb_headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "access_token": "dc_us_tech1.193f1ba4ca7-5bd586952af0445ea4e4883003c577b1",
            "app": "global",
            "app-group": "broker",
            "appid": "wb_web_app",
            "device-type": "Web",
            "did": "w35fbki4nv4n4i6fjbgjca63niqpo_22",
            "hl": "en",
            "origin": "https://app.webull.com",
            "os": "web",
            "osv": "i9zh",
            "platform": "web",
            "priority": "u=1, i",
            "referer": "https://app.webull.com/",
            "reqid": "h15qdhcy99l2sidi00t2sox8y748h_35",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "tz": "America/Chicago",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "ver": "5.2.1",
            "x-s": "9ad7d1393ca5c705bfe6469622b6805384a53b27c86fcaf5966061737c602747",
            "x-sv": "xodp2vg9"
        }

        self.api_key = os.environ.get('YOUR_POLYGON_KEY')
        self.scalar_tickers = ['SPX', 'VIX', 'OSTK', 'XSP', 'NDX', 'MXEF']
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.semaphore = asyncio.Semaphore(10)
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.thirty_days_from_now = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        self.fifteen_days_ago = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
        self.fifteen_days_from_now = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
        self.eight_days_from_now = (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d')
        self.eight_days_ago = (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d')
        self.timeframes = ['m1','m5', 'm10', 'm15', 'm20', 'm30', 'm60', 'm120', 'm240', 'd1']
        self.now_timestamp_int = int(datetime.now(timezone.utc).timestamp())
        self.day = int(86400)
        self.ticker_df = pd.read_csv('files/ticker_csv.csv')
        self.id = 15765933
        self.ticker_to_id_map = dict(zip(self.ticker_df['ticker'], self.ticker_df['id']))
        self.wb_headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "access_token": "dc_us_tech1.193f1ba4ca7-5bd586952af0445ea4e4883003c577b1",
    "app": "global",
    "app-group": "broker",
    "appid": "wb_web_app",
    "device-type": "Web",
    "did": "w35fbki4nv4n4i6fjbgjca63niqpo_22",
    "hl": "en",
    "origin": "https://app.webull.com",
    "os": "web",
    "osv": "i9zh",
    "platform": "web",
    "priority": "u=1, i",
    "referer": "https://app.webull.com/",
    "reqid": "h15qdhcy99l2sidi00t2sox8y748h_35",
    "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "tz": "America/Chicago",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "ver": "5.2.1",
    "x-s": "9ad7d1393ca5c705bfe6469622b6805384a53b27c86fcaf5966061737c602747",
    "x-sv": "xodp2vg9"
}
        

    async def get_quotes_for_tickers(self, tickers: List[str]):
        async def chunk_and_get_ids(lst, chunk_size):
            """Asynchronously chunk the list and fetch IDs for each chunk."""
            for i in range(0, len(lst), chunk_size):
                chunk = lst[i:i + chunk_size]
                ids = await self.get_webull_id_for_tickers(chunk)  # Fetch IDs for the current chunk
                yield ids
        
        results = []
        
        async with httpx.AsyncClient() as client:
            # Asynchronously process chunks and make API requests
            async for ticker_ids in chunk_and_get_ids(tickers, 54):
                ticker_ids_str = ",".join(map(str, ticker_ids)) # Join IDs into a comma-separated string
                response = await client.get(
                    f"https://quotes-gw.webullfintech.com/api/bgw/quote/realtime?ids={ticker_ids_str}&includeSecu=1&delay=0&more=1"
                )
                if response.status_code == 200:
                    # Assuming the API returns JSON data
                    results.extend(response.json())
                else:
                    # Handle errors (optional logging)
                    print(f"Failed to fetch data for IDs: {ticker_ids}")

        return MultiQuote(results)
    


    async def get_webull_id_for_tickers(self, tickers: List[str]):
        """Converts ticker name to ticker ID to be passed to other API endpoints from Webull."""
        ticker_ids = [self.ticker_to_id_map.get(symbol) for symbol in tickers]
        # Remove None values from the list
        filtered_ticker_ids = [ticker_id for ticker_id in ticker_ids if ticker_id is not None]
        return filtered_ticker_ids

    async def get_webull_id(self, symbol):
        """Converts ticker name to ticker ID to be passed to other API endpoints from Webull."""
        ticker_id = self.ticker_to_id_map.get(symbol)
        return ticker_id

    async def get_analyst_ratings(self, symbol: str):
        try:
            ticker_id = self.ticker_to_id_map.get(symbol)
            endpoint = f"https://quotes-gw.webullfintech.com/api/information/securities/analysis?tickerId={ticker_id}"
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    if resp.status == 200:
                        datas = await resp.json()
                        return Analysis(datas)
        except Exception as e:
            print(e)
        return None

    async def get_short_interest(self, symbol: str):
        try:
            ticker_id = self.ticker_to_id_map.get(symbol)
            if not ticker_id:
                raise ValueError(f"Ticker {symbol} not found in ticker_to_id_map.")

            endpoint = f"https://quotes-gw.webullfintech.com/api/information/brief/shortInterest?tickerId={ticker_id}"
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    if resp.status == 200:
                        datas = await resp.json()
                        return ShortInterest(datas)
        except Exception as e:
            print(f"Error: {e}")
        return None

    async def institutional_holding(self, symbol: str):
        try:
            ticker_id = self.ticker_to_id_map.get(symbol)
            endpoint = f"https://quotes-gw.webullfintech.com/api/information/stock/getInstitutionalHolding?tickerId={ticker_id}"
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    if resp.status == 200:
                        datas = await resp.json()
                        return InstitutionStat(datas)
        except Exception as e:
            print(e)
        return None

    async def volume_analysis(self, symbol: str):
        try:
            ticker_id = self.ticker_to_id_map.get(symbol)
            endpoint = f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/stat?count=10&tickerId={ticker_id}&type=0"
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    if resp.status == 200:
                        datas = await resp.json()
                        return WebullVolAnalysis(datas, symbol)
        except Exception as e:
            print(e)
        return None

    async def new_cost_dist(self, symbol: str, start_date: str, end_date: str):
        """Returns list"""
        try:
            ticker_id = self.ticker_to_id_map.get(symbol)
            endpoint = (
                f"https://quotes-gw.webullfintech.com/api/quotes/chip/query?"
                f"tickerId={ticker_id}&startDate={start_date}&endDate={end_date}"
            )
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        data = data['data']
                        return NewCostDist(data, symbol)
        except Exception as e:
            print(e)
        return None

    # ---------------------------------------------------------------
    # MULTI-TICKER METHODS (concurrent versions)
    # ---------------------------------------------------------------

    async def institutional_holdings_for_tickers(
        self, 
        tickers: list[str]
    ) -> dict[str, InstitutionStat | None]:
        """
        Fetch institutional holding for multiple tickers concurrently.
        Returns a dict: { ticker: InstitutionStat object (or None) }
        """
        tasks = [
            asyncio.create_task(self.institutional_holding(ticker))
            for ticker in tickers
        ]
        results = await asyncio.gather(*tasks)
        return dict(zip(tickers, results))

    async def short_interest_for_tickers(
        self, 
        tickers: list[str]
    ) -> dict[str, ShortInterest | None]:
        """
        Fetch short interest for multiple tickers concurrently.
        Returns a dict: { ticker: ShortInterest object (or None) }
        """
        tasks = [
            asyncio.create_task(self.get_short_interest(ticker))
            for ticker in tickers
        ]
        results = await asyncio.gather(*tasks)
        return dict(zip(tickers, results))

    async def analyst_ratings_for_tickers(
        self, 
        tickers: list[str]
    ) -> dict[str, Analysis | None]:
        """
        Fetch analyst ratings for multiple tickers concurrently.
        Returns a dict: { ticker: Analysis object (or None) }
        """
        tasks = [
            asyncio.create_task(self.get_analyst_ratings(ticker))
            for ticker in tickers
        ]
        results = await asyncio.gather(*tasks)
        return dict(zip(tickers, results))

    async def volume_analysis_for_tickers(
        self, 
        tickers: list[str]
    ) -> dict[str, WebullVolAnalysis | None]:
        """
        Fetch volume analysis for multiple tickers concurrently.
        Returns a dict: { ticker: WebullVolAnalysis object (or None) }
        """
        tasks = [
            asyncio.create_task(self.volume_analysis(ticker))
            for ticker in tickers
        ]
        results = await asyncio.gather(*tasks)
        return dict(zip(tickers, results))

    async def new_cost_dist_for_tickers(
        self, 
        tickers: list[str], 
        start_date: str, 
        end_date: str
    ) -> dict[str, NewCostDist | None]:
        """
        Fetch new cost dist for multiple tickers concurrently (requires start_date & end_date).
        Returns a dict: { ticker: NewCostDist object (or None) }
        """
        tasks = [
            asyncio.create_task(self.new_cost_dist(ticker, start_date, end_date))
            for ticker in tickers
        ]
        results = await asyncio.gather(*tasks)
        return dict(zip(tickers, results))

    async def _news_single(self, session: httpx.AsyncClient, symbol: str, pageSize: str, headers) -> "NewsItem | None":
        """
        Private helper for fetching news for a single ticker using an existing session.
        """
        try:
            if not headers:
                raise ValueError("Headers are required but not provided.")

            ticker_id = self.ticker_to_id_map.get(symbol)
            if not ticker_id:
                raise ValueError(f"Ticker {symbol} not found in ticker_to_id_map.")

            endpoint = (
                "https://nacomm.webullfintech.com/api/information/news/"
                f"tickerNews?tickerId={ticker_id}&currentNewsId=0&pageSize={pageSize}"
            )
            # session is already created by the caller
            response = await session.get(endpoint)
            if response.status_code == 200:
                datas = response.json()
                return NewsItem(datas)  # your existing data class
            else:
                raise Exception(f"Failed to fetch news data: {response.status_code}")
        except Exception as e:
            print(f"Error in news: {symbol}, {e}")
            return None

    async def _company_brief_single(self, session: httpx.AsyncClient, symbol: str) -> tuple | None:
        """
        Private helper to fetch a company's brief for a single ticker.
        Returns (CompanyBrief, Sectors, Executives) or None.
        """
        try:
            ticker_id = self.ticker_to_id_map.get(symbol)
            if not ticker_id:
                raise ValueError(f"Ticker {symbol} not found.")

            endpoint = f"https://quotes-gw.webullfintech.com/api/information/stock/brief?tickerId={ticker_id}"
            resp = await session.get(endpoint)
            if resp.status_code != 200:
                raise Exception(f"HTTP error: {resp.status_code}")

            datas = resp.json()
            # Your existing data classes
            companyBrief = CompanyBrief(datas["companyBrief"])
            sectors = Sectors(datas["sectors"])
            executives = Executives(datas["executives"])
            return (companyBrief, sectors, executives)
        except Exception as e:
            print(f"Error in company_brief: {symbol}, {e}")
            return None

    async def _balance_sheet_single(self, session: httpx.AsyncClient, symbol: str, limit: str) -> "BalanceSheet | None":
        try:
            ticker_id = self.ticker_to_id_map.get(symbol)
            if not ticker_id:
                raise ValueError(f"Ticker {symbol} not found.")

            endpoint = (
                "https://quotes-gw.webullfintech.com/api/information/financial/"
                f"balancesheet?tickerId={ticker_id}&type=101&fiscalPeriod=0&limit={limit}"
            )
            resp = await session.get(endpoint)
            if resp.status_code == 200:
                datas = resp.json()
                return BalanceSheet(datas)
        except Exception as e:
            print(f"Error in balance_sheet: {symbol}, {e}")
        return None

    async def _cash_flow_single(self, session: httpx.AsyncClient, symbol: str, limit: str) -> "CashFlow | None":
        try:
            ticker_id = self.ticker_to_id_map.get(symbol)
            if not ticker_id:
                raise ValueError(f"Ticker {symbol} not found.")

            endpoint = (
                "https://quotes-gw.webullfintech.com/api/information/financial/"
                f"cashflow?tickerId={ticker_id}&type=102&fiscalPeriod=1,2,3,4&limit={limit}"
            )
            resp = await session.get(endpoint)
            if resp.status_code == 200:
                datas = resp.json()
                return CashFlow(datas)
        except Exception as e:
            print(f"Error in cash_flow: {symbol}, {e}")
        return None

    async def _income_statement_single(self, session: httpx.AsyncClient, symbol: str, limit: str) -> "FinancialStatement | None":
        try:
            ticker_id = self.ticker_to_id_map.get(symbol)
            if not ticker_id:
                raise ValueError(f"Ticker {symbol} not found.")

            endpoint = (
                "https://quotes-gw.webullfintech.com/api/information/financial/"
                f"incomestatement?tickerId={ticker_id}&type=102&fiscalPeriod=1,2,3,4&limit={limit}"
            )
            resp = await session.get(endpoint)
            if resp.status_code == 200:
                datas = resp.json()
                return FinancialStatement(datas)
        except Exception as e:
            print(f"Error in income_statement: {symbol}, {e}")
        return None

    async def _order_flow_single(self, session: httpx.AsyncClient, symbol: str, headers, flow_type: str, count: str) -> "OrderFlow | None":
        try:
            ticker_id = self.ticker_to_id_map.get(symbol)
            if not ticker_id:
                raise ValueError(f"Ticker {symbol} not found.")

            endpoint = (
                "https://quotes-gw.webullfintech.com/api/stock/capitalflow/stat?"
                f"count={count}&tickerId={ticker_id}&type={flow_type}"
            )
            resp = await session.get(endpoint)
            if resp.status_code == 200:
                data = resp.json()
                return OrderFlow(data)
            else:
                raise Exception(f"Failed to fetch order flow data. HTTP Status: {resp.status_code}")
        except Exception as e:
            print(f"Error in order_flow: {symbol}, {e}")
            return None

    async def _capital_flow_single(self, session: httpx.AsyncClient, symbol: str) -> tuple["CapitalFlow | None", "CapitalFlowHistory | None"]:
        try:
            ticker_id = self.ticker_to_id_map.get(symbol)
            if not ticker_id:
                raise ValueError(f"Ticker {symbol} not found.")

            endpoint = (
                "https://quotes-gw.webullfintech.com/api/stock/capitalflow/"
                f"ticker?tickerId={ticker_id}&showHis=true"
            )
            resp = await session.get(endpoint)
            resp.raise_for_status()
            datas = resp.json()

            latest = datas.get("latest", {})
            historical = datas.get("historical", [])

            dates = [i.get("date") for i in historical]
            historical_items = [i.get("item") for i in historical]
            latest_item = latest.get("item", {})

            data = CapitalFlow(latest_item, ticker=symbol)
            history = CapitalFlowHistory(historical_items, dates)
            return data, history
        except httpx.RequestError as req_err:
            print(f"Request error for {symbol}: {req_err}")
        except httpx.HTTPStatusError as http_err:
            print(f"HTTP status error for {symbol}: {http_err}")
        except Exception as e:
            print(f"An unexpected error occurred: {symbol}, {e}")

        return None, None

    async def _etf_holdings_single(self, session: httpx.AsyncClient, symbol: str, pageSize: str) -> "ETFHoldings | None":
        try:
            ticker_id = self.ticker_to_id_map.get(symbol)
            if not ticker_id:
                raise ValueError(f"Ticker {symbol} not found.")

            endpoint = (
                "https://quotes-gw.webullfintech.com/api/information/"
                f"company/queryEtfList?tickerId={ticker_id}&pageIndex=1&pageSize={pageSize}"
            )
            resp = await session.get(endpoint)
            if resp.status_code == 200:
                datas = resp.json()
                return ETFHoldings(datas)
        except Exception as e:
            print(f"Error in etf_holdings: {symbol}, {e}")
        return None

    # -------------------------------------------
    # "for_tickers" methods (concurrent)
    # -------------------------------------------

    async def news_for_tickers(
        self, 
        tickers: list[str], 
        pageSize: str = "100", 
        headers=None
    ) -> dict[str, "NewsItem | None"]:
        """
        Fetch news for multiple tickers concurrently using a single session.
        Returns a dict {ticker: NewsItem or None}.
        """
        async with httpx.AsyncClient(headers=headers) as session:
            tasks = [
                asyncio.create_task(self._news_single(session, sym, pageSize, headers))
                for sym in tickers
            ]
            results = await asyncio.gather(*tasks)
        return dict(zip(tickers, results))

    async def company_brief_for_tickers(
        self, 
        tickers: list[str]
    ) -> dict[str, tuple | None]:
        """
        Fetch company briefs for multiple tickers concurrently.
        Returns {ticker: (companyBrief, sectors, executives) or None}.
        """
        async with httpx.AsyncClient() as session:
            tasks = [
                asyncio.create_task(self._company_brief_single(session, sym))
                for sym in tickers
            ]
            results = await asyncio.gather(*tasks)
        return dict(zip(tickers, results))

    async def balance_sheet_for_tickers(
        self, 
        tickers: list[str], 
        limit: str = "11"
    ) -> dict[str, "BalanceSheet | None"]:
        """
        Fetch balance sheets for multiple tickers concurrently.
        Returns {ticker: BalanceSheet or None}.
        """
        async with httpx.AsyncClient() as session:
            tasks = [
                asyncio.create_task(self._balance_sheet_single(session, sym, limit))
                for sym in tickers
            ]
            results = await asyncio.gather(*tasks)
        return dict(zip(tickers, results))

    async def cash_flow_for_tickers(
        self, 
        tickers: list[str], 
        limit: str = "12"
    ) -> dict[str, "CashFlow | None"]:
        """
        Fetch cash flow statements for multiple tickers concurrently.
        Returns {ticker: CashFlow or None}.
        """
        async with httpx.AsyncClient() as session:
            tasks = [
                asyncio.create_task(self._cash_flow_single(session, sym, limit))
                for sym in tickers
            ]
            results = await asyncio.gather(*tasks)
        return dict(zip(tickers, results))

    async def income_statement_for_tickers(
        self, 
        tickers: list[str], 
        limit: str = "12"
    ) -> dict[str, "FinancialStatement | None"]:
        """
        Fetch income statements for multiple tickers concurrently.
        Returns {ticker: FinancialStatement or None}.
        """
        async with httpx.AsyncClient() as session:
            tasks = [
                asyncio.create_task(self._income_statement_single(session, sym, limit))
                for sym in tickers
            ]
            results = await asyncio.gather(*tasks)
        return dict(zip(tickers, results))

    async def order_flow_for_tickers(
        self, 
        tickers: list[str], 
        headers, 
        flow_type: str = "0", 
        count: str = "1"
    ) -> dict[str, "OrderFlow | None"]:
        """
        Fetch order flow data for multiple tickers concurrently.
        Returns {ticker: OrderFlow or None}.
        """
        async with httpx.AsyncClient(headers=headers) as session:
            tasks = [
                asyncio.create_task(self._order_flow_single(session, sym, headers, flow_type, count))
                for sym in tickers
            ]
            results = await asyncio.gather(*tasks)
        return dict(zip(tickers, results))

    async def capital_flow_for_tickers(
        self, 
        tickers: list[str]
    ) -> dict[str, tuple["CapitalFlow | None", "CapitalFlowHistory | None"]]:
        """
        Fetch capital flow data (latest + history) for multiple tickers concurrently.
        Returns {ticker: (CapitalFlow, CapitalFlowHistory) or (None, None)}.
        """
        async with httpx.AsyncClient() as session:
            tasks = [
                asyncio.create_task(self._capital_flow_single(session, sym))
                for sym in tickers
            ]
            results = await asyncio.gather(*tasks)
        return dict(zip(tickers, results))

    async def etf_holdings_for_tickers(
        self, 
        tickers: list[str], 
        pageSize: str = "200"
    ) -> dict[str, "ETFHoldings | None"]:
        """
        Fetch ETF holdings for multiple tickers concurrently.
        Returns {ticker: ETFHoldings or None}.
        """
        async with httpx.AsyncClient() as session:
            tasks = [
                asyncio.create_task(self._etf_holdings_single(session, sym, pageSize))
                for sym in tickers
            ]
            results = await asyncio.gather(*tasks)
        return dict(zip(tickers, results))
    


    async def fetch_latest_rsi(self, session: aiohttp.ClientSession, ticker: str, timespan:str='day') -> tuple[str, float | None]:
        """
        Fetch the latest RSI value for a single ticker.
        Returns a tuple of (ticker, latest_rsi_value).
        If something goes wrong or no data is found, returns (ticker, None).
        """
        params = {
            "timespan": timespan,
            "adjusted": "true",
            "window": "14",
            "series_type": "close",
            "order": "desc",
            "limit": "100",      
            "apiKey": self.api_key
        }
        url = f"https://api.polygon.io/v1/indicators/rsi/{ticker}"
        
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()      # Raise an exception for 4xx/5xx errors
                data = await response.json()
                # Safely extract the RSI value if it exists
                results = data.get("results", {})
                values = results.get("values", [])
                if values:
                    # "order=desc" ensures the first item in `values` is the latest
                    return ticker, values[0]["value"]
                else:
                    return ticker, None
        except Exception:
            # Handle network/API errors
            return ticker, None

    async def fetch_rsi_for_tickers(self, tickers: list[str], timespan:str='day') -> dict[str, float | None]:
        """
        Fetch the latest RSI for multiple tickers concurrently.
        Returns a dict: { ticker: latest_rsi_value_or_None }.
        """
        async with aiohttp.ClientSession() as session:
            # Create a task for each ticker
            tasks = [
                asyncio.create_task(self.fetch_latest_rsi(session, ticker, timespan=timespan))
                for ticker in tickers
            ]
            # Run tasks concurrently
            results = await asyncio.gather(*tasks)
            # Convert list of tuples into a dictionary { ticker: rsi }
            return dict(results)


    def extract_rsi_value(self, rsi_data):
        """Helper method to extract the most recent RSI value safely."""
        try:
            if rsi_data and 'results' in rsi_data:
                values = rsi_data['results'].get('values')
                if values and len(values) > 0:
                    return values[-1]['value']  # Get the latest RSI value
        except Exception as e:
            print(f"Error extracting RSI value: {e}")
        return None
    async def rsi_snapshot(self, tickers: List[str]) -> pd.DataFrame:
        """
        Gather a snapshot of the RSI across multiple timespans for multiple tickers.
        """
        timespans = ['minute', 'day', 'hour', 'week', 'month']
        tasks = []
        for timespan in timespans:
            tasks.append(self.rsi(tickers, timespan))

        # Run RSI calculations concurrently for all timespans
        rsi_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Aggregate the results
        aggregated_data = {}
        for timespan, rsi_data in zip(timespans, rsi_results):
            if isinstance(rsi_data, Exception):
                print(f"Error fetching RSI data for timespan '{timespan}': {rsi_data}")
                continue
            for ticker, data in rsi_data.items():
                if ticker not in aggregated_data:
                    aggregated_data[ticker] = {}
                rsi_value = self.extract_rsi_value(data)
                if rsi_value is not None:
                    aggregated_data[ticker][f"{timespan}_rsi"] = rsi_value

        # Convert aggregated data to DataFrame
        records = []
        for ticker, rsi_values in aggregated_data.items():
            record = {'ticker': ticker}
            record.update(rsi_values)
            if len(rsi_values) > 0:
                records.append(record)

        if records:
            df = pd.DataFrame(records)
            return df
        else:
            print("No RSI data available for the provided tickers.")
            return None



    async def fetch_rsi_with_ema10_for_tickers(self, tickers: list[str], timespan: str) -> dict[str, float | None]:
        """
        Fetch the latest RSI (calculated with EMA10) for multiple tickers concurrently.
        Returns a dict: { ticker: latest_rsi_value_or_None }.
        """
        async with aiohttp.ClientSession() as session:
            results = {}

            for ticker in tickers:
                # Fetch price data for the current ticker
                try:
                    price_data = await poly.get_price(ticker)
                    
                    if price_data and len(price_data) >= 10:  # Ensure we have enough data
                        prices_series = pd.Series(price_data)  # Convert to a pandas Series
                        rsi_series = self.calculate_rsi_with_ema10(prices_series)  # Calculate RSI
                        results[ticker] = rsi_series.iloc[-1]  # Get the latest RSI value
                    else:
                        results[ticker] = None  # Not enough data
                except Exception as e:
                    print(f"Error fetching data for {ticker}: {e}")
                    results[ticker] = None  # Handle errors gracefully

            return results
        
    async def get_option_chain_all(
        self,
        underlying_asset: str,
        strike_price: float = None,
        strike_price_lte: float = None,
        strike_price_gte: float = None,
        expiration_date: str = None,
        expiration_date_gte: str = None,
        expiration_date_lte: str = None,
        contract_type: str = None,
        order: str = None,
        limit: int = 250,
        sort: str = None,
        insert: bool = False
    ):
        """
        Retrieve all options contracts for a specific underlying asset (ticker symbol) across multiple pages.
        """
        try:
            if not underlying_asset:
                raise ValueError("Underlying asset ticker symbol must be provided.")

            # Handle special case for index assets (e.g., "I:SPX" for S&P 500 Index)
            if underlying_asset.startswith("I:"):
                underlying_asset = underlying_asset.replace("I:", "")

            # Build query parameters
            params = {
                'strike_price': strike_price,
                'strike_price.lte': strike_price_lte,
                'strike_price.gte': strike_price_gte,
                'expiration_date': expiration_date,
                'expiration_date.gte': expiration_date_gte,
                'expiration_date.lte': expiration_date_lte,
                'contract_type': contract_type,
                'order': order,
                'limit': limit,
                'sort': sort
            }

            # Filter out None values
            params = {key: value for key, value in params.items() if value is not None}

            # Construct the API endpoint and query string
            endpoint = f"https://api.polygon.io/v3/snapshot/options/{underlying_asset}"
            if params:
                query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
                endpoint += '?' + query_string
            endpoint += f"&apiKey={self.api_key}"

            logging.debug(f"Fetching option chain data for {underlying_asset} with query: {params}")

            # Fetch the data using asynchronous pagination
            response_data = await self.paginate_concurrent(endpoint)

            # Parse response data into a structured option snapshot object
            option_data = UniversalOptionSnapshot(response_data)

            # Insert into the database if specified
            if insert:
                logging.info("Inserting option chain data into the database.")
                await self.connect()  # Ensure connection to the database
                await self.batch_insert_dataframe(
                    option_data.df,
                    table_name='all_options',
                    unique_columns='option_symbol'
                )

            logging.info("Option chain data retrieval successful.")
            return option_data

        except ValueError as ve:
            logging.error(f"ValueError occurred: {ve}")
            return None
        except Exception as e:
            logging.error(f"An error occurred while fetching the option chain: {e}")
            return None
    def check_macd_sentiment(self, hist: list) -> str:
        """
        Analyze the MACD histogram to determine sentiment.
        - Returns 'bullish' if the histogram shows a bullish setup (near -0.02 and trending upward).
        - Returns 'bearish' if the histogram shows a bearish setup (near +0.02 and trending downward).
        - Returns '-' if no clear signal is detected.

        'hist' should be a list of histogram values in reverse-chronological order (index 0 = newest).
        """
        try:
            if hist is None or len(hist) < 3:
                return '-'

            # Extract the last three values
            last_three_values = hist[:3]

            # Check for bullish sentiment: close to -0.02 and trending upward
            if (
                abs(last_three_values[0] + 0.02) < 0.04 and
                all(last_three_values[i] > last_three_values[i + 1] for i in range(len(last_three_values) - 1))
            ):
                return 'bullish'

            # Check for bearish sentiment: close to +0.02 and trending downward
            if (
                abs(last_three_values[0] - 0.02) < 0.04 and
                all(last_three_values[i] < last_three_values[i + 1] for i in range(len(last_three_values) - 1))
            ):
                return 'bearish'

            return '-'

        except Exception as e:
            print(f"Error in check_macd_sentiment: {e}")
            return '-'
    async def fetch_macd(self, session: aiohttp.ClientSession, ticker: str, timespan: str = 'day') -> pd.DataFrame:
        """
        Fetch MACD data for `ticker`.
        Merge MACD data into a single DataFrame with columns:
            [timestamp, macd, signal, histogram, sentiment]

        If any error occurs, returns an empty DataFrame.
        """
        # 1) Fetch MACD data (Polygon Indicators endpoint).
        params = {
            "timespan": timespan,
            "adjusted": "true",
            "short_window": "12",
            "long_window": "26",
            "signal_window": "9",
            "series_type": "close",
            "order": "desc",    # newest data first
            "limit": "100",
            "apiKey": self.api_key
        }
        url = f"https://api.polygon.io/v1/indicators/macd/{ticker}"

        try:
            async with session.get(url, params=params) as resp:
                resp.raise_for_status()
                data = await resp.json()

            # Check for "results" or bail
            results = data.get("results", {})
            if not results:
                return pd.DataFrame()

            # Build a DataFrame of MACD values
            macd_values = results.get("values", [])
            if not macd_values:
                return pd.DataFrame()

            df_macd = pd.DataFrame(macd_values)
            # The Polygon MACD response typically has:
            #   "histogram", "signal", "timestamp", "value" (the MACD line)
            # We'll rename "value" to "macd" for clarity
            df_macd.rename(
                columns={
                    "histogram": "histogram",
                    "signal": "signal",
                    "timestamp": "timestamp",
                    "value": "macd",
                },
                inplace=True
            )
            # Sort by timestamp ascending for easier analysis
            df_macd.sort_values("timestamp", inplace=True)
            df_macd.reset_index(drop=True, inplace=True)
            df_macd = df_macd[::-1]
            # Calculate sentiment for the entire DataFrame
            df_macd["sentiment"] = self.check_macd_sentiment(
                df_macd["histogram"].tolist()
            )

            # Convert timestamp from milliseconds to datetime
            df_macd['timestamp'] = pd.to_datetime(df_macd['timestamp'], unit='ms')


            # Localize the timestamps to UTC (assumes current timestamps are in UTC)
            df_macd['timestamp'] = df_macd['timestamp'].dt.tz_localize('UTC')

            # Convert timestamps to Eastern Time (ET)
            df_macd['timestamp'] = df_macd['timestamp'].dt.tz_convert('US/Eastern')
            df_macd = df_macd.sort_values(by='timestamp', ascending=True).reset_index(drop=True)
            return df_macd

        except Exception as e:
            print(f"Error fetching MACD data for {ticker}: {e}")
            return pd.DataFrame()

    async def fetch_macd_signals_for_tickers(self, tickers: List[str], timespan: str = 'day') -> Dict[str, pd.DataFrame]:
        """
        Fetch the MACD + underlying data for multiple tickers concurrently.
        Returns a dict of { "TICKER": merged_df }.
        Each `merged_df` has columns: [timestamp, open, high, low, close, volume, macd, signal, histogram, sentiment]
        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            for t in tickers:
                tasks.append(
                    asyncio.create_task(self.fetch_macd(session, t, timespan=timespan))
                )
            dataframes = await asyncio.gather(*tasks)

        # Map each ticker to its resulting dataframe
        results = {}
        for ticker, df in zip(tickers, dataframes):
            results[ticker] = df


    async def paginate_concurrent(self, url, as_dataframe=False, concurrency=250):
        """
        Concurrently paginates through polygon.io endpoints that contain the "next_url".
        """
        all_results = []
        pages_to_fetch = [url]

        while pages_to_fetch:
            tasks = []
            for _ in range(min(concurrency, len(pages_to_fetch))):
                next_url = pages_to_fetch.pop(0)
                tasks.append(self.fetch_page(next_url))

            results = await asyncio.gather(*tasks)
            if results is not None:
                for data in results:
                    if data is not None:
                        if "results" in data:
                            all_results.extend(data["results"])
                        next_url = data.get("next_url")
                        if next_url:
                            next_url += f'&{urlencode({"apiKey": f"{self.api_key}"})}'
                            pages_to_fetch.append(next_url)
                    else:
                        break

        if as_dataframe:
            return pd.DataFrame(all_results)
        else:
            return all_results
    def chunk_list(self, data, chunk_size):
        """Split a list into smaller chunks."""
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]
    async def fetch_page(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()

    # ------------------------------------------------
    #  NEW: Multi-ticker concurrency
    # ------------------------------------------------
    async def get_option_chain_for_tickers(
        self,
        tickers: list[str],
        strike_price: float = None,
        strike_price_lte: float = None,
        strike_price_gte: float = None,
        expiration_date: str = None,
        expiration_date_gte: str = None,
        expiration_date_lte: str = None,
        contract_type: str = None,
        order: str = None,
        limit: int = 250,
        sort: str = None,
        insert: bool = False,
        concurrency: int = 50  # <-- Control your concurrency here
    ) -> dict[str, UniversalOptionSnapshot | None]:
        """
        Fetch option chain data for multiple tickers concurrently.
        Uses a semaphore to limit concurrency (instead of chunking).

        Returns:
            A dict mapping each ticker to either:
            - A UniversalOptionSnapshot object (if successful),
            - or None (if an error occurred).
        """
        out = {}

        # Define an inner async function that respects the semaphore
        async def fetch_with_semaphore(sem: asyncio.Semaphore, ticker: str):
            async with sem:
                try:
                    # Call your existing "get_option_chain_all" method
                    data = await self.get_option_chain_all(
                        underlying_asset=ticker,
                        strike_price=strike_price,
                        strike_price_lte=strike_price_lte,
                        strike_price_gte=strike_price_gte,
                        expiration_date=expiration_date,
                        expiration_date_gte=expiration_date_gte,
                        expiration_date_lte=expiration_date_lte,
                        contract_type=contract_type,
                        order=order,
                        limit=limit,
                        sort=sort,
                        insert=insert
                    )
                    return (ticker, data)
                except Exception as exc:
                    logging.error(f"Error fetching {ticker}: {exc}")
                    return (ticker, None)

        # Create a semaphore to limit concurrency
        semaphore = asyncio.Semaphore(concurrency)

        # Kick off all tasks at once
        tasks = [
            asyncio.create_task(fetch_with_semaphore(semaphore, ticker))
            for ticker in tickers
        ]

        # Gather all results
        results = await asyncio.gather(*tasks)

        # Build the output dictionary
        for ticker, data in results:
            out[ticker] = data

        return out


    async def fetch_option_aggregates(self,
        session: aiohttp.ClientSession,
        symbol: str,
        multiplier: int,
        timespan: str,
        date_from: str,
        date_to: str,
        adjusted: bool = True,
        sort: str = "asc",
        limit: int = 5000,
    ) -> pd.DataFrame:
        """
        Fetch aggregate bars from Polygon for a single option symbol.
        Returns a pandas DataFrame with parsed columns and converted timestamps.
        """

        url = (
            f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/"
            f"{multiplier}/{timespan}/{date_from}/{date_to}"
            f"?adjusted={str(adjusted).lower()}"
            f"&sort={sort}"
            f"&limit={limit}"
            f"&apiKey={self.api_key}"
        )

        async with session.get(url) as response:
            data = await response.json()

        # Check for errors (e.g., status != 'OK')
        if data.get("status") != "OK":
            # In your production code, handle error logic here
            raise ValueError(
                f"Request for {symbol} returned an unexpected status: {data.get('status')}"
            )

        results = data.get("results", [])
        if not results:
            # Return empty DataFrame if there are no results
            return pd.DataFrame()

        # Convert the JSON results to a DataFrame
        df = pd.DataFrame(results)

        # Convert the Unix Msec timestamps in 't' to human-readable datetimes
        # Polygon returns timestamps in milliseconds, so divide by 1000
        df["t"] = pd.to_datetime(df["t"], unit="ms", utc=True)

        # Rename the columns to something more descriptive if desired
        df.rename(
            columns={
                "c": "close",
                "h": "high",
                "l": "low",
                "n": "transactions",
                "o": "open",
                "t": "timestamp",
                "v": "volume",
                "vw": "vwap",
            },
            inplace=True,
        )

        # Set index to timestamp if you prefer time-series style DataFrames
        df.set_index("timestamp", inplace=True, drop=True)

        return df
    

    async def fetch_option_aggs_for_tickers(self,
        symbols: list,
        multiplier: int,
        timespan: str,
        date_from: str,
        date_to: str,
        adjusted: bool = True,
        sort: str = "asc",
        limit: int = 5000,
    ) -> dict:
        """
        Fetch aggregate bars for multiple option symbols concurrently.
        Returns a dictionary of DataFrames, keyed by symbol.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch_option_aggregates(
                    session,
                    symbol,
                    multiplier,
                    timespan,
                    date_from,
                    date_to,
                    adjusted,
                    sort,
                    limit,
                )
                for symbol in symbols
            ]

            # Gather all tasks (run them concurrently)
            results = await asyncio.gather(*tasks)

        # Combine each DataFrame into a dictionary keyed by symbol
        return {symbol: df for symbol, df in zip(symbols, results)}





    async def get_candle_data(
        self,
        ticker: str,
        interval: str,
        count: str = '800',
        timestamp: Optional[int] = None,
        client: Optional[httpx.AsyncClient] = None
    ) -> pd.DataFrame:
        """
        Fetch Webull candle data for a single ticker and interval.
        Optionally reuses an external httpx.AsyncClient session for concurrency.
        """
        try:
            # Handle Webull index tickers
            original_ticker = ticker
            if ticker == 'I:SPX':
                ticker = 'SPX'
            elif ticker == 'I:NDX':
                ticker = 'NDX'
            elif ticker == 'I:VIX':
                ticker = 'VIX'
            elif ticker == 'I:RUT':
                ticker = 'RUT'
            elif ticker == 'I:XSP':
                ticker = 'XSP'

            # Default to the current timestamp if none provided
            if timestamp is None:
                timestamp = int(time.time())

            # Retrieve the Webull ID for the ticker
            tickerid = await self.get_webull_id(ticker)

            # Build the URL
            base_fintech_gw_url = (
                f'https://quotes-gw.webullfintech.com/api/quote/charts/query-mini'
                f'?tickerId={tickerid}&type={interval}&count={count}'
                f'&timestamp={timestamp}&restorationType=1&extendTrading=1'
            )

            # Define user-friendly labels for intervals (if needed)
            interval_mapping = {
                'm5': '5 min',
                'm30': '30 min',
                'm60': '1 hour',
                'm120': '2 hour',
                'm240': '4 hour',
                'd': 'day',
                'w': 'week',
                'm': 'month'
            }
            timespan = interval_mapping.get(interval, interval)  # Not strictly required

            # If a shared client isn't provided, create a new one just for this call
            session_provided = True
            if client is None:
                client = httpx.AsyncClient(headers=self.wb_headers)
                session_provided = False

            try:
                response = await client.get(base_fintech_gw_url)
                response.raise_for_status()
                data_json = response.json()

                # The returned JSON often looks like: [ { "data": [...], ... } ]
                if data_json and isinstance(data_json, list) and 'data' in data_json[0]:
                    raw_data = data_json[0]['data']

                    # Each row from Webull is comma-separated
                    split_data = [row.split(",") for row in raw_data]
                    df = pd.DataFrame(
                        split_data,
                        columns=['Timestamp', 'Open', 'Close', 'High', 'Low', 'Vwap', 'Volume', 'Avg']
                    )

                    # Convert Timestamp from int => datetime
                    df['Timestamp'] = pd.to_numeric(df['Timestamp'], errors='coerce')
                    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', utc=True)

                    # Convert UTC => US/Eastern, then remove the timezone
                    df['Timestamp'] = df['Timestamp'].dt.tz_convert('US/Eastern').dt.tz_localize(None)

                    # Attach extra info
                    df['Ticker'] = original_ticker
                    df['timespan'] = interval

                    # Format the Timestamp column into ISO-8601 strings
                    df['Timestamp'] = df['Timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')

                    # Reverse the DataFrame so earliest date is first
                    # (Depending on how Webull returns data, you may or may not want this)
                    df = df.iloc[::-1].reset_index(drop=True)
                    df['Close'] = df['Close'].astype(float)
                    df['Open'] = df['Open'].astype(float)
                    df['High'] = df['High'].astype(float)
                    df['Low'] = df['Low'].astype(float)
                    df['Volume'] = df['Volume'].astype(float)
                    df['Vwap'] = df['Vwap'].astype(float)
                    return df

                # If the response is empty or malformed, return an empty DataFrame
                return pd.DataFrame()

            finally:
                # Only close the session if we created it in this function
                if not session_provided:
                    await client.aclose()

        except Exception as e:
            print(f"Error fetching data for {ticker} ({interval}): {e}")
            return pd.DataFrame()

    async def get_candle_data_for_tickers_and_intervals(self, tickers, intervals, count='800'):
        """
        Fetch candle data for multiple tickers and multiple intervals concurrently.
        Returns a nested dict like: { ticker: { interval: DataFrame } }.
        """
        # We'll store results in a nested dict
        results = {}
        async with httpx.AsyncClient(headers=self.wb_headers) as client:
            tasks = []
            task_info = []
            for ticker in tickers:
                for interval in intervals:
                    # Create a coroutine (but don't await yet)
                    task = self.get_candle_data(
                        ticker=ticker,
                        interval=interval,
                        count=count,
                        client=client
                    )
                    tasks.append(task)
                    task_info.append((ticker, interval))

            # Run all requests in parallel
            fetched_data = await asyncio.gather(*tasks, return_exceptions=True)

        # Attach each fetched DataFrame to its ticker/interval
        for (ticker, interval), df in zip(task_info, fetched_data):
            if ticker not in results:
                results[ticker] = {}
            if isinstance(df, Exception):
                print(f"Failed to fetch data for {ticker} @ {interval}: {df}")
                results[ticker][interval] = pd.DataFrame()
            else:
                results[ticker][interval] = df

        return results
    

    async def get_candle_data_for_tickers(self, tickers, interval, count='800'):
        """
        Fetch candle data for multiple tickers concurrently using a shared HTTP session.
        Returns a dictionary {ticker: DataFrame}.
        """
        results = {}
        async with httpx.AsyncClient(headers=self.wb_headers) as client:
            # Prepare all tasks
            tasks = [
                self.get_candle_data(
                    ticker=ticker,
                    interval=interval,
                    count=count,
                    client=client
                )
                for ticker in tickers
            ]
            # Run tasks in parallel
            fetched_data = await asyncio.gather(*tasks, return_exceptions=True)

        # Combine each DataFrame into a dictionary keyed by ticker
        for ticker, df in zip(tickers, fetched_data):
            if isinstance(df, Exception):
                print(f"Failed to fetch data for {ticker}: {df}")
                results[ticker] = pd.DataFrame()
            else:
                results[ticker] = df

        return results
    

    async def fetch_option_trades(
        self,
        session: aiohttp.ClientSession,
        symbol: str,
        start_timestamp: str = None,
        end_timestamp: str = None,
        order: str = "asc",
        sort: str = "sip_timestamp",
        limit: int = 1000,
    ) -> pd.DataFrame:
        """
        Fetch trade data for a single option symbol from Polygon's v3/trades endpoint,
        then add a 'notional_value' column, as well as global scalar columns for
        lowest/highest trade prices (and timestamps) plus highest trade size (and timestamp).
        """

        # Base URL for the trades endpoint
        base_url = f"https://api.polygon.io/v3/trades/{symbol}"
        
        # Build initial query params
        params = {
            "limit": limit,
            "apiKey": self.api_key,
            "order": order,
            "sort": sort,
        }
        if start_timestamp:
            params["timestamp.gte"] = start_timestamp
        if end_timestamp:
            params["timestamp.lte"] = end_timestamp

        all_results = []
        next_url = None

        while True:
            if next_url:
                url = next_url
                query_params = {}
            else:
                url = base_url
                query_params = params

            async with session.get(url, params=query_params) as response:
                data = await response.json()

            status = data.get("status", None)
            if status != "OK":
                raise ValueError(
                    f"Request for {symbol} returned an unexpected status: {status}"
                )

            results = data.get("results", [])
            if not results:
                # No trades found or no more pages
                break

            all_results.extend(results)
            next_url = data.get("next_url", None)
            if next_url is not None:
                next_url += f'&{urlencode({"apiKey": f"{self.api_key}"})}'
            if not next_url:
                break

        if not all_results:
            # Return an empty DataFrame if no trades
            return pd.DataFrame()

        # Convert results -> DataFrame
        df = pd.DataFrame(all_results)
        df['option_symbol'] = symbol
        components = get_human_readable_string(symbol)
        strike = components.get('strike_price')
        expiry = components.get('expiry_date')
        cp = components.get('call_put')
        ticker = components.get('underlying_symbol')
        df['ticker'] = ticker
        df['strike'] = strike
        df['call_put'] = cp
        df['expiry'] = expiry

        if "sip_timestamp" in df.columns:
            df["sip_timestamp"] = pd.to_datetime(
                df["sip_timestamp"], unit="ns", utc=True
            ).dt.strftime("%Y-%m-%d %H:%M:%S.%f%z")  # Convert to string format

        # Rename for clarity
        df.rename(
            columns={
                "sip_timestamp": "sip_datetime",
            },
            inplace=True,
        )

        # --------------------------------------------------------------------
        # 1) Compute the notional value per trade:
        #     notional = trade_size * (price * 100)
        # --------------------------------------------------------------------
        if {"size", "price"}.issubset(df.columns):
            df["notional_value"] = df["size"] * (df["price"] * 100.0)
        else:
            # In case the data is missing these columns, handle accordingly
            df["notional_value"] = None

        # --------------------------------------------------------------------
        # 2) Compute global scalar metrics for the entire DataFrame:
        #    lowest trade price, highest trade price, highest trade size,
        #    plus each of their timestamps.
        # --------------------------------------------------------------------
        # ------------------------------------------------------------------------------
        # Convert "conditions" from [int] -> int -> label
        # conditions is always a one-item list, e.g. conditions = [209]
        # ------------------------------------------------------------------------------
        if "conditions" in df.columns:
            # Extract the integer from the one-item list
            df["condition_code"] = df["conditions"].apply(
                lambda arr: arr[0] if isinstance(arr, list) and len(arr) > 0 else None
            )
            # Map the integer to a descriptive string
            df["condition_label"] = df["condition_code"].map(option_condition_dict)

        # ------------------------------------------------------------------------------
        # Convert "exchange" from int -> label
        # ------------------------------------------------------------------------------
        if "exchange" in df.columns:
            df["exchange_label"] = df["exchange"].map(OPTIONS_EXCHANGES)
        if "price" in df.columns:
            lowest_price = df["price"].min()
            highest_price = df["price"].max()

            # idxmin/idxmax -> gets the row index where the price is min/max
            lowest_price_idx = df["price"].idxmin()
            highest_price_idx = df["price"].idxmax()

            lowest_price_ts = (
                df.loc[lowest_price_idx, "sip_datetime"]
                if pd.notnull(lowest_price_idx)
                else None
            )
            highest_price_ts = (
                df.loc[highest_price_idx, "sip_datetime"]
                if pd.notnull(highest_price_idx)
                else None
            )

            # Insert these metrics as columns of repeated scalars (so that each row has them)
            df["lowest_price"] = lowest_price
            df["lowest_price_timestamp"] = lowest_price_ts
            df["highest_price"] = highest_price
            df["highest_price_timestamp"] = highest_price_ts

        # Highest trade size
        if "size" in df.columns:
            highest_size = df["size"].max()
            highest_size_idx = df["size"].idxmax()
            highest_size_ts = (
                df.loc[highest_size_idx, "sip_datetime"]
                if pd.notnull(highest_size_idx)
                else None
            )
            df["highest_trade_size"] = highest_size
            df["highest_trade_timestamp"] = highest_size_ts

        return df

    async def fetch_option_trades_for_tickers(
        self,
        symbols: list,
        start_timestamp: str = None,
        end_timestamp: str = None,
        order: str = "asc",
        sort: str = "sip_timestamp",
        limit: int = 1000,
    ) -> dict:
        """
        Concurrently fetch trade data for multiple option symbols.
        Returns a dict of DataFrames keyed by symbol. Each DataFrame includes
        the notional_value and scalar metrics as computed in fetch_option_trades().
        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            for symbol in symbols:
                task = self.fetch_option_trades(
                    session,
                    symbol,
                    start_timestamp,
                    end_timestamp,
                    order,
                    sort,
                    limit,
                )
                tasks.append(task)

            results = await asyncio.gather(*tasks)

        return {symbol: df for symbol, df in zip(symbols, results)}
    
    async def fetch_ticker_news(
        self,
        session: aiohttp.ClientSession,
        ticker: str,
    ) -> pd.DataFrame:
        """
        Fetch up to 1000 recent news articles for a single ticker from Polygon's
        /v2/reference/news endpoint (one request, no pagination).

        Normalizes nested data:
          - Extracts publisher fields into top-level columns
          - Extracts the first item of `insights` into columns
          - Joins 'keywords' and 'tickers' into comma-separated strings
        """
        try:

            async with session.get(f"https://api.polygon.io/v2/reference/news?ticker={ticker}&limit=100&apiKey={self.api_key}") as response:
                data = await response.json()
                results = data['results']


                insights = [i.get('insights') for i in results]
                insights = [item for sublist in insights for item in sublist]
                ticker = [i.get('ticker') for i in insights]
                sentiment = [i.get('sentiment') for i in insights]
                sent_reason = [i.get('sentiment_reasoning') for i in insights]


                df = pd.DataFrame({ 
                    'ticker': ticker,
                    'sentiment': sentiment,
                    'sentiment_reason': sent_reason
                })
                print(df)
                return df

        except Exception as e:
            print(e)

    async def fetch_ticker_news_for_symbols(
        self,
        symbols: list,
    ) -> dict:
        """
        Fetch up to 1000 recent news articles concurrently for multiple tickers
        from Polygon's /v2/reference/news endpoint (one request per symbol, no pagination).

        Normalizes nested data similarly to fetch_ticker_news.

        Returns
        -------
        dict : {ticker: pd.DataFrame}
        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            for sym in symbols:
                task = self.fetch_ticker_news(
                    session,
                    sym,
                )
                tasks.append(task)

            # Gather all tasks (run them concurrently)
            results = await asyncio.gather(*tasks)

        # Combine each DataFrame into a dict keyed by the symbol
        return {symbol: df for symbol, df in zip(symbols, results)}