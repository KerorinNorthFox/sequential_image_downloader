from rules.basic_rule import BasicRule
import re

"""
セレクターに記事idが必要なルール
"""
class IdRequiredRule(BasicRule):
    def get_complete_selectors(self, i: int, uri) -> list[str]:
        selectors =  super().get_complete_selectors(i, uri)
        return [selector.replace("yyyy", re.sub("\\D", "", uri.file)) for selector in selectors]
    