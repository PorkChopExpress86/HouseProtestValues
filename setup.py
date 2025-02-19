import os
import json
from pyhcad import (unzip_files,
                    unzip_parcel_data, 
                    extract_parcel_data,
                    create_tables, 
                    import_data, 
                    import_parcels,
                    download_link_by_url,
                    compute_hashes_recursive)

HASH_FILE = "hashes.txt"

def load_hashes():
    """
    Load the previously stored file hashes from HASH_FILE.
    """
    if os.path.exists(HASH_FILE):
        try:
            with open(HASH_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading hashes: {e}")
            return {}
    return {}

def save_hashes(hashes):
    """
    Save the current file hashes to HASH_FILE.
    """
    try:
        with open(HASH_FILE, "w") as f:
            json.dump(hashes, f, indent=4)
    except Exception as e:
        print(f"Error saving hashes: {e}")
if __name__ == "__main__":
    # Download files
    file_urls = [
        "https://download.hcad.org/data/CAMA/2024/Real_acct_owner.zip",
        "https://download.hcad.org/data/CAMA/2024/Real_building_land.zip",
        "https://download.hcad.org/data/CAMA/2024/Code_description_real.zip",
    ]

    # Tax data information
    # Replace with the target website's URL
    ajax_site_url = "https://hcad.org/pdata/pdata-property-downloads.html"
    download_link_by_url(ajax_site_url, file_urls, "Zips", 90)

    # Download GIS data on tax particles
    file_urls = ["https://download.hcad.org/data/GIS/Parcels.zip"]
    ajax_site_url = "https://hcad.org/pdata/pdata-gis-downloads.html"
    download_link_by_url(ajax_site_url, file_urls, "Zips", 90)

    # Step 2: Compute hashes for all files in the "Zips" directory
    current_hashes = compute_hashes_recursive("Zips")
    stored_hashes = load_hashes()

   # Check if any file has changed
    if current_hashes == stored_hashes:
        print("No changes detected in data files. Skipping extraction and database update.")
    else:
        print("Changes detected. Processing data...")

        # Step 3: Unzip files and process data
        print("Extracting data...")
        data_files = [
            "real_neighborhood_code.txt",
            "building_res.txt",
            "real_acct.txt",
            "land.txt",
            "fixtures.txt",
            "extra_features.txt",
            "exterior.txt",
            "extra_features_detail1.txt",
        ]
        unzip_files(src="Zips", dst="Data", file_list=data_files)
        unzip_parcel_data("Zips", "Data")
        extract_parcel_data("Data/Parcels.shp", "Data/parcels.csv")
        data_files.append("parcels.csv")

        # Step 4: Create database tables and import data
        create_tables()
        import_data("real_acct.txt", "real_acct")
        import_data("building_res.txt", "building_res")
        import_data("fixtures.txt", "fixtures")
        import_data("extra_features_detail1.txt", "extra_features_detail1")
        import_parcels()

        print("Done! Ready to run House Values Notebook")

        # Step 5: Update stored hashes with the current state
        save_hashes(current_hashes)
