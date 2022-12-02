import pandas as pd
from django.core.management.base import BaseCommand
from login.models import *
from IPython.display import display
from alpha_vantage.timeseries import TimeSeries
from sqlalchemy import create_engine, String


class Command(BaseCommand):
    help = "A command to add data from an Excel file to the database"

    # if file_extension == 'xlsx':
    #     df = pd.read_excel(file.read(), engine='openpyxl')
    # elif file_extension == 'xls':
    #     df = pd.read_excel(file.read())
    # elif file_extension == 'csv':
    #     df = pd.read_csv(file.read())
    def handle(self, *args, **options):
        # excel_file = "stonks.xlsx"
        # df = pd.read_excel(excel_file, engine="openpyxl")

        engine = create_engine("sqlite:///db.sqlite3")

        api_key = "F71WF3729MHFB57L"

        ts = TimeSeries(
            key=api_key,
            output_format="pandas",
        )

        data = ts.get_daily_adjusted("MSFT")
        data = data[0].head(10)
        print("fail1")

        data.reset_index().to_sql(
            Stock._meta.db_table,
            if_exists="replace",
            con=engine,
            index=False,
            # index_label="Id",
            # dtype={"IdColumn": String(length=255)},
        )
        print(data)

        print("fail2")
        print("fail3")
        conv_dict = {
            "date": "date",
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. adjusted close": "adjusted_close",
            "6. volume": "volume",
            "7. dividend amount": "dividend_amount",
            "8. split coefficient": "split_coefficient",
        }

        new_df = data.rename(columns=conv_dict)
        print("fail4")
        print(new_df)

        new_df.reset_index().to_sql(
            Stock._meta.db_table,
            if_exists="replace",
            con=engine,
            index=True,
            index_label="Id",
            dtype={"IdColumn": String(length=255)},
        )

        print("success")
