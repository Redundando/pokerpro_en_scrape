import csv
import json
import os.path
import urllib.request
from glob import glob

import requests
import unicodedata
from bs4 import BeautifulSoup

import image_operations
import link_operations
import logos
import ratings
import bonus
import pokerpro_box_operations
import review_operations
import twitter_operations
import video_operations
from logger import log

ROOT_URL = "https://en.pokerpro.cc/"


def clean_string(string):
    result = "".join(char for char in string if unicodedata.category(char)[0] != "C")
    result = result.replace(" ", " ")
    return result


@log
def read_urls(csv_file="indexed_urls.csv"):
    with open("indexed_urls.csv", newline='', encoding="utf8") as file:
        data = list(csv.reader(file))
        data.pop(0)
        urls = [d[0] for d in data]
    return urls


@log
def read_soup(url="", auth=None):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'}
    response = requests.get(url, headers=headers, timeout=5, auth=auth)
    soup = BeautifulSoup(response.content, "html.parser")
    response.close()
    return soup


def filename_from_url(url=""):
    name = url[url.find("//") + 2::].replace("/", "_") + ".json"
    return name


@log
def get_page_information(url="", download_images = True, args=None):
    soup = read_soup(url=url)
    if type(soup) == int:
        return {"url": url, "status": soup}
    ld_json_data = get_ld_json_data(soup)
    html_body = get_article_html(soup)
    body = BeautifulSoup(html_body, "html.parser")
    data = {"article_url": url,
            "title": get_title(soup),
            "slug": get_slug(url),
            "category": get_category(url),
            "description": get_description(soup),
            "thumbnail": get_thumbnail(soup),
            "meta_title": get_meta_title(soup),
            "author": ld_json_data["author"] if ld_json_data else "PokerPro",
            "page_type": ld_json_data["@type"] if ld_json_data else "other",
            "date_published": ld_json_data["datePublished"] if ld_json_data else "2023-01-01",
            "date_modified": ld_json_data["dateModified"] if ld_json_data else "2023-01-01",
            "html_content": html_body,
            "tags": get_tags(soup)}
    if download_images:
        data["images"] = image_operations.update_page_images(body, default_alt=data["title"])
    data["links"] = link_operations.update_page_links(body)
    data["youtube_embeds"] = video_operations.update_youtube_embeds(body)
    data["twitter_embeds"] = twitter_operations.update_twitter_embeds(body)
    data["tag_links"] = link_operations.update_page_tags(body)
    data["contact_us_boxes"] = pokerpro_box_operations.update_contact_us_box(body)
    if (("/play-now/" in data["article_url"] and data["article_url"][-9:] != "play-now/")):
        data["short_title"] = review_operations.get_short_title(data["title"])
        data["logo"] = review_operations.get_logo(soup)
        data["promo_description"] = review_operations.get_bonus(soup)
        data["short_promo_line"] = bonus.get_proper_bonus(operator=data["short_title"])
        data["external_URL"] = review_operations.get_external_link(soup)
        data["TC"] = "New Customers Only | 18+ | T&C Apply"
        data["license"] = review_operations.get_license(soup)
        data["restricted_countries"] = review_operations.get_restricted_countries(soup)
        data["company_name"] = review_operations.get_company_name(soup)
        data["thumbnail"] = get_thumbnail(soup, operator=data["short_title"])
        data["rating"] = ratings.get_proper_rating(operator=data["short_title"])
        data["detailed_rating"] = ratings.get_four_ratings(data["rating"])
        pass

    if args and args["video"]:
        tags = args["tags"]
        page_tag = video_operations.get_video_tag(soup)
        tags.append(page_tag)
        data["tags"] = ",".join(list(set(tags)))
        data["date_published"] = args["date"]
        data["date_modified"] = args["date"]

    data["html_content"] = str(body)

    return data



def save_page_json(page_json={}, sub_directory=""):
    filename = filename_from_url(url=page_json["article_url"])
    directory = "json_files/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    if sub_directory != "":
        directory = "json_files/" + sub_directory + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
    with open(directory + filename, 'w', encoding='utf-8') as file:
        json.dump(page_json, file, ensure_ascii=False, indent=4)


def get_title(soup):
    og_title = soup.find("meta", property="og:title")
    if og_title:
        return og_title["content"]
    return soup.find("title").text


def get_description(soup):
    og_desc = soup.find("meta", property="og:description")
    if og_desc:
        return clean_string(og_desc["content"])
    meta_desc = soup.find("meta", {"name": "description"})
    if meta_desc:
        return clean_string(meta_desc["content"])
    return None


