
This project is for Qishi Advanced Python Programming course.  


## Introduction
There is no search engine on Qishi website: https://www.qishicpc.com. Every time I need to go to specific pages and scroll up and down to find the items I look for. So I think it's valuable to build a search engine for Qishi website. I will folow a course from https://www.lanqiao.cn for this project: https://www.lanqiao.cn/courses/1196. In this project, we will build an async version web scraper to scrap the information of activities and positions from different pages in Qishi website. The scrapped data will be stored in mongodb database. Then, we will build index for the items and build ranking system for searching. If we have more time, we can build a web server for the search engine. 
  
**Learn from the project**:
-	async http request
-	web spider framework
-	css selector
-	MongoDB
-	search engine indexing


## Qishi spider
I have spent most time on this part. In oirder to scrap links from Qishi website, it requires to understand the html source scripts of the website. On the source code of the mainpage, we'd like to scrap the infomration from the subpages: qcalendar, activities and positions. There is one more subpage which is not shown here we'd like to scrap as well, the subpage for upcoming activities: https://www.qishicpc.com/topics/list/recent/. 
![Qishi page source code](/docs/qishicpc_page_source.jpeg?raw=true "Qishi page source code")

For the subpage such as Qishi activities, we can find the activities in the following pattern.<br />
![item](/docs/item.jpg?raw=true "Item")

The activities are listed in multiple pages, so we need to continue searching whether there is more page to scrap by finding the pattern at the end of the page. <br />
![infinite page](/docs/infinite_page.jpg?raw=true "Infinite page")

To grab the elements of items and new pages, we use css selector here.

The spider is in search_engine/spider/qishi_spider.py. The data saved are title, url and html content.

## Data storage
MongDB is used for storing the data. In order to run qishi_spider.py, we need to start the local MongDB service. Instalation and usage of MongDB in Mac OS can be found at https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/.


## Search server
I mainly used the scripts from the course for this part and the the client interface, with some customized changes. The idea is to indexing the title and do cosine similarity to rank the doc seaching results.


## Client interface
Run python app.py, it will start the server. The local url for the search engine is : http://0.0.0.0:8001. You can see the user interface as below:<br />
![qishi search page](/docs/qishi_search.jpg?raw=true "qishi search")

For example, searching for "advanced python program":
![qishi search results](/docs/qishi_search_results.jpg?raw=true "qishi search results")



