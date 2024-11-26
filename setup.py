from download import download_link_by_url
from unzip_and_load_db import load_tables_to_sqlite, unzip_files
from extract_and_load_parcel_data import unzip_parcel_data, extract_parcel_data

if __name__ == "__main__":
    # Download files
    file_urls = ["https://download.hcad.org/data/CAMA/2024/Real_acct_owner.zip",
        "https://download.hcad.org/data/CAMA/2024/Real_building_land.zip",
        "https://download.hcad.org/data/CAMA/2024/Code_description_real.zip", ]

    # Tax data information
    ajax_site_url = "https://hcad.org/pdata/pdata-property-downloads.html"  # Replace with the target website's URL
    download_link_by_url(ajax_site_url, file_urls, "Zips", 90)

    # Download GIS data on tax particles
    file_urls = ["https://download.hcad.org/data/GIS/Parcels.zip"]
    ajax_site_url = "https://hcad.org/pdata/pdata-gis-downloads.html"
    download_link_by_url(ajax_site_url, file_urls, "Zips", 90)

    # Unzip files
    print("Extracting data...")
    data_files = ["real_neighborhood_code.txt", "building_res.txt", "real_acct.txt", "land.txt", "fixtures.txt",
        "extra_features.txt", "exterior.txt", "extra_features_detail1.txt", ]

    # Extract files
    unzip_files(src="Zips", dst="Data", file_list=data_files)

    # Unzip parcel data
    unzip_parcel_data('Zips', 'Data')

    # Add latitude and longitude coordinates in decimal degrees and export file
    extract_parcel_data('Data/HCAD_PDATA/Parcels/Parcels.shp', 'Data/parcels.csv')

    # Add parcels.csv
    data_files.append("parcels.csv")

    # Load tables into sqlite data
    load_tables_to_sqlite(data_files)

    # Extract files
    unzip_files(src="Zips", dst="Data", file_list=data_files)

    # Load data into sqlite database
    load_tables_to_sqlite(data_files)

    print("Done! Ready to run House Values Notebook")
