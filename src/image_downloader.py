import urllib.parse
from rules.rules import RULES
from rules.rule import Rule
from uri import Uri
from logger import logger
import os
import urllib

def load_urls(url_txt_path:str) -> list[str]:
    with open(url_txt_path, mode="r", encoding="utf-8") as f:
        urls: list[str] = f.readlines()
        return urls

class ImageDownloader(object):
    def download(self, uri:Uri, save_dir:str):
        print("\n================================")
        logger.info(f"The Url :{uri()}")
        
        if self._check_uri(uri):
            raise Exception("The uri is wrong.")
        
        logger.info(f"\nurl_structure:{uri.url_structure}\nprotocol     :{uri.protocol}\ndomain       :{uri.domain}\ndirectories  :{uri.directories}\nfile         :{uri.file}\n")
        
        rule = self._get_selector_rule(uri.domain)
        if rule is None:
            raise Exception("Rule does not exist.")
        html = rule.get_html(uri)
        body = rule.parse_html(html)
        image_urls: list[str] = rule.collect_image_urls(uri, body)
        title: str|None = rule.get_title(body)
        author: str|None = rule.get_author(body)
        circle_name: str|None = rule.get_circle_name(body)
        
        post_descs = self._compile_post_description(title, author, circle_name, uri.url)
        for desc in post_descs:
            print(desc.strip("\n"))
        
        complete_save_dir = self._combine_save_dir(save_dir, uri, title, author)
        
        for i, image_url in enumerate(image_urls):
            unique_title = title if title is not None else uri.file
            file_name = self._replace_ban_words(f"{unique_title}_{i+1}.jpg", is_slash_contain=True)
            save_path = os.path.join(complete_save_dir, file_name)
            if os.path.exists(save_path):
                logger.warn(f"The file '{file_name}' is already exists. Skip it.")
                continue
            
            with open(save_path, mode="wb") as f:
                image_url = self._supplement_protocol_domain(image_url, uri.protocol, uri.domain)
                img_res = rule.request(image_url)
                f.write(img_res.content)
                logger.info(f"{image_url} Download completed.")

        return post_descs
    
    """
    uriをチェックする
    1.uriにhttpが含まれているか
    """
    def _check_uri(self, uri: Uri) -> bool:
        if not "http" in uri.protocol:
            logger.error("Given uri is not url")
            return True
        return False
    
    """
    ドメインに対応するパースルールを取得
    """
    def _get_selector_rule(self, domain:str) -> Rule:
        for rule in RULES:
            if domain == rule():
                return rule
    
    def _combine_save_dir(self, save_path:str, uri:Uri, title:str|None, author:str|None) -> str:
        dirs = ""
        if uri.directories != []: # urlの間のディレクトリをパスにする
            for directory in uri.directories:
                dirs += "/" + directory
                
        if author is not None:
            dirs = f"{uri.domain}{dirs}/{author}"
        else:
            dirs = f"{uri.domain}{dirs}"
        
        if title is not None:
            dirs = f"{dirs}/{title}_{uri.file}"
        else:
            dirs = f"{dirs}/{uri.file}"
            
        dirs = self._replace_ban_words(dirs)
            
        save_dir_path = os.path.join(save_path, dirs)
        save_dir_path = self._unquote_save_dir(save_dir_path)
            
        logger.info(f"The save directory :{save_dir_path}")
        
        if not os.path.isdir(save_dir_path):
            os.makedirs(save_dir_path)
            logger.info(f"Created a directory {save_dir_path}")
            
        return save_dir_path
    
    def _replace_ban_words(self, text, is_slash_contain=False):
        dir_ban_words = ["?", ":", "<", ">", "|"]
        if is_slash_contain:
            dir_ban_words.append("/")
        for dir_ban_word in dir_ban_words:
            text = text.replace(dir_ban_word, "")
        return text
    
    def _unquote_save_dir(self, save_dir_path):
        dir_path = urllib.parse.unquote(save_dir_path)
        return dir_path
    
    def _supplement_protocol_domain(self, uri_base, protocol, domain):
        uri = uri_base
        if not domain in uri:
            uri = urllib.parse.urljoin(domain, uri_base)
            
        if not protocol in uri:
            uri = urllib.parse.urljoin(protocol, uri_base)
        
        return uri

    def _compile_post_description(self, title:str, author:str, circle_name:str, url:str) -> list[str]:
        result = [f"{title}\n", f"作者：{author}\n", f"サークル名：{circle_name}\n", f"URL：{url}\n", "\n"]
        if circle_name is None:
            result.pop(2)
        return result

