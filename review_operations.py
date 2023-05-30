from bs4 import BeautifulSoup

import country_operations
import image_operations
import wp_blocks

ROOT_URL = "https://en.pokerpro.cc/"


def create_review(body: BeautifulSoup = None, side_boxes: list[BeautifulSoup] = None,
                  promotions_tab: BeautifulSoup = None, include_restricted_countries = False) -> BeautifulSoup:
    result = BeautifulSoup()
    company_information = None
    screenshots = None
    restricted_countries = None
    eligible_countries = None

    for side_box in side_boxes:
        headline = side_box.find(class_="top").find("span").text.lower().strip()
        if headline == "company information":
            company_information = side_box
        if headline == "lobby & table":
            screenshots = side_box
        if headline == "restricted countries":
            restricted_countries = side_box
        if headline == "eligible countries":
            eligible_countries = side_box
    result.append(how_to_sign_up_box(promotions_tab))
    result.append(body)
    if screenshots:
        result.append(screenshots_box(screenshots))
    if company_information:
        result.append(company_information_box(company_information))

    if restricted_countries and include_restricted_countries:
        result.append(countries_box(restricted_countries, type="restricted"))
    if eligible_countries:
        result.append(countries_box(eligible_countries, type="eligible"))
    return result


def screenshots_box(box: BeautifulSoup) -> BeautifulSoup:
    images = box.find_all("img")
    html = ('<!-- wp:group {"className":"operator-screenshots","layout":{"type":"constrained"}} -->'
            '<div class="wp-block-group operator-screenshots"><!-- wp:heading {"style":{"typography":{"fontStyle":"normal","fontWeight":"100"}},"fontSize":"medium"} -->'
            '<h2 class="has-medium-font-size" style="font-style:normal;font-weight:100">Screenshots</h2>'
            '<!-- /wp:heading -->'
            '<!-- wp:columns -->'
            '<div class="wp-block-columns">')

    for image in images:
        html += ('<!-- wp:column -->'
                 '<div class="wp-block-column"><!-- wp:image {"sizeSlug":"large"} -->'
                 '<figure class="wp-block-image size-large"><img src="')
        html += image["src"]
        html += ('" alt="Screenshot"/></figure>'
                 '<!-- /wp:image --></div>'
                 '<!-- /wp:column -->')
    html += ('</div><!-- /wp:columns --></div>'
             '<!-- /wp:group -->')

    result = BeautifulSoup(html, "html.parser")
    return result


def company_information_box(box: BeautifulSoup) -> BeautifulSoup:
    html = ('<!-- wp:group {"className":"company-information","layout":{"type":"constrained"}} -->'
            '<div class="wp-block-group company-information"><!-- wp:heading {"style":{"typography":{"fontStyle":"normal","fontWeight":"100"}},"fontSize":"medium"} -->'
            '<h2 class="has-medium-font-size" style="font-style:normal;font-weight:100">Company Information</h2>'
            '<!-- /wp:heading -->'
            '<!-- wp:table {"className":"is-style-stripes"} -->'
            '<figure class="wp-block-table is-style-stripes">')
    table = box.find_all("table")[0]
    html += str(table)
    html += ('</figure>'
             '<!-- /wp:table --></div>'
             '<!-- /wp:group -->')
    html = html.replace("<tbody>", "").replace("</tbody>", "")
    result = BeautifulSoup(html, "html.parser")
    return result


