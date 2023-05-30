import os
import shutil

import requests
from PIL import Image
from bs4 import BeautifulSoup
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

from logger import log

ROOT_URL = "https://en.pokerpro.cc/"


def get_image_information(image):

    url = image["src"]
    if ("http://" not in url) or ("https://" not in url):
        image_url = ROOT_URL + url
    result = image.attrs.copy()
    result["image_url"] = image_url
    result["filename"] = image_url.split("/")[-1]
    return result


def get_content_images(body=BeautifulSoup()):
    images = body.find_all("img")
    result = []
    for i in images:
        info = get_image_information(i)
        result.append(info)

    return result


def update_page_images(body: BeautifulSoup, default_alt=""):
    images = body.find_all("img")
    image_information = []
    for i in images:
        image_info = get_image_information(i)
        r = requests.get(image_info["image_url"], stream=True)
        if i["src"] == "" or r.status_code != 200:
            print("::::")
            print("IMAGE NOT FOUND")
            print(image_info)
            print("::::")
            i.replaceWith("")
        else:
            image_info["filename"] = download_image(image_info["image_url"])
        i["src"] = "/wp-content/uploads/" + image_info["filename"]
        i["alt"] = image_info["alt"] if ("alt" in image_info and image_info["alt"] != "") else default_alt
        image_information.append(image_info | i.attrs.copy())
    return image_information



def convert_svg_to_png(filename=""):
    if filename[-3:] != "svg":
        return filename
    image = svg2rlg(filename)
    new_filename = filename[:-3] + "png"
    renderPM.drawToFile(image, new_filename, fmt="PNG")
    os.remove(filename)
    return new_filename


def resize_image(image: Image, max_width = 1200, max_height=2400):
    image.thumbnail((max_width, max_height), resample=Image.Resampling.LANCZOS)


def compress_image(filename="", max_size=95000, min_quality=10):
    remove_old_file = False
    if filename[-3:] == "svg":
        filename = convert_svg_to_png(filename)
    with Image.open(filename) as image:
        file_size = os.path.getsize(filename)
        if file_size > max_size:
            remove_old_file = True
            new_filename = filename[0:filename.rfind(".")] + ".webp"
            quality = 95
            resize_image(image)
            while file_size > max_size and quality >= min_quality:
                print(f"Compressing image {filename:<40} - Size: {file_size:<10} - Quality: {quality:<5}")
                image.save(new_filename, optimize=True, quality=quality)
                file_size = os.path.getsize(new_filename)
                quality -= 10
    if remove_old_file:
        os.remove(filename)
    return new_filename if remove_old_file else filename


def download_image(image_url=""):
    filename = "images/" + image_url.split("/")[-1]
    if not os.path.exists("images/"):
        os.makedirs("images/")

    r = requests.get(image_url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        new_filename = compress_image(filename)
        return new_filename.split("/")[-1]
    return -1
