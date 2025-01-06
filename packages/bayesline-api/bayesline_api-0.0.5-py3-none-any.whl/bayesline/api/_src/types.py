import datetime as dt
from typing import Any, Literal

import pandas as pd

IdType = Literal[
    "ticker", "composite_figi", "cik", "qaid", "cusip", "isin", "sedol", "bayesid"
]
DateLike = str | dt.date | dt.datetime | pd.Timestamp
DataFrameFormat = Literal["unstacked", "stacked"]
DNFFilterExpression = tuple[str, str, Any]
DNFFilterExpressions = list[DNFFilterExpression | list[DNFFilterExpression]]
