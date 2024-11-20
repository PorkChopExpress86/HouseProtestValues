import sqlite3

import pandas as pd


def load_building_data():
    con = sqlite3.connect('HouseProtestValues.db')
    sql_query = '''SELECT  br.acct,
                           br.bld_num,
                           br.date_erected,
                           br.im_sq_ft,
                           br.gross_ar,
                           br.base_ar,
                           ra.land_ar,
                           br.perimeter,
                           br.size_index,
                           ra.land_val,
                           ra.bld_val,
                           ra.assessed_val,
                           ra.tot_appr_val,
                           ra.tot_mkt_val
                FROM building_res as br
                LEFT JOIN real_acct as ra ON br.acct = ra.acct
                WHERE br.impr_tp = 1001 AND br.property_use_cd = 'A1' AND br.date_erected > 10;'''

    base_df = pd.read_sql_query(sql_query, con)
    return base_df


def load_fixture_data():
    con = sqlite3.connect('HouseProtestValues.db')
    # Story Height Index: STY
    # Room: Bedroom: RMB
    # Room: Full Bath: RMF
    # Room: Half Bath: RMH
    # Room: Total: RMT
    fixtures_sql = """SELECT *
                      FROM "fixtures"
                      WHERE type IN ('STY', 'RMB','RMF','RMH','RMT')
                    """
    fixtures = pd.read_sql_query(fixtures_sql, con)

    # Pivot table
    fix_pt = fixtures.pivot_table(index=['acct', 'bld_num'], columns='type', values='units', aggfunc='sum')
    fix_pt = fix_pt.reset_index()
    fix_pt.fillna(0, inplace=True)

    return fix_pt


def merge_dataframes(base_df, fix_pt):
    data_df = pd.merge(base_df, fix_pt, on=['acct', 'bld_num'], how='left')
    data_df.dropna(inplace=True)
    data_df.reset_index(drop=True, inplace=True)

    return data_df

def load_all():
    df_1 = load_building_data()
    df_2 = load_fixture_data()
    df_3 = merge_dataframes(df_1, df_2)
    return df_3

if __name__ == '__main__':
    build_df = load_building_data()
    fix_df = load_fixture_data()
    df = merge_dataframes(build_df, fix_df)
