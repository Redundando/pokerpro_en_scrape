# PokerProCC Scraper

Run `main.py` to run the entire script. The process will take some minutes.

## Actions taken

- Downloads all pages listed under [https://en.pokerpro.cc/sitemap.xml](https://en.pokerpro.cc/sitemap.xml)
- Extracts:
  - URL
  - Title
  - Slug
  - Category
  - Meta Description
  - Meta Title
  - Author Name
  - Page Type
  - Published Date
  - Modified Date
  - Post Body (as HTML)
  - Tags
  - All Images (including Thumbnail)
- Extracts for Casino reviews:
  - Logo
  - Bonus Description
  - Promo Description
  - Affiliate Link
  - Licence Information
  - List of restricted countries
  - Company name
- Resizes all images (ensure size is <100kb)
- Provides fitting alt text for image
- Adjusts internal links to fit new URL structure
- Converts "Contact Us Block" into WP block (if in post body)
- Converts "Social Links Block" into WP block (if in post body)
- Converts Twitter Embeds into WP block (if in post body)
- Converts Youtube Embeds into WP block (if in post body)

## Information that needs to entered manually:

- Short bonus text for each operator (in `bonus.py`)
- Operator rating (in `ratings.py`)

## Uploading data to WordPress

After the script is run, the following actions need to be taken to import the data to wordpress:
- Upload all images into the media library
- Import `articles-casinos.json`, `articles-posts.json`, `articles-videos.json` via WP all import plugin
  - Full version needed (contact `arved.kloehn@gmail.com` for access)
  - All fields need to be connected correctly in the plugin before import

## Open Issues

- Sort videos pages properly
- Run proper checks to ensure all links work correctly
- Provide list of all link adjustments for redirects (to ensure old external links pointing to now non existing URLs still work)
