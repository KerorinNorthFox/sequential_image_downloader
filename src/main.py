from image_downloader import ImageDownloader, load_urls
from uri import Uri
import os

def main(save_dir:str, urls_path:str):
    p = ImageDownloader()

    urls_r = load_urls(urls_path)
    urls_w = urls_r.copy()

    error_url_index = 0
    for url in urls_r:
        try:
            p.download(Uri(url), save_dir)
            urls_w.pop(error_url_index)
        except Exception as e:
            print(e)
            error_url_index += 1
            
    with open(urls_path, mode="w", encoding="utf-8") as f:
        f.writelines(urls_w)

if __name__ == '__main__':
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    save_dir = os.path.join(parent_dir, "save")
    urls_path = os.path.join(parent_dir, "urls.txt")
    
    main(save_dir, urls_path)