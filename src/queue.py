from image_downloader import ImageDownloader
from uri import Uri
import os
import click

@click.command()
@click.argument("url", type=str)
def main(url:str, save_dir, post_path):
    print(url)
    print(type(url))
    p = ImageDownloader()

    try:
        post_texts = p.download(Uri(url), save_dir)
        with open(post_path, mode="a", encoding="utf-8") as f:
            f.writelines(post_texts)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    save_dir = os.path.join(parent_dir, "save")
    post_path = os.path.join(parent_dir, "posts.txt")
    
    main(save_dir)
