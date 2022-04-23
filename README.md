# COVID-19-Monitoring
COVID-19 Real Time Tracking

This project comes from https://www.bilibili.com/video/BV177411j7qJ 。

This project crawls all COVID-19 data from Tencent COVID-19 related websites by using crawlers, and then stores them in MySQL database. After analyzing and screening the data, it is displayed on the page by using auxiliary tools such as Echarts, JS and Jieba.

The page layout is divided into seven parts:

The title, date and time are displayed at the top.

The upper left is the trend curve analysis of daily new diagnosis and heal.

The lower left is a rolling display of the list of medium and high risk areas.

The upper center is the numerical display of important data.

The middle and lower center shows the severity of the COVID-19 situation in various regions by dyeing the map of China.

The top right is the histogram analysis of the remaining five provinces with the most confirmed cases.

The lower right is the word cloud picture composed of daily hot search keywords.

Change the database username and password in spider.py and sql_utils.py to yours, and run spider.py first, then run app.py.
