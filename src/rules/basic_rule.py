from bs4 import BeautifulSoup
from uri import Uri
from rules.rule import Rule
import requests
from logger import logger

"""
基本的な処理が実装されたルール
"""
class BasicRule(Rule):
    """
    _domain                : str       -> ルールのドメイン名
    _selectors             : list[str] -> 先頭のimgタグのセレクター
    _start_nth_child_index : int       -> imgタグの開始位置 (nth-child(xxxx))
    _step                  : int       -> nth-childの増え方
    _try_again_limit       : int       -> imgタグが見つからなかった時何回やり直すか
    """
    def __init__(self, domain:str, selectors:list[str], start_nth_child_index:int, title_selector:str="", step:int=1, try_again_limit:int=2):
        self._domain = domain
        self._selectors = selectors
        self._start_nth_child_index = start_nth_child_index
        self._title_selector = title_selector
        self._step = step
        self._try_again_limit = try_again_limit
    
    def __call__(self) -> str:
        return self._domain
        
    @property
    def selectors(self):
        return self._selectors
    
    @property
    def start_nth_child_index(self):
        return self._start_nth_child_index
        
    # uri先のサイトの縦に並べられた画像のurlをリストとして取得
    def collect_image_urls(self, uri, body) -> list[str]:
        image_urls: list[str] = []
        
        i = 0
        selector_number = 0
        try_again_limit = self._try_again_limit
        while(True):
            selectors: str = self.get_complete_selectors(i, uri)
            img = body.select(selectors[selector_number])
            
            if img == []:
                if try_again_limit > 0:
                    logger.warn(f"img is not exist. Try again same selector. (try count :{try_again_limit})")
                    try_again_limit -= 1
                    i += 1
                    continue
                if selector_number+1 >= len(selectors):
                    logger.error("img is not exist.")
                    break
                logger.warn("img is not exist. Try another selector.")
                selector_number += 1
                continue
            
            src = self.get_image_src(img)
            if src == "" or src is None:
                logger.error("src is not exist.")
                continue
            logger.info(f"src :{src}")
            image_urls.append(src)
            i += self._step
            try_again_limit = self._try_again_limit
        
        return image_urls
    
    def get_title(self, body) -> str | None:
        if self._title_selector == "":
            return None
        title = body.select(self._title_selector)
        if title == []:
            return None
        return title[0].get_text(strip=True)
    
    def request(self, url:str):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"}
        res = requests.get(url, headers=headers)
        return res
    
    # uri先のhtmlを取得
    def get_html(self, uri:Uri) -> str:
        res = self.request(uri.url)
        if res.status_code != 200 and res.status_code != 201:
            raise Exception(f"Cannot connect -> status code:{res.status_code}")
        html = res.text
        return html
    
    # htmlをbeautifulsoupでパース
    def parse_html(self, html:str):
        body = BeautifulSoup(html, "html.parser")
        return body
        
    def get_complete_selectors(self, i:int, uri) -> list[str]:
        return [selector.replace("xxxx", str(i+self.start_nth_child_index)) for selector in self.selectors]
    
    def get_image_src(self, img):
        for attr in img[0].__dict__["attrs"]:
            if "src" in attr:
                key = attr
        src = img[0][key]
        src = src.split(" ")[0]
        return src