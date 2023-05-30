from bs4 import BeautifulSoup

ROOT_URL = "https://en.pokerpro.cc/"


def update_twitter_embeds(body: BeautifulSoup):
    twitters = body.find_all("blockquote", attrs={"class": "twitter-tweet"})

    result = []
    for twitter in twitters:
        link = twitter.find_all("a")[-1]
        url = link["href"].split("?")[0]
        twitter_info = {"tweet_url": url}
        result.append(twitter_info)
        html = '<!-- wp:embed {"url":"' + url + '","type":"rich","providerNameSlug":"twitter","responsive":true} -->'
        html += '<figure class="wp-block-embed is-type-rich is-provider-twitter wp-block-embed-twitter">'
        html += '<div class="wp-block-embed__wrapper">' + url + '</div>'
        html += '</figure><!-- /wp:embed -->'

        embed_element = BeautifulSoup(html, 'html.parser')
        twitter.replaceWith(embed_element);

    twitter_scripts = body.find_all("script", attrs={"src": "https://platform.twitter.com/widgets.js"})
    for twitter_script in twitter_scripts:
        twitter_script.replaceWith("")

    return result
