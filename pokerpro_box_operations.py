from bs4 import BeautifulSoup

ROOT_URL = "https://en.pokerpro.cc/"


def update_contact_us_box(body: BeautifulSoup):
    boxes = body.find_all("div", class_="contact-us-inline-wrap")
    result = []
    for box in boxes:
        result.append(box.text)
        html = """
        <!-- wp:group {"className":"contact-us","layout":{"type":"constrained"}} -->
<div class="wp-block-group contact-us"><!-- wp:paragraph {"fontSize":"medium"} -->
<p class="has-medium-font-size"><strong>How to start playing</strong></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Contact us via one of the following options and you will be playing within minutes. Our support team is at your disposal and will be happy to help you!</p>
<!-- /wp:paragraph -->

<!-- wp:social-links {"openInNewTab":true,"showLabels":true,"className":"is-style-pill-shape","layout":{"type":"flex","justifyContent":"center"}} -->
<ul class="wp-block-social-links has-visible-labels is-style-pill-shape"><!-- wp:social-link {"url":"https://wa.me/38669903361","service":"whatsapp"} /-->

<!-- wp:social-link {"url":"https://t.me/PokerProSupportTeam","service":"telegram"} /-->

<!-- wp:social-link {"url":"mailto:prosupport@pokerpro.cc","service":"mail"} /-->

<!-- wp:social-link {"url":"https://join.skype.com/invite/mDg7oNhEIEj7","service":"skype"} /--></ul>
<!-- /wp:social-links --></div>
<!-- /wp:group -->
        """
        box.replace_with(BeautifulSoup(html, "html.parser"))

    return result


def update_social_box(soup: BeautifulSoup):
    boxes = soup.find_all("div", class_="social-list")
    result = []
    for box in boxes:
        result.append(box.text)
        html = """
<!-- wp:group {"className":"social-box","layout":{"type":"constrained"}} -->
<div class="wp-block-group social-box"><!-- wp:paragraph {"align":"center","fontSize":"medium"} -->
<p class="has-text-align-center has-medium-font-size"><strong>Join our channels for more exclusive content</strong></p>
<!-- /wp:paragraph -->

<!-- wp:social-links {"openInNewTab":true,"showLabels":true,"className":"is-style-pill-shape","layout":{"type":"flex","justifyContent":"center"}} -->
<ul class="wp-block-social-links has-visible-labels is-style-pill-shape"><!-- wp:social-link {"url":"https://www.facebook.com/pokerproworld/","service":"facebook"} /-->

<!-- wp:social-link {"url":"https://www.instagram.com/pokerproworld/","service":"instagram"} /-->

<!-- wp:social-link {"url":"https://www.youtube.com/channel/UCe3Yrln50VuemfUFzLaAzYw/","service":"youtube"} /-->

<!-- wp:social-link {"url":"https://t.me/PokerProSupportTeam","service":"telegram"} /-->

<!-- wp:social-link {"url":"https://twitter.com/PokerProWorld","service":"twitter"} /-->

<!-- wp:social-link {"url":"https://wa.me/38669903361","service":"whatsapp"} /-->

<!-- wp:social-link {"url":"mailto:prosupport@pokerpro.cc","service":"mail"} /-->

<!-- wp:social-link {"url":"https://join.skype.com/invite/mDg7oNhEIEj7","service":"skype"} /--></ul>
<!-- /wp:social-links -->

<!-- wp:paragraph {"align":"center"} -->
<p class="has-text-align-center">Make sure to join our <a rel="noreferrer noopener" href="https://discord.gg/ns57da246a" target="_blank">Discord Server</a></p>
<!-- /wp:paragraph --></div>
<!-- /wp:group -->
            """
        box.replace_with(html)

    return result

