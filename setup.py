from download import download_link_by_url
from unzip_and_load_db import load_tables_to_sqlite, unzip_files

if __name__ == '__main__':

    # Download files
    file_urls = ["https://download.hcad.org/data/CAMA/2024/Real_acct_owner.zip",
                 "https://download.hcad.org/data/CAMA/2024/Real_building_land.zip",
                 "https://download.hcad.org/data/CAMA/2024/Code_description_real.zip"]

    # Download all three zips
    ajax_site_url = "https://hcad.org/pdata/pdata-property-downloads.html"  # Replace with the target website's URL
    download_link_by_url(ajax_site_url, file_urls, 'Zips', 90)

    # Unzip files
    print("Extracting data...")
    data_files = ['real_neighborhood_code.txt', 'building_res.txt', "real_acct.txt", 'land.txt', 'fixtures.txt',
                  'extra_features.txt', 'exterior.txt']

    # Extract files
    unzip_files(src="Zips", dest='Data', file_list=data_files)

    # Load data into sqlite database
    load_tables_to_sqlite(data_files)

    print("Done!")