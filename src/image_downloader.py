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
        logger.info(f"The Url :{uri()}")
        
        if self._check_uri(uri):
            raise Exception("The uri is wrong.")
        
        print("\n================================")
        logger.info(f"\nurl_structure:{uri.url_structure}\nprotocol     :{uri.protocol}\ndomain       :{uri.domain}\ndirectories  :{uri.directories}\nfile         :{uri.file}\n")
        
        rule = self._get_selector_rule(uri.domain)
        if rule is None:
            raise Exception("Rule does not exist.")
        image_urls: list[str] = rule.collect_image_urls(uri)
        
        complete_save_dir = self._combine_save_dir(save_dir, uri)
        
        for i, image_url in enumerate(image_urls):
            save_path = os.path.join(complete_save_dir, f"{i+1}.jpg")
            if os.path.exists(save_path):
                logger.warn(f"The file is already exists. Skip it.")
                continue
            
            with open(save_path, mode="wb") as f:
                img_res = rule.request(image_url)
                f.write(img_res.content)
                logger.info(f"{image_url} Download completed.")
    
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
    
    def _combine_save_dir(self, save_path, uri) -> str:
        dirs = ""
        if uri.directories != []: # urlの間のディレクトリをパスにする
            for directory in uri.directories:
                dirs += "/" + directory
                
        dirs = f"{uri.domain}{dirs}/{uri.file}"
        
        dir_ban_words = ["?", "？", ":"]
        for dir_ban_word in dir_ban_words:
            dirs = dirs.replace(dir_ban_word, "")
            
        save_dir_path = os.path.join(save_path, dirs)
        save_dir_path = self._unquote_save_dir(save_dir_path)
            
        logger.info(f"save directory :{save_dir_path}")
        
        if not os.path.isdir(save_dir_path):
            logger.info(f"Try to create a directory : {save_dir_path}")
            os.makedirs(save_dir_path)
            logger.info(f"Created a directory {save_dir_path}")
            
        return save_dir_path
    
    def _unquote_save_dir(self, save_dir_path):
        dir_path = urllib.parse.unquote(save_dir_path)
        return dir_path