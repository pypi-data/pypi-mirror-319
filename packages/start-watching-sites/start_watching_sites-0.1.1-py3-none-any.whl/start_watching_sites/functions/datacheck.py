from tabulate import tabulate
from requests import Session
from start_watching_sites.database.models.models import Site, Base
from start_watching_sites.database.database import Session, engine


def view_sites_from_db():
    with Session() as session:
        site_data = session.query(Site).all()
        table_data = [(site.id, site.url, site.status, site.created_at, site.updated_at) for site in site_data]
        headers = ["id", "url", "status", "created_at", "updated_at"]
        table = tabulate(table_data, headers=headers, tablefmt="grid")
        print(table)
        session.close()


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database reset successfully.")
