import requests


def health_check(site_url):
    try:
        url = "https://" + site_url if not site_url.startswith("http") else site_url
        response = requests.get(url, timeout=5)

        if response.status_code == 404:
            url = "http://" + site_url if not site_url.startswith("http") else site_url
            response = requests.get(url, timeout=5)

        return response.status_code
    except requests.RequestException as e:
        return "ERROR"
