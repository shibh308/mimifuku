from credentials import scrapbox_cookies
import requests
import urllib

DOMAIN_URL = "https://scrapbox.io"

PAGE_MAX=10000

def get_page_list(project_name: str):
    project_url = f'{DOMAIN_URL}/api/pages/{project_name}?limit={PAGE_MAX}'
    response = requests.get(project_url, cookies=scrapbox_cookies)
    if not response.ok:
        print(f"Failed to get page list from {project_url}")
        return []
    resp = response.json()
    return [page['title'] for page in resp['pages']]

def get_page_content(project_name: str, page_name: str):
    page_url = f'{DOMAIN_URL}/api/pages/{project_name}/{urllib.parse.quote(page_name)}'
    response = requests.get(page_url, cookies=scrapbox_cookies)
    if not response.ok:
        print(f"Failed to get page content from {page_url}")
        return ""
    resp = response.json()
    return [line['text'] for line in resp['lines']]

if __name__ == '__main__':
    l = get_page_list("checkedpapers")
    print(l)
    p = get_page_content("checkedpapers", "Template")
    print(p)