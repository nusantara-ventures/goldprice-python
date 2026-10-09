# Goldprice for Python

Python clients for precious metal prices from goldprice.dev. Read spot prices,
price history, bars, ratios, and account usage. Conversion methods cover amounts
and carat values. The package provides synchronous and asynchronous access.

## Install

Requires Python 3.10 or newer.

```sh
pip install goldprice-dev
```

## Quickstart

Set `GOLDPRICE_API_KEY` in your environment, then run:

```python
from goldprice_dev import Goldprice

with Goldprice() as client:
    spot = client.prices.spot("XAU-USD-SPOT")
    print(spot.price)
    print(spot.meta.request_id)
```

The context manager closes the client. `AsyncGoldprice` provides asynchronous
access. Supply `api_key=` to configure a key explicitly. The default base URL
is `https://api.goldprice.dev`; override it with `GOLDPRICE_BASE_URL`.

Use `prices.list()` for price listings and `prices.history(...)` for a symbol's
history. `bars.latest(symbol=...)` and `ratios.latest(pair=...)` return the latest
bar or ratio. `account.usage()` reads account usage. History queries accept
`from_` and `to` keyword arguments.

## Decimals

Prices and other decimal values use exact `decimal.Decimal` objects, never
floats. Pass conversion amounts as strings to preserve decimal input.

Every response carries `meta` with `request_id` and rate-limit values from
headers. Bar and ratio pages expose the wire field named `meta` as `meta_`.
Use `meta_` for page data and `meta` for response information.

## Errors and retries

`errors.Unauthorized`, `errors.RateLimited`, `errors.NotFound`, and
`errors.BadRequest` extend `errors.ApiError`. API errors expose `status`, `code`,
`detail`, and `request_id`. `errors.RateLimited` also carries `retry_after`.
All client errors derive from `errors.GoldpriceError`. Import `errors` from
`goldprice_dev` when handling these exceptions.

Requests retry up to twice by default for short-window rate limits and temporary
unavailability. Quota exhaustion is not retried.

## Pagination iterators

Use `bars.list_iter(...)` and `ratios.list_iter(...)` to consume items across
pages. Use `for` with `Goldprice` and `async for` with `AsyncGoldprice`.
The corresponding `list(...)` methods return a single page.

Links: [Documentation](https://goldprice.dev/docs)

MIT licensed
