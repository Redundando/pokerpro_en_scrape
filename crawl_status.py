import csv
import json
import requests
from glob import glob
from bs4 import BeautifulSoup

from json2xml import json2xml
from json2xml.utils import readfromstring

from logger import log
import create_csv
import download_html_files

NEW_ROOT = "https://pokerprowp.backendarchitects.com"
AUTH = ('pokerproteam','oPo-1e;g=S6S')

CHECKED_IMAGES = {}
CHECKED_LINKS = {}

def get_jsons():
    file_names = create_csv.get_file_names("json_files")
    jsons = create_csv.open_jsons(file_names)
    return jsons


def get_sitemap_urls(sitemap_url="", auth=None):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'}
    response = requests.get(sitemap_url, headers=headers, timeout=5, auth=AUTH)
    soup = BeautifulSoup(response.content, features="xml")
    result = []
    urls = soup.find_all("url")
    for url in urls:
        result.append(url.find_next("loc").text)
    return result


def get_request_header(url=""):
    print("Checking "+url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=5, auth=AUTH, stream=True)
        header = response.headers
        header["status_code"] = response.status_code
        response.close()
        return header
    except Exception as e:
        return {"status_code": 400, "details": str(e)}



def get_absolute_url(src="")-> str:
    if src[0:4]=="http":
        return src
    return NEW_ROOT + src


def check_image(url)->{}:
    if url in CHECKED_IMAGES.keys():
        return CHECKED_IMAGES[url]
    raw_image_info = get_request_header(url)
    image_info = {
        "url": url,
        "status_code": raw_image_info["status_code"],
        "size": int(raw_image_info["Content-Length"]) if "Content-Length" in raw_image_info.keys() else -1
    }
    CHECKED_IMAGES[url] = image_info
    return image_info

def check_images(soup)->[]:
    result = []
    images = soup.find_all("img")
    for image in images:
        src = image["src"] if "src" in image.attrs else None
        if src:
            src = get_absolute_url(src)
            result.append(check_image(src))
    return result

def check_link(url)->{}:
    if url in CHECKED_LINKS.keys():
        return CHECKED_LINKS[url]
    raw_link_info = get_request_header(url)
    link_info = {
        "url": url,
        "status_code": raw_link_info["status_code"],
        "details": raw_link_info["details"] if "details" in raw_link_info.keys() else ""
    }
    CHECKED_LINKS[url] = link_info
    return link_info


def check_links(soup)->[]:
    result = []
    links = soup.find_all("a")
    for link in links:
        href = link["href"] if "href" in link.attrs else None
        if href:
            href = get_absolute_url(href)
            result.append(check_link(href))
    return result


@log
def check_url(url):
    result = {"article_url": url}
    soup = download_html_files.read_soup(url=url, auth=AUTH)
    result["links"] = check_links(soup)
    result["images"] = check_images(soup)
    download_html_files.save_page_json(result,sub_directory="checks")


def get_all_links_from_jsons():
    file_names = create_csv.get_file_names("json_files")
    jsons = create_csv.open_jsons(file_names)
    result = []
    for json in jsons:
        if "links" in json:
            for link in json["links"]:
                link["from_url"] = json["article_url"]
                result.append(link)
    return result

def filter_internal_links(links):
    result = []
    seen_urls = []
    for link in links:
        if "absolute_url" in link and link["absolute_url"] not in seen_urls and download_html_files.ROOT_URL in link["absolute_url"]:
            seen_urls.append(link["absolute_url"])
            result.append(link)
    return result

if __name__ == "__main__":
    urls = get_sitemap_urls(sitemap_url="https://pokerprowp.backendarchitects.com/sitemap.xml", auth=AUTH)
    #check_url("https://pokerprowp.backendarchitects.com/promotions/biggest-ever-bounty-hunter-series-on-ipoker-with-4m-gtd-241/")
    #print(get_request_header("https://www.example.com/no-there"))

    links = get_all_links_from_jsons()
    internal_links = filter_internal_links(links)
    i = [i["href"] for i in internal_links]
    print(i)