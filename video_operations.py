from bs4 import BeautifulSoup

import download_html_files

ROOT_URL = "https://en.pokerpro.cc/"


def update_youtube_embeds(body: BeautifulSoup):
    youtubes = body.find_all("div", attrs={"data-vendor": "youtube"})
    result = []
    for youtube in youtubes:
        youtube_info = {}
        youtube_info["src"] = youtube.get("data-src")
        youtube_info["slug"] = youtube_info["src"].split("/")[-1]
        result.append(youtube_info)
        html = f'<iframe width="100%" height="400" src="https://www.youtube.com/embed/{youtube_info["slug"]}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'
        embed_element = BeautifulSoup(html, 'html.parser')
        youtube.replaceWith(embed_element)
    return result


def get_video_categories(soup: BeautifulSoup):
    result = []
    rows = soup.find_all("div", class_="video-page")
    for row in rows:
        category = {"name": "", "video_urls": []}
        category["name"] = row.find("h2", class_="incontent-title").text
        videos = row.find_all("div", class_="homepage-video-item")
        for video in videos:
            url = download_html_files.ROOT_URL + video.find("a")["href"]
            category["video_urls"].append(url)

        result.append(category)
    return result


def get_all_video_categories():
    all_urls = download_html_files.get_urls_from_sitemap()
    return [url for url in all_urls if
            (("/videos/" in url) and ("/videos/video/") not in url and 'https://en.pokerpro.cc/videos/' != url)]


def get_all_video_links_from_video_category_page(url):
    soup = download_html_files.read_soup(url)
    general_tag = soup.find("title").text.split("|")[0].strip()
    parts = soup.find_all("div", class_="video-page")
    result = []
    for part in parts:
        tag = {"tags": [part.find("h2").text, general_tag], "videos": []}
        videos = part.find_all("div", class_="homepage-video-item")
        for video in videos:
            tag["videos"].append(video.find("a")["href"])
        result.append(tag)
    return result


def download_video_tag(tag_info, stop_on_error=True):
    i = 60
    for video in tag_info["videos"]:
        if i > 0:
            i -= 1
        download_html_files.download_page(download_html_files.ROOT_URL + video, stop_on_error=stop_on_error,
                                          args={"video": True, "tags": tag_info["tags"],
                                                "date": f"2023-01-01 23:{i if i > 10 else '0' + str(i)}"})


def get_video_tag(soup: BeautifulSoup) -> str:
    tag = soup.find("div", class_="video-information").find("div").find_all("div")[1].text.strip()
    print(tag)
    return tag


def download_video_category(url="", stop_on_error=True):
    video_tags = get_all_video_links_from_video_category_page(url)
    for tag_info in video_tags:
        download_video_tag(tag_info, stop_on_error)


def download_all_videos(stop_on_error=True, limit=None):
    video_category_pages = get_all_video_categories()
    if limit:
        video_category_pages = video_category_pages[0:limit]
    for category_page in video_category_pages:
        download_video_category(category_page, stop_on_error)

