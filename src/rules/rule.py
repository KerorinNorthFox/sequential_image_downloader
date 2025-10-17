import abc
from uri import Uri

class Rule(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self) -> str:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def collect_image_urls(self, uri:Uri) -> list[str]:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def request(self, url:str):
        raise NotImplementedError()