
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


The activities are listed in multiple pages, so we need to continue searching whether there is more page to scrap. <br />
![infinite page](/docs/infinite_page.jpg?raw=true "Infinite page")

## Data storage


## Backend server


## Client interface

