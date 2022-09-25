from ruia import ElementField, AttrField, Item, Request, Spider, TextField
from ruia_ua import middleware as ua_middleware

from search_engine.database.motor_base import MotorBase
import asyncio

class QishiItem(Item):
    target_item = TextField(css_select='div#navbar li')
    # sector = ElementField(css_select="ul")
    href = AttrField(css_select="li>a", attr="href")


class TestSpider(Spider):
    start_urls = ["https://www.qishicpc.com"]

    async def parse(self, response):
        async for item in QishiItem.get_items(html=await response.text()):
            print(item.href)
            yield Request(
                item.href,
                callback=self.parse_item
            )

    async def parse_item(self, res):
        pass


# async def print_href(url):
#     async for item in QishiItem.get_items(url="https://www.qishicpc.com"):
#         print(item.href)

if __name__ == "__main__":
    # async_func = QishiItem.get_item(url="https://www.qishicpc.com")
    # item = asyncio.get_event_loop().run_until_complete(async_func)
    # for li in item.sector.findall('li'):
    #     print(li.find('a').get("href"), end=" ")

    # print_href(url="https://www.qishicpc.com")
    TestSpider.start()
