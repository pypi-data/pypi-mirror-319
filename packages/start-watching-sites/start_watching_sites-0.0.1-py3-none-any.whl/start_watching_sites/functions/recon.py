import os

from tqdm import tqdm
import pandas as pd
from start_watching_sites.database.models.site import Site
from start_watching_sites.functions.sitecheck import health_check
from start_watching_sites.database.database import Session


def recon_site_and_save_to_db(source=None):
    try:
        if source is None:
            xlsx_files = [f for f in os.listdir(".") if f.endswith(".xlsx")]
            if not xlsx_files:
                print("No .xlsx file found in the current folder.")
                return
            source = xlsx_files[0]

        excel_data = pd.ExcelFile(source)
        sheet_name = excel_data.sheet_names[0]
        parsed_data = excel_data.parse(sheet_name)

        with Session() as session:
            for _, row in tqdm(parsed_data.iterrows(), total=parsed_data.shape[0], desc="Processing sites"):
                try:
                    existing_site = session.query(Site).filter_by(url=row["url"]).first()

                    if existing_site:
                        existing_site.status = health_check(row["url"])
                    else:
                        new_site = Site(url=row["url"])
                        session.add(new_site)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    print(f"ERROR: Failed to process {row['url']}: {e}")

    except Exception as e:
        print(f"Error processing Excel file: {e}")
