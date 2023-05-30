from bs4 import BeautifulSoup


def heading(soup: BeautifulSoup = None, level=2) -> BeautifulSoup:
    html = '<!-- wp:heading '
    if level != 2:
        html += '{"level":' + level + '} '
    html+= '-->'
    html+=str(soup)
    html+='<!-- /wp:heading -->'
    return BeautifulSoup(html, "html.parser")


def paragraph(soup: BeautifulSoup = None) -> BeautifulSoup:
    html = '<!-- wp:paragraph -->'
    html+=str(soup)
    html+='<!-- /wp:paragraph -->'
    return BeautifulSoup(html, "html.parser")


def div(soup: BeautifulSoup = None) -> BeautifulSoup:
    html = ''
    for child in soup.children:
        html+=str(child)
    return BeautifulSoup(html, "html.parser")
