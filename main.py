
import configparser

import pandas as pd
from tqdm import tqdm
import xlwings as xw

from co2e.filedialog_window import open_filedialog
from co2e.ceva_co2e import CevaCO2e


def main():

    file = open_filedialog()

    CONFIG_FILE = r"bin\variables.ini"
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    cfg = config['EXCEL COLUMN NAMES']
    
    POL = cfg['port-of-loading-column']
    POD = cfg['port-of-discharge-column']
    TRANSPORT = cfg['transport-type-column']
    WEIGHT = cfg['weight-column']
    CO2E_COL = cfg['co2e-calculation-column']

    UNLOCODE_FILE = config['FILE PATHS']['path-to-UNLOCODE-file']

    dict_of_keys = {
        "pol": POL,
        "pod": POD,
        "transport": TRANSPORT,
        "weight": WEIGHT,
    }

    # STEPS
    # 1) get dictionary of dataframes
    # 2) for each dataframe:
    # 3) filter na values
    # 4) look up values
    # 5) update original dataframe
    # 6) insert to excel

    # Creates a Dictionary of Dataframes
    dict_of_dfs = read_and_return_dfs(file)
    df_unlocode = get_unlocode_data(UNLOCODE_FILE)



    # Opens up Excel file with Xlwings for smoother handling
    with xw.App(visible=False) as app:
        wb = app.books.open(file)

        # Loop each DataFrame in Dict
        for sheet, df in tqdm(dict_of_dfs.items(), desc="Outer loop", position=0):
            # Filter NA values
            filtered_df = filter_df(df, CO2E_COL, **dict_of_keys)

            # Look up values on web
            list_of_co2e = []
            for values in tqdm(
                filtered_df.values, desc="Inner loop", position=1, leave=False
            ):
                data = CevaCO2e(*values, df=df_unlocode).response()
                list_of_co2e.append(data)

            df2 = filtered_df.copy()
            df2[CO2E_COL] = list_of_co2e
            df2 = df2.loc[:, CO2E_COL]

            # Get location of column in Dataframe
            column_index = df.columns.get_loc(CO2E_COL)

            # Update DataFrame with values
            df.update(df2)

            # Sheet name from main loop
            ws = wb.sheets[sheet]

            # Insert values from Dataframe into excel file again
            ws.range((2, column_index + 1)).options(
                pd.Series,
                index=False,
                header=False).value = df[CO2E_COL].copy()

        wb.save()
        wb.close()


def read_and_return_dfs(file: str) -> dict:
    return pd.read_excel(file, sheet_name=None)


def filter_df(df: pd.DataFrame, column=str, **kwargs) -> pd.DataFrame:

    df_filtered = df.loc[df[column].isna()].fillna(0)
    columns = list(kwargs.values())
    return df_filtered.loc[:, columns]


def get_unlocode_data(csv_file: str) -> pd.DataFrame:
    return pd.read_csv(csv_file, delimiter=";")


if __name__ == "__main__":
    main()
