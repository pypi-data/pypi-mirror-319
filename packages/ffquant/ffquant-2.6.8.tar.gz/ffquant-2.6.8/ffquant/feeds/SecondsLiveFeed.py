import pandas as pd
import backtrader as bt
import requests
import os
from datetime import datetime, timedelta, timezone
import time
import pytz
import queue
from ffquant.utils.Logger import stdout_log

__ALL__ = ['SecondsLiveFeed']

class SecondsLiveFeed(bt.feeds.DataBase):
    params = (
        ('url', f"{os.environ.get('FINTECHFF_FEED_BASE_URL', 'http://192.168.25.127:8288')}/symbol/info/list"),
        ('fromdate', None),
        ('todate', None),
        ('symbol', None),
        ('timeframe', bt.TimeFrame.Seconds),
        ('compression', 5),
        ('debug', False),
        ('max_retries', 60),
        ('backpeek_size', 60),
        ('backfill_size', 0),
    )

    lines = (('turnover'),)

    def __init__(self):
        self._timeframe = self.p.timeframe
        self._compression = self.p.compression
        super(SecondsLiveFeed, self).__init__()
        self.cache = {}
        self.hist_data_q = queue.Queue()

    def islive(self):
        return True

    def start(self):
        super().start()

        if self.p.backfill_size > 0:
            now = datetime.now()
            now = now - timedelta(seconds=now.second % 5, microseconds=now.microsecond)
            end_time = now
            end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

            start_time = (end_time - timedelta(seconds=self.p.backfill_size * 5)).replace(microsecond=0)
            start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')

            params = {
                'startTime': start_time_str,
                'endTime': end_time_str,
                'symbol': self.p.symbol,
                'interval': '5S'
            }

            if self.p.debug:
                stdout_log(f"SecondsLiveFeed, backfill params: {params}")

            response = requests.get(self.p.url, params=params).json()
            if self.p.debug:
                stdout_log(f"SecondsLiveFeed, backfill response: {response}")

            if response.get('code') != '200':
                raise ValueError(f"API request failed: {response}")

            results = response.get('results', [])
            results.sort(key=lambda x: x['timeOpen'])

            last_time_open = None
            for result in results:
                time_open = result["timeOpen"]
                if last_time_open is not None:
                    if time_open > last_time_open + 60 * 1000:
                        missing_ts = last_time_open + 60 * 1000
                        while missing_ts < time_open:
                            if self.p.debug:
                                stdout_log(f"SecondsLiveFeed, missing kline: {missing_ts} {datetime.fromtimestamp(missing_ts / 1000.0, timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')}")

                            v = self.hist_data_q.queue[-1]
                            if v is not None:
                                new_v = {
                                    'timeOpen': missing_ts,
                                    'timeClose': missing_ts + 60 * 1000,
                                    'createTime': missing_ts,
                                    'updateTime': missing_ts,
                                    'symbol': v['symbol'],
                                    'open': v['close'],
                                    'high': v['close'],
                                    'low': v['close'],
                                    'close': v['close'],
                                    'vol': 0.0,
                                    'turnover': 0.0,
                                    'type': v['type']
                                }
                                self.hist_data_q.put(new_v)
                            missing_ts += 60 * 1000

                self.hist_data_q.put(result)
                last_time_open = time_open


    def _load(self):
        if not self.hist_data_q.empty():
            history_item = self.hist_data_q.get()
            self.lines.datetime[0] = bt.date2num(datetime.fromtimestamp(history_item['timeOpen'] / 1000.0, timezone.utc))
            self.lines.open[0] = history_item['open']
            self.lines.high[0] = history_item['high']
            self.lines.low[0] = history_item['low']
            self.lines.close[0] = history_item['close']
            self.lines.volume[0] = history_item['vol']
            self.lines.turnover[0] = history_item['turnover']
            if self.p.debug:
                stdout_log(f"SecondsLiveFeed, hist_data_q size: {self.hist_data_q.qsize() + 1}, backfill from history, kline datetime: {self.lines.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')}")
            return True

        now = datetime.now()
        now = now - timedelta(seconds=now.second % 5, microseconds=now.microsecond)
        current_kline_time = (now - timedelta(seconds=1 * 5)).astimezone(pytz.utc)
        current_kline_time_str = current_kline_time.strftime('%Y-%m-%d %H:%M:%S')

        # _load method of live feed is invoked frequently
        # so only in following case we need to fetch data
        # 1. the very first bar
        # 2. the very first _load invoke in a new bar
        if self.lines.datetime.idx == 0 or self.lines.datetime.datetime(-1).strftime('%Y-%m-%d %H:%M:%S') != current_kline_time_str:
            start_time = (now - timedelta(seconds=1 * 5)).replace(microsecond=0)
            end_time = now
            start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
            end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

            retry_count = 0
            while retry_count < self.p.max_retries:
                retry_count += 1

                key = f"{current_kline_time_str}"
                if key not in self.cache:
                    params = {
                        'startTime': start_time_str,
                        'endTime': end_time_str,
                        'symbol': self.p.symbol,
                        'interval': '5S'
                    }

                    if self.p.debug:
                        stdout_log(f"SecondsLiveFeed, fetch data params: {params}")

                    response = requests.get(self.p.url, params=params).json()
                    if self.p.debug:
                        stdout_log(f"SecondsLiveFeed, fetch data response: {response}")

                    if response.get('code') != '200':
                        raise ValueError(f"API request failed: {response}")

                    results = response.get('results', [])
                    if results is not None and len(results) > 0:
                        self.cache[key] = results[0]

                bar = self.cache.get(key, None)
                if bar is not None:
                    self.lines.datetime[0] = bt.date2num(datetime.fromtimestamp(bar['timeOpen'] / 1000.0, timezone.utc))
                    self.lines.open[0] = bar['open']
                    self.lines.high[0] = bar['high']
                    self.lines.low[0] = bar['low']
                    self.lines.close[0] = bar['close']
                    self.lines.volume[0] = bar['vol']
                    self.lines.turnover[0] = bar['turnover']
                    return True
                else:
                    time.sleep(0.1)

            # no available data for current bar, so we backpeek for the most recent data
            self.backpeek_for_result(current_kline_time)

            # heartbeat info print
            stdout_log(f"[INFO], {self.__class__.__name__}, {current_kline_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')}, open: {self.lines.open[0]}, high: {self.lines.high[0]}, low: {self.lines.low[0]}, close: {self.lines.close[0]}")
            return True

    def backpeek_for_result(self, cur_kline_time):
        # update backpeek window
        end_time = cur_kline_time.astimezone()
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
        start_time = (end_time - timedelta(seconds=self.p.backpeek_size * 5)).replace(microsecond=0)
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        params = {
            'startTime': start_time_str,
            'endTime': end_time_str,
            'symbol': self.p.symbol,
            'interval': '5S'
        }
        if self.p.debug:
            stdout_log(f"SecondsLiveFeed, update backpeek window params: {params}")

        response = requests.get(self.p.url, params=params).json()
        if self.p.debug:
            stdout_log(f"SecondsLiveFeed, update backpeek window response: {response}")

        if response.get('code') != '200':
            raise ValueError(f"API request failed: {response}")
        results = response.get('results', [])
        results.sort(key=lambda x: x['timeOpen'])
        for result in results:
            key = datetime.fromtimestamp(result['timeOpen'] / 1000.0, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            self.cache[key] = result

        # preset the default values
        self.lines.datetime[0] = bt.date2num(datetime.fromtimestamp(cur_kline_time.timestamp(), timezone.utc))
        self.lines.open[0] = 0.0
        self.lines.high[0] = 0.0
        self.lines.low[0] = 0.0
        self.lines.close[0] = 0.0
        self.lines.volume[0] = 0.0
        self.lines.turnover[0] = 0.0

        backpeek_v = None
        for i in range(1, self.p.backpeek_size):
            k = (cur_kline_time - timedelta(seconds=i * 5)).strftime('%Y-%m-%d %H:%M:%S')
            backpeek_v = self.cache.get(k, None)
            if backpeek_v is not None:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, backpeek index: {i}, datetime: {(cur_kline_time - timedelta(seconds=i * 5)).astimezone().strftime('%Y-%m-%d %H:%M:%S')}, backpeek_v: {backpeek_v}")

                self.lines.datetime[0] = bt.date2num(datetime.fromtimestamp(int(cur_kline_time.timestamp()), timezone.utc))
                self.lines.open[0] = backpeek_v['close']
                self.lines.high[0] = backpeek_v['close']
                self.lines.low[0] = backpeek_v['close']
                self.lines.close[0] = backpeek_v['close']
                self.lines.volume[0] = 0.0
                self.lines.turnover[0] = 0.0
                break

        self.cache[cur_kline_time.strftime('%Y-%m-%d %H:%M:%S')] =  {
            'timeOpen': int(cur_kline_time.timestamp()) * 1000,
            'timeClose': (int(cur_kline_time.timestamp()) + 60) * 1000,
            'createTime': 0,
            'updateTime': 0,
            'symbol': self.p.symbol,
            'open': self.lines.open[0],
            'high': self.lines.high[0],
            'low': self.lines.low[0],
            'close': self.lines.close[0],
            'vol': 0.0,
            'turnover': 0.0,
            'type': '1'
        }

        if backpeek_v is not None:
            stdout_log(f"[CRITICAL], {self.__class__.__name__}, {cur_kline_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')} use backpeek from {datetime.fromtimestamp(backpeek_v['timeOpen'] / 1000.0, timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')}")

        if self.lines.close[0] == 0.0:
            stdout_log(f"[CRITICAL], {self.__class__.__name__}, {cur_kline_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')} close price is 0")