import datetime
import polars as pl


def filter_date_range(df: pl.DataFrame, date_range: list):
    if len(date_range) != 2:
        return df
    start, end = date_range
    return df.filter(
        (pl.col("Date") >= pl.lit(start)) & (pl.col("Date") <= pl.lit(end))
    )


def from_dtn_to_age(born: datetime.date):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