def get_thumbnail(soup=BeautifulSoup(), operator=""):
    og_image = soup.find("meta", property="og:image")
    src = None
    if og_image:
        src = og_image["content"]
    header_offer_logo = None
    if soup.find("div", class_="header-offer-logo"):
        header_offer_logo = soup.find("div", class_="header-offer-logo").find("img")
    if header_offer_logo:
        src = header_offer_logo["src"]
        proper_logo = logos.get_proper_logo(operator)
        if proper_logo != "":
            src = proper_logo
    if src:
        """
        image = BeautifulSoup("","html.parser").new_tag("img")
        image["src"] = src
        image_info = image_operations.get_image_information(image)
        image_info["filename"] = image_operations.download_image(image_info["image_url"])
        image["src"] = ROOT_URL + "wp-content/uploads/" + image_info["filename"]
        return image_info["image_url"]
        """
        return src
    return None


def get_meta_title(soup=BeautifulSoup()):
    return soup.find("title").text


def get_ld_json_data(soup=BeautifulSoup()):
    data = [json.loads(x.string) for x in soup.find_all("script", type="application/ld+json")]
    return data[0] if data else None


def get_review_html(soup=BeautifulSoup()):
    review_text = soup.find(class_="tab-c-wrap")
    promotions_tab = soup.find(class_="offer--signup")
    if review_text:
        side_boxes = soup.find_all(class_="side-box")
        body = get_inner_soup(review_text)
        return review_operations.create_review(body=body, side_boxes=side_boxes, promotions_tab=promotions_tab)




def get_video_html(soup=BeautifulSoup()):
    video = soup.find(class_="lazyframe")
    video_desc = get_inner_soup(soup.find(class_="video-desc"))
    result = BeautifulSoup(str(video)+str(video_desc),"html.parser")
    share_box = result.find("div", class_="shareContent--Wrap")
    if share_box:
        share_box.decompose()
    video_information = result.find("div", class_="video-information")
    if video_information:
        video_information.decompose()
    return result


def get_inner_soup(soup=BeautifulSoup):
    r_html = ""
    for tag in soup.children:
        r_html += str(tag)
    return BeautifulSoup(r_html, "html.parser")


def get_article_html(soup=BeautifulSoup()):
    pokerpro_box_operations.update_social_box(soup)
    news_content = soup.find(class_="news-single-content")
    result = BeautifulSoup("", "html.parser")
    if news_content:
        result = get_inner_soup(news_content)
    elif soup.find(class_="tab-c-wrap"):
        result = get_review_html(soup=soup)
    elif soup.find(class_="video-information"):
        result = get_video_html(soup=soup)
    elif soup.find(class_="leaderboard-item-wrap"):
        result = get_inner_soup(soup.find(class_="leaderboard-item-wrap"))
    return str(result)


def get_tags(soup=BeautifulSoup):
    tags_section = soup.find("div", class_="news-tags")
    result = []
    if tags_section:
        tags = tags_section.find_all("a")
        result = [t.text for t in tags]
    return ", ".join(result)


def get_slug(url=""):
    return url[url.rfind("/") + 1:999].replace(".html", "")


def get_category(url=""):
    preslug = url[0:url.find(get_slug(url)) - 1]
    return preslug[preslug.rfind("/"):999].replace("/", "")



def download_page(url="", stop_on_error=True, args=None, download_images = True):
    result = {"article_url": url}
    if stop_on_error:
        page = get_page_information(url=url, args=args, download_images = download_images)
        save_page_json(page_json=page)
        return

    try:
        page = get_page_information(url=url, args=args, download_images = download_images)
        save_page_json(page_json=page)
    except Exception as e:
        result["success"] = False
        result["details"] = str(e)
        save_page_json(page_json=result, sub_directory="errors")



def get_urls_from_sitemap(sitemap_url="https://en.pokerpro.cc/sitemap.xml"):
    req = requests.head(sitemap_url, timeout=5)
    if req.status_code != 200:
        return req.status_code
    with urllib.request.urlopen(sitemap_url) as response:
        xml = response.read()
        soup = BeautifulSoup(xml, features="xml")
    result = []
    urls = soup.find_all("url")
    for url in urls:
        result.append(url.find_next("loc").text)
    return result


def get_error_urls():
    error_files = glob(f"json_files/errors/*.json")
    result = []
    for f in error_files:
        with open(f, encoding="utf-8") as file:
            data = json.load(file)
            result.append(data["article_url"])
    return result


def run_all(urls=None, filter="", limit=None, stop_on_error=True, download_images = True):
    if urls is None:
        urls = get_urls_from_sitemap()
    if filter == "casinos":
        urls = [url for url in urls if ("/play-now/" in url and url[-9:] != "play-now/")]
    if filter == "posts":
        urls = [url for url in urls if (
                    "/articles/" in url or "/news/" in url or "/promotions/" in url or "/leaderboards/" in url or "/e-wallets/" in url)]
    if filter == "videos":
        pass
    for url in (urls[0:limit] if limit else urls):
        download_page(url, stop_on_error=stop_on_error, download_images = download_images)


if __name__ == "__main__":
    run_all(urls=get_urls_from_sitemap(), filter="posts", stop_on_error=False)
    #download_page(url="https://en.pokerpro.cc/play-now/betkings.html")
    # download_page(url="https://en.pokerpro.cc/play-now/coral-poker.html")
    # print(get_error_urls())
