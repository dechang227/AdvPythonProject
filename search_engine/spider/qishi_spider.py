from ruia import ElementField, AttrField, Item, Request, Spider, TextField
from ruia_ua import middleware as ua_middleware

from search_engine.database.motor_base import MotorBase

class QishiItem(Item):
    target_item = TextField(css_select='div#navbar li')
    href = AttrField(css_select="li>a", attr="href")

class ProjectItem(Item):
    target_item = TextField(css_select='div.infinite-item')
    title = TextField(css_select='span')
    href = AttrField(css_select="div.infinite-item>p.text-align-left>a", attr="href")
    # next_page = AttrField(css_select="a.infinite-more-link", attr="href")

class QishiSpider(Spider):
    # root_url = "https://www.qishicpc.com"
    # start_urls = ["https://www.qishicpc.com/activities/fulllist/", "https://www.qishicpc.com/positions/fulllist/"]
    start_urls = ["https://www.qishicpc.com"]

    request_config = {"RETRIES": 3, "DELAY": 0, "TIMEOUT": 20}
    # 请求信号量
    concurrency = 10
    blog_nums = 0

    async def parse_helper(self, start_url):
        print(start_url)
        next_page = "?page=1"
        while next_page:
            # url = self.start_urls[0] + next_page
            url = start_url + next_page
            req = self.request(url=url, callback=self.parse_item)
            res = await req.fetch()
            # html = await res.text()
            etree = res.html_etree(html=await res.text())
            try:
                next_page = etree.cssselect("a.infinite-more-link")[0].get("href")
            except:
                next_page = None
            yield req

    async def parse(self, response):
        try:
            self.mongo_db = MotorBase(loop=self.loop).get_db()
        except Exception as e:
            self.logger.exception(e)
        
        async for item in QishiItem.get_items(html=await response.text()):
            # print(item.href)
            if item.href.split("/")[1] in ["qcalendar", "activities","positions"]:
                start_url = self.start_urls[0] + item.href
                # print(start_url)
                yield self.parse_helper(start_url)
                # next_page = "?page=24"
                # while next_page:
                #     # url = self.start_urls[0] + next_page
                #     url = start_url + next_page
                #     req = self.request(url=url, callback=self.parse_item)
                #     res = await req.fetch()
                #     # html = await res.text()
                #     etree = res.html_etree(html=await res.text())
                #     try:
                #         next_page = etree.cssselect("a.infinite-more-link")[0].get("href")
                #     except:
                #         next_page = None
                #     yield req
        yield self.parse_helper("https://www.qishicpc.com/topics/list/recent/")

    async def parse_item(self, res):
        # res_list = []
        async for item in ProjectItem.get_items(html=await res.text()):
            # res_list.append(item)
            item_url = self.start_urls[0] + item.href
            is_exist = (
                await self.mongo_db.source_docs.find_one({"url": item_url}) or {}
            )

            if not is_exist.get("html"):
                yield Request(
                    item_url,
                    callback=self.save,
                    metadata={"title": item.title},
                    request_config=self.request_config,
                )

    async def save(self, res):
        html = await res.text()
        data = {"url": res.url, "title": res.metadata["title"], "html": html}
        if html:
            try:
                await self.mongo_db.source_docs.update_one(
                    {"url": data["url"]}, {"$set": data}, upsert=True
                )
            except Exception as e:
                self.logger.exception(e)



if __name__ == '__main__':
    QishiSpider.start(middleware=ua_middleware)





