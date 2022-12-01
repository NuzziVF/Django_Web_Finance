import pandas as pd
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "A command to add data from an Excel file to the database"

    # if file_extension == 'xlsx':
    #     df = pd.read_excel(file.read(), engine='openpyxl')
    # elif file_extension == 'xls':
    #     df = pd.read_excel(file.read())
    # elif file_extension == 'csv':
    #     df = pd.read_csv(file.read())
    def handle(self, *args, **options):
        excel_file = "stonks.xlsx"
        df = pd.read_excel(excel_file, engine="openpyxl")
        print(df)
