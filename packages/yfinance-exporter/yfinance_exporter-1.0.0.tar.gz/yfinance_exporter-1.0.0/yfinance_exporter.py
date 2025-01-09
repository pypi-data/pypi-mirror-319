#!/usr/bin/env python3

import logging

from prometheus_client import Gauge, start_http_server
from datetime import datetime
import time
from the_conf import TheConf
from yfinance import Ticker

metaconf = {
    "source_order": ["files"],
    "config_files": [
        "~/.config/yfinance-exporter.json",
        "/etc/yfinance-exporter/yfinance-exporter.json",
    ],
    "parameters": [
        {
            "type": "list",
            "stocks": [
                {"name": {"type": str}},
                {"isin": {"type": str}},
                {"ycode": {"type": str}},
            ],
        },
        {
            "loop": [
                {"interval": {"type": int, "default": 240}},
            ]
        },
        {
            "prometheus": [
                {"port": {"type": int, "default": 9100}},
                {"namespace": {"type": str, "default": ""}},
            ]
        },
        {"logging": [{"level": {"default": "WARNING"}}]},
    ],
}
conf = TheConf(metaconf)
logger = logging.getLogger("yfinance-exporter")
try:
    logger.setLevel(getattr(logging, conf.logging.level))
    logger.addHandler(logging.StreamHandler())
except AttributeError as error:
    raise AttributeError(
        f"{conf.logging.level} isn't accepted, only DEBUG, INFO, WARNING, "
        "ERROR and FATAL are accepted"
    ) from error

YFINANCE_EXPORTER = Gauge(
    "yfinance_exporter",
    "",
    ["status"],
    namespace=conf.prometheus.namespace,
)
STOCK = Gauge(
    "financial_positions",
    "",
    [
        "bank",
        "account_type",
        "account_name",
        "account_id",
        "line_name",
        "line_id",
        "value_type",  # par-value, shares-value, gain, gain-percent, quantity
    ],
    namespace=conf.prometheus.namespace,
)


def collect(stock):
    logger.debug("Collecting for %r", stock.name)
    labels = [
        stock.ycode.split(".")[1] if "." in stock.ycode else "",
        "stocks",
        "market",
        "market",
        stock.name,
        stock.isin,
        "par-value",
    ]
    ticker = Ticker(stock.ycode)
    try:
        value = ticker.fast_info["last_price"]
    except KeyError:
        value = None
    if not isinstance(value, (int, float)):
        try:
            STOCK.remove(*labels)
        except KeyError:
            pass
        return False
    STOCK.labels(*labels).set(value)
    return True


def main():
    YFINANCE_EXPORTER.labels("loop-count").set(0)
    while True:
        start = datetime.now()

        results = {"ok-stock": 0, "ko-stock": 0}
        for stock in conf.stocks:
            if collect(stock):
                results["ok-stock"] += 1
            else:
                results["ko-stock"] += 1

        exec_interval = (datetime.now() - start).total_seconds()
        YFINANCE_EXPORTER.labels("loop-duration-second").set(exec_interval)
        YFINANCE_EXPORTER.labels("loop-count").inc()
        for result, count in results.items():
            YFINANCE_EXPORTER.labels(result).set(count)

        interval = conf.loop.interval - exec_interval
        if interval > 0:
            time.sleep(interval)


if __name__ == "__main__":
    logger.info(
        "Starting yfinance exporter with %d stocks to watch", len(conf.stocks)
    )
    start_http_server(conf.prometheus.port)
    main()
