from uri import Uri
from rules.basic_rule import BasicRule
from DrissionPage import ChromiumPage
import time

class CloudflareRule(BasicRule): 
    def getHtml(self, uri: Uri) -> str:
        page = ChromiumPage()
        page.get(uri.url)
        time.sleep(2.5) # 認証画面をgetしてしまうので2.5秒スリープ
        html = page.html
        page.quit()
        return html