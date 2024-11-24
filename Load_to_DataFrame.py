import sqlite3

import pandas as pd


def load_data_frame():
    con = sqlite3.connect("HouseProtestValues.db")
    sql_query = """
    SELECT br.acct,
       br.bld_num,
       br.date_erected,
       br.im_sq_ft,
       ra.land_ar,
       br.perimeter,
       br.dpr_val,
       f.bedrooms,
       f.full_bath,
       f.half_bath,
       f.total_rooms,
       case when dscr = 'Good' then 1 else 0 end      as dscr_good,
       case when dscr = 'Average' then 1 else 0 end   as dscr_average,
       case when dscr = 'Low' then 1 else 0 end       as dscr_low,
       case when dscr = 'Very Low' then 1 else 0 end  as dscr_very_low,
       case when dscr = 'Excellent' then 1 else 0 end as dscr_excellent,
       case when dscr = 'Superior' then 1 else 0 end  as dscr_superior,
       case when dscr = 'Poor' then 1 else 0 end      as dscr_poor,
       IFNULL(ex1.frame_detached_garage, 0) AS frame_detached_garage,
       IFNULL(ex1.gunite_pool, 0) AS gunite_pool,
       IFNULL(ex1.solar_panel, 0) AS solar_panel,
       IFNULL(ex1.pool_heater, 0) AS pool_heater,
       IFNULL(ex1.brick_garage, 0) AS brick_garage,
       IFNULL(ex1.canopy_residential, 0) AS canopy_residential,
       IFNULL(ex1.frame_abov, 0) AS frame_abov,
       IFNULL(ex1.frame_shed, 0) AS frame_shed,
       IFNULL(ex1.carport_residential, 0) AS carport_residential,
       IFNULL(ex1.foundation_repaired, 0) AS foundation_repaired,
       IFNULL(ex1.cracked_slab, 0) AS cracked_slab,
       p.lat,
       p.long,
       ra.land_val,
       ra.bld_val,
       ra.assessed_val,
       ra.tot_appr_val,
       ra.tot_mkt_val
FROM building_res br
         LEFT JOIN real_acct ra ON br.acct = ra.acct
         LEFT JOIN (select acct,
                           IFNULL(sum(units) filter (where type = 'RMB'), 0) as "bedrooms",
                           IFNULL(sum(units) filter (where type = 'RMF'), 0) as "full_bath",
                           IFNULL(sum(units) filter (where type = 'RMH'), 0) as "half_bath",
                           IFNULL(sum(units) filter (where type = 'RMT'), 0) as "total_rooms"
                    from fixtures
                    group by acct) f ON br.acct = f.acct
         LEFT JOIN (select acct,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RRG1'), 0) as frame_detached_garage,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RRP5'), 0) as gunite_pool,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RSP1'), 0) as solar_panel,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RRP9'), 0) as pool_heater,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RRG2'), 0) as brick_garage,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RRC2'), 0) as canopy_residential,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RRG3'), 0) as frame_abov,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RRS1'), 0) as frame_shed,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RRC1'), 0) as carport_residential,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RCS9'), 0) as foundation_repaired,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RCS1'), 0) as cracked_slab
                    from extra_features_detail1
                    group by acct) ex1 on br.acct = ex1.acct
         LEFT JOIN parcels p on br.acct = p.HCAD_NUM
WHERE br.impr_tp = 1001
  AND br.property_use_cd = 'A1'
  AND br.date_erected > 1900
  AND ra.assessed_val > 0;"""

    df = pd.read_sql_query(sql_query, con)
    df["assessed_per_sqft"] = df["assessed_val"] / df["im_sq_ft"]
    df.dropna(inplace=True)
    return df


# def load_fixture_data():
#     con = sqlite3.connect('HouseProtestValues.db')
#     # Story Height Index: STY
#     # Room: Bedroom: RMB
#     # Room: Full Bath: RMF
#     # Room: Half Bath: RMH
#     # Room: Total: RMT
#     fixtures_sql = """SELECT *
#                       FROM "fixtures"
#                       WHERE type IN ('STY', 'RMB','RMF','RMH','RMT')
#                     """
#     fixtures = pd.read_sql_query(fixtures_sql, con)
#
#     # Pivot table
#     fix_pt = fixtures.pivot_table(index=['acct', 'bld_num'], columns='type', values='units', aggfunc='sum')
#     fix_pt = fix_pt.reset_index()
#     fix_pt.fillna(0, inplace=True)
#
#     return fix_pt
#
#
# def merge_dataframes(base_df, fix_pt):
#     data_df = pd.merge(base_df, fix_pt, on=['acct', 'bld_num'], how='left')
#     data_df.dropna(inplace=True)
#     data_df.reset_index(drop=True, inplace=True)
#
#     return data_df


# def load_all():
#     df_1 = load_building_data()
#     df_2 = load_fixture_data()
#     df_3 = merge_dataframes(df_1, df_2)
#     return df_3


if __name__ == "__main__":
    # build_df = load_building_data()
    # fix_df = load_fixture_data()
    # df = merge_dataframes(build_df, fix_df)

    load_data_frame()
