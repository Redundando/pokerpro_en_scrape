from bs4 import BeautifulSoup

ROOT_URL = "https://en.pokerpro.cc/"


def fix_play_now_link(href="")->str:
    if "play-now/" in href:
        return href[:href.rfind("-")]
    return href


def get_link_information(link):
    if "href" not in link.attrs: return link.attrs.copy()
    href = link["href"]
    result = link.attrs.copy()
    result["original_link"] = href
    if ("http:" not in href) and ("https:" not in href):
        if href[0]=="/":
            href=href[1:]
        absolute_url = ROOT_URL + href
        result["absolute_url"] = absolute_url
        if href[0] != "#" and href[0] != "/":
            href = "/" + href
    result["href"] = href.replace(".html", "")
    result["href"] = fix_play_now_link(result["href"])
    return result



def get_content_links(body=BeautifulSoup()):
    links = body.find_all("a")
    result = []
    for a in links:
        if "href" not in a.attrs or "/tags" in a["href"]:
            continue
        result.append(get_link_information(a))
    return result


def update_page_links(body: BeautifulSoup):
    result = []
    links = body.find_all("a")
    for a in links:
        link_info = get_link_information(a)
        a["href"] = link_info["href"] if "href" in link_info else "#"
        result.append(link_info)
    return result


def update_page_tags(body: BeautifulSoup):
    tags = [tag for tag in body.find_all("a") if "/tags/" in tag["href"]]
    result = []
    for tag in tags:
        tag_info = get_link_information(tag)
        tag_identifier = tag_info["href"].split("/")[-1]
        tag_identifier_without_trailing_number = tag_identifier[0:tag_identifier.rfind("-")]
        tag_info["href"] = "/tag/"+tag_identifier_without_trailing_number+"/"
        tag_info["absolute_url"] = ROOT_URL + tag_info["href"][1:]
        result.append(tag_info)

    return result
