import argparse
from database.models.site import Base
from functions.datacheck import view_sites_from_db
from database.database import engine
from functions.recon import recon_site_and_save_to_db

Base.metadata.create_all(engine)


def main():
    parser = argparse.ArgumentParser(description="Reconsites sites from an Excel file and saves the results to a SQLite database.")
    parser.add_argument("-t", "--task", type=str, default="update", help="[update, view, notify, reset]")
    parser.add_argument("-s", "--source", type=str, help="Excel file")
    args = parser.parse_args()

    if args.task == "update":
        recon_site_and_save_to_db(args.source)
    elif args.task == "view":
        view_sites_from_db()
    elif args.task == "reset":
        print("test")
    else:
        print("ERROR: Invalid task")


if __name__ == "__main__":
    main()
