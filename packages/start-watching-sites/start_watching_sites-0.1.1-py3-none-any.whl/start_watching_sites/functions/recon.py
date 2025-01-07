import os

from tqdm import tqdm
import pandas as pd
from start_watching_sites.database.models.models import Site
from start_watching_sites.database.database import Session
from start_watching_sites.functions.exceltools import create_excel, get_excel_source, parse_excel_data
from start_watching_sites.functions.sitecheck import health_check


def process_site_data(session, row):
    try:
        existing_site = session.query(Site).filter_by(url=row["url"]).first()

        if existing_site:
            existing_site.status = health_check(row["url"])
        else:
            new_site = Site(url=row["url"], status=health_check(row["url"]))
            session.add(new_site)

        session.commit()
    except Exception as e:
        session.rollback()
        raise RuntimeError(f"Failed to process {row['url']}: {e}")


def recon_site_and_save_to_db(source=None):
    try:
        source = get_excel_source(source)
        parsed_data = parse_excel_data(source)

        with Session() as session:
            for _, row in tqdm(parsed_data.iterrows(), total=parsed_data.shape[0], desc="Processing sites"):
                try:
                    process_site_data(session, row)
                except Exception as e:
                    print(f"ERROR: {e}")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"Unexpected error: {e}")


def export_result_to_excel():
    with Session() as session:
        site_data = session.query(Site).all()
        create_excel(site_data)
        session.close()
