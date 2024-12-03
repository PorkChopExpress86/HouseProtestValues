import sqlite3

import pandas as pd
import numpy as np
import os
from zipfile import ZipFile as zf

import chardet
import pandas as pd


def load_housing_data():
    if does_file_exist("HouseProtestValues.db"):
        df = load_housing_data_from_sqlite()
    else:
        os.makedirs("Data", exist_ok=True)
        if does_file_exist("Data/complete_sample_data.csv") == False:
            with zf("housing_data.zip", "r") as zFile:
                zFile.extractall("Data")
        df = pd.read_csv("Data/complete_sample_data.csv", low_memory=False)
    return df


def load_mailing_data():
    if does_file_exist("HouseProtestValues.db"):
        df = load_mail_data_from_sqlite()
    else:
        os.makedirs("Data", exist_ok=True)
        if does_file_exist("Data/mailing_data.csv") == False:
            with zf("mailing_data.zip", "r") as zFile:
                zFile.extractall("Data")
        df = pd.read_csv("Data/mailing_data.csv")
    return df


def does_file_exist(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False


def load_mail_data_from_sqlite():
    con = sqlite3.connect("HouseProtestValues.db")
    sql_address = """SELECT acct,
                            mailto,
                            mail_addr_1,
                            mail_addr_2,
                            Mail_city,
                            mail_state,
                            mail_zip
                    FROM real_acct;"""
    df = pd.read_sql_query(sql_address, con)
    return df


def load_housing_data_from_sqlite():
    con = sqlite3.connect("HouseProtestValues.db")
    sql_query = """
SELECT br.acct,
       br.bld_num,
       br.date_erected,
       br.im_sq_ft,
       ra.land_ar,
       br.perimeter,
       f.bedrooms,
       f.full_bath,
       f.half_bath,
       f.total_rooms,
       CASE
           WHEN br.dscr = 'Poor' THEN 0
           WHEN br.dscr = 'Very low' THEN 1
           WHEN br.dscr = 'Low' THEN 2
           WHEN br.dscr = 'Average' THEN 3
           WHEN br.dscr = 'Good' THEN 4
           WHEN br.dscr = 'Excellent' THEN 5
           WHEN br.dscr = 'Superior' THEN 6
           END                              AS dscr_e,
       IFNULL(ex1.frame_detached_garage, 0) AS frame_detached_garage,
       IFNULL(ex1.gunite_pool, 0)           AS gunite_pool,
       IFNULL(ex1.solar_panel, 0)           AS solar_panel,
       IFNULL(ex1.pool_heater, 0)           AS pool_heater,
       IFNULL(ex1.brick_garage, 0)          AS brick_garage,
       IFNULL(ex1.canopy_residential, 0)    AS canopy_residential,
       IFNULL(ex1.frame_abov, 0)            AS frame_abov,
       IFNULL(ex1.frame_shed, 0)            AS frame_shed,
       IFNULL(ex1.carport_residential, 0)   AS carport_residential,
       IFNULL(ex1.foundation_repaired, 0)   AS foundation_repaired,
       IFNULL(ex1.cracked_slab, 0)          AS cracked_slab,
       p.latitude,
       p.longitude,
       ra.land_val,
       ra.bld_val,
       br.dpr_val,
       ra.assessed_val,
       ra.mailto,
       ra.mail_addr_1,
       ra.mail_addr_2,
       ra.Mail_city,
       ra.mail_state,
       ra.mail_zip
FROM building_res br
         LEFT JOIN real_acct ra ON br.acct = ra.acct
         LEFT JOIN (select acct,
                           IFNULL(sum(units) filter (where type = 'RMB'), 0) AS "bedrooms",
                           IFNULL(sum(units) filter (where type = 'RMF'), 0) AS "full_bath",
                           IFNULL(sum(units) filter (where type = 'RMH'), 0) AS "half_bath",
                           IFNULL(sum(units) filter (where type = 'RMT'), 0) AS "total_rooms"
                    FROM fixtures
                    GROUP BY acct) f ON br.acct = f.acct
         LEFT JOIN (SELECT acct,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RRG1'), 0) AS frame_detached_garage,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RRP5'), 0) AS gunite_pool,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RSP1'), 0) AS solar_panel,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RRP9'), 0) AS pool_heater,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RRG2'), 0) AS brick_garage,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RRC2'), 0) AS canopy_residential,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RRG3'), 0) AS frame_abov,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RRS1'), 0) AS frame_shed,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RRC1'), 0) AS carport_residential,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RCS9'), 0) AS foundation_repaired,
                           IFNULL(sum(asd_val) FILTER (WHERE cd = 'RCS1'), 0) AS cracked_slab
                    from extra_features_detail1
                    group by acct) ex1 on br.acct = ex1.acct
         LEFT JOIN parcels p on br.acct = p.HCAD_NUM
WHERE br.impr_tp = 1001
  AND br.property_use_cd = 'A1'
  AND br.date_erected > 1900
  AND ra.assessed_val > 0
  AND br.im_sq_ft > 50;"""

    df = pd.read_sql_query(sql_query, con)
    df.dropna(inplace=True)

    return df


if __name__ == "__main__":
    load_data_frame()
