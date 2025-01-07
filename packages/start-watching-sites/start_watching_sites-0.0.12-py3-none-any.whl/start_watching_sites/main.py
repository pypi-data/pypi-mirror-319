import argparse
from start_watching_sites.functions.datacheck import reset_database, view_sites_from_db
from start_watching_sites.functions.recon import export_result_to_excel, recon_site_and_save_to_db
from start_watching_sites.database.models.models import Base
from start_watching_sites.database.database import engine

Base.metadata.create_all(engine)


def main():
    parser = argparse.ArgumentParser(description="Reconsites sites from an Excel file and saves the results to a SQLite database.")
    parser.add_argument("-t", "--task", type=str, default="start", help="[start, view, export, reset]")
    parser.add_argument("-s", "--source", type=str, help="Excel file")
    args = parser.parse_args()

    if args.task == "start":
        recon_site_and_save_to_db(args.source)
    elif args.task == "view":
        view_sites_from_db()
    elif args.task == "export":
        export_result_to_excel()
    elif args.task == "reset":
        reset_database()
    else:
        print("ERROR: Invalid task")


if __name__ == "__main__":
    main()
