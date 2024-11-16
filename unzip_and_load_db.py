"""
This file will be called by a timing function by the os like cron and will download
the data on a schedule.
"""
import os
import sqlite3
from zipfile import ZipFile as zf

import pandas as pd


def unzip_files(src, dest, file_list):
    for root, dirs, files in os.walk(src):
        for name in files:
            file_name = name.split('.')[0]
            file_type = name.split('.')[-1]
            if file_type == 'zip':
                file = str(os.path.join(root, name))

                with zf(file, 'r') as zFile:
                    all_files = zFile.namelist()
                    files_to_unzip = [f for f in all_files if f in file_list]

                    if not files_to_unzip:
                        print(f"No files in {file}")

                    for file in files_to_unzip:
                        print(f"Unzipping {file}")
                        zFile.extract(file, f"{dest}/")


def load_tables_to_sqlite(year_list, file_list):
    conn = sqlite3.connect('HouseProtestValues.db')
    cursor = conn.cursor()
    # year_list = ['2023', '2024']
    # file_list = [['building_res.txt', 'mbcs'], ["real_acct.txt", 'mbcs'], ['land.txt', 'utf-8']]

    for year in year_list:
        for file in file_list:
            try:
                print(f"Reading {file}, try 1")
                df = pd.read_csv(f"Data/{year}/{file}", sep='\t', encoding='utf-8', low_memory=False)
            except:
                try:
                    print(f"Reading {file}, try 2")
                    df = pd.read_csv(f"Data/{year}/{file}", sep='\t', encoding='mbcs', low_memory=False)
                except:
                    print(f"File did not complete load:{year} {file}")

            table_name = table_name_gen(year, file)
            if df is not None:
                print(f"Writing {file} to sqlite db")
                df.to_sql(table_name, conn, if_exists='replace', index=True)

    conn.commit()
    conn.close()


def table_name_gen(year, file):
    file_name = file.split('.')[0]
    return year + "_" + file_name


if __name__ == "__main__":
    print("Extracting data...")
    year_list = ['2023', '2024']
    file_list = ['building_res.txt', "real_acct.txt", 'land.txt']
    # Extract files
    for i in year_list:
        unzip_files(f"{i}", f"Data/{i}", file_list)

    load_tables_to_sqlite(year_list, file_list)
