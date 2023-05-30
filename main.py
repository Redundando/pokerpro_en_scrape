from create_csv import save_combined_jsons
from download_html_files import get_urls_from_sitemap, run_all

if __name__ == "__main__":
    run_all(urls=get_urls_from_sitemap(), stop_on_error=False)
    save_combined_jsons(filter="casinos")
    save_combined_jsons(filter="posts")
    save_combined_jsons(filter="videos")
