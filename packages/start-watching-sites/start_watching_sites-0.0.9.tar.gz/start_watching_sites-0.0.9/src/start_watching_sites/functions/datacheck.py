from tabulate import tabulate
from requests import Session
from start_watching_sites.database.models.site import Site
from start_watching_sites.database.database import Session


def view_sites_from_db():
    with Session() as session:
        site_data = session.query(Site).all()
        table_data = [(site.id, site.url, site.status, site.created_at, site.updated_at) for site in site_data]
        headers = ["id", "url", "status", "created_at", "updated_at"]
        table = tabulate(table_data, headers=headers, tablefmt="grid")
        print(table)
        session.close()
