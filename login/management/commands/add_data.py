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

        data.reset_index().to_sql(
            Stock._meta.db_table,
            if_exists="replace",
            con=engine,
            index=True,
            index_label="Id",
            dtype={"IdColumn": String(length=255)},
        )

        print("success")