def countries_box(box: BeautifulSoup, type="eligible") -> BeautifulSoup:
    images = box.find_all("img")
    html = ('<!-- wp:group {"className":"country-information","layout":{"type":"constrained"}} -->'
            '<div class="wp-block-group country-information"><!-- wp:heading {"style":{"typography":{"fontStyle":"normal","fontWeight":"100"}},"fontSize":"medium"} -->'
            '<h2 class="has-medium-font-size" style="font-style:normal;font-weight:100">')
    html += type.title()
    html += (' Countries</h2>'
             '<!-- /wp:heading -->'
             '<!-- wp:group {"className":"country-flags","layout":{"type":"constrained"}} -->'
             '<div class="wp-block-group country-flags">')
    for image in images:
        # image["alt"] = "Country Flag " + image["title"]
        # html += ('<!-- wp:image {"sizeSlug":"large"} -->'
        #         '<figure class="wp-block-image size-large">')
        # html += f'<img src="{image["src"]}" alt="{image["alt"]}" title="{image["title"]}"/>'
        # html += '</figure><!-- /wp:image -->'
        html += f'<!-- wp:shortcode -->[flag-{image["title"].split(" ")[0]}]<!-- /wp:group -->'
    html += ('</div>'
             '<!-- /wp:group --></div>'
             '<!-- /wp:group -->')
    result = BeautifulSoup(html, "html.parser")
    return result


def how_to_sign_up_box(box: BeautifulSoup) -> BeautifulSoup:
    remove_double_paragraphs_html = str(box).replace("<p><p>", "<p>").replace("</p></p>", "</p>")
    box = BeautifulSoup(remove_double_paragraphs_html, "html.parser")
    html = ('<!-- wp:group {"style":{"color":{"background":"#00aae017"}},"layout":{"type":"constrained"}} -->'
            '<div class="wp-block-group has-background" style="background-color:#00aae017">')
    divs = box.find_all("div")
    for div in divs:
        div.unwrap()
    for child in box.find_all(recursive=False):
        if child.name in ["h1", "h2", "h3", "h4", "h5"]:
            html += str(wp_blocks.heading(child, child.name[-1]))
        if child.name == "p":
            html += str(wp_blocks.paragraph(child))
    html += ('<!-- wp:shortcode -->'
             '[offer-contact-form]'
             '<!-- /wp:shortcode -->'
             '</div>'
             '<!-- /wp:group -->')
    result = BeautifulSoup(html, "html.parser")
    return result


def get_logo(soup: BeautifulSoup) -> str:
    logo = soup.find("div", class_="header-offer-logo")
    image_information = image_operations.update_page_images(logo)
    return image_information[0]["src"]


def get_bonus(soup: BeautifulSoup) -> str:
    bonus_block = soup.find("div", class_="header-offer-deal")
    bonus_headline = bonus_block.find("h2").text
    bonus_details = bonus_block.find("p").text
    return f"<p><strong>{bonus_headline}</strong></p><p>{bonus_details}</p>"


def get_short_bonus(soup: BeautifulSoup) -> str:
    bonus_block = soup.find("div", class_="header-offer-deal")
    bonus_headline = bonus_block.find("h2").text
    return bonus_headline

def get_external_link(soup: BeautifulSoup) -> str:
    bonus_block = soup.find("div", class_="header-offer-deal")
    link = bonus_block.find("a")["href"]
    return link


def get_license(soup: BeautifulSoup) -> str:
    side_boxes = soup.find_all(class_="side-box")
    for side_box in side_boxes:
        headline = side_box.find(class_="top").find("span").text.lower().strip()
        if headline == "company information":
            return side_box.find_all("td")[-1].text


def get_restricted_countries(soup: BeautifulSoup) -> str:
    result = []
    side_boxes = soup.find_all(class_="side-box")
    for side_box in side_boxes:
        headline = side_box.find(class_="top").find("span").text.lower().strip()
        if headline == "restricted countries":
            images = side_box.find_all("img")
            for image in images:
                alpha2 = image["title"].split(" ")[0]
                result.append(country_operations.alpha2_to_country_name(alpha2))
    return ",".join(result)


def get_short_title(title: str = "") -> str:
    return title.split("|")[0].strip()


def get_company_name(soup: BeautifulSoup) -> str:
    side_boxes = soup.find_all(class_="side-box")
    for side_box in side_boxes:
        headline = side_box.find(class_="top").find("span").text.lower().strip()
        if headline == "company information":
            return side_box.find_all("td")[1].text
