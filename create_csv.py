import csv
import json
from glob import glob

from json2xml import json2xml
from json2xml.utils import readfromstring

from logger import log

ignore_urls = ["https://en.pokerpro.cc/news/", "https://en.pokerpro.cc/play-now/", "https://en.pokerpro.cc/news/tags/",
               "https://en.pokerpro.cc/promotions/", "https://en.pokerpro.cc/promotions/tags/",
               "https://en.pokerpro.cc/videos/", "https://en.pokerpro.cc/articles/",
               "https://en.pokerpro.cc/articles/tags/", "https://en.pokerpro.cc/e-wallets/",
               "https://en.pokerpro.cc/leaderboards/", "https://en.pokerpro.cc/contact/",
               "https://en.pokerpro.cc/contact/telegram-2.html", "https://en.pokerpro.cc/contact/skype-4.html",
               "https://en.pokerpro.cc/contact/email-contacts-5.html", "https://en.pokerpro.cc/contact/discord-7.html",
               "https://en.pokerpro.cc/contact/whatsapp-8.html"]


@log
def get_file_names(folder=""):
    return glob(f"{folder}/*.json")


@log
def open_jsons(file_names=[]):
    result = []
    for f in file_names:
        with open(f, encoding="utf-8") as file:
            data = json.load(file)
            if data["article_url"] not in ignore_urls:
                result.append(data)
    return result


@log
def save_json_as_csv(jsons=[]):
    csv_file = open("articles.csv", "w", newline="", encoding="utf-8")
    csv_writer = csv.writer(csv_file)
    count = 0
    for data in jsons:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
    csv_file.close()


@log
def save_combined_jsons(filter="", limit = None):
    file_names = get_file_names("json_files")
    if filter == "casinos":
        file_names = [file_name for file_name in file_names if ("_play-now_" in file_name)]
    if filter == "posts":
        file_names = [file_name for file_name in file_names if (
                    ("_articles_" in file_name) or ("_news_" in file_name) or (
                        "_promotions_" in file_name) or ("_leaderboards_" in file_name) or ("_e-wallets_" in file_name))]
    if filter == "videos":
        file_names = [file_name for file_name in file_names if ("_videos_video_" in file_name)]
    jsons = open_jsons(file_names)
    if limit:
        jsons = jsons[0:limit]
    filename = "articles" + ("-" + filter if filter != "" else "") + ".json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(jsons, file, indent=4)


@log
def save_all_jsons_as_csv():
    file_names = get_file_names("json_files")
    jsons = open_jsons(file_names)
    save_json_as_csv(jsons)


@log
def save_all_jsons_as_xml():
    file_names = get_file_names("json_files")
    jsons = open_jsons(file_names)
    data = readfromstring(jsons)
    print(json2xml.Json2xml(data).to_xml())


if __name__ == "__main__":
    save_combined_jsons(filter="posts")
