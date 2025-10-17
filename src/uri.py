from typing import Any

class Uri(object):
    def __init__(self, raw_url: str) -> None:
        self.url: str = raw_url.replace(" ", "").replace("\n", "")
        
        self.url_structure: list [str] = [elem for elem in self.url.split("/") if elem != ""] # http:, , example.com, fuga, hoge.html
        
        self.protocol: str = self.url_structure[0]
        self.domain: str = self.url_structure[1]
        self.directories: list[str] = self.url_structure[2:-1] if len(self.url_structure) > 3 else []
        filename_and_ext = self.url_structure[-1].split(".")
        self.file: str = filename_and_ext[0]
        self.ext: str = filename_and_ext[1] if (filename_and_ext) == 2 else ""
        
    def __call__(self) -> str:
        return self.url