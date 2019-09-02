SKILL DEMAND MONITORING
-----------------------

This script/application scrap job boards/websites to build a database of job offers that will be exploited to determine the trends of IT skills demands: what technologies are being asked ? 

# Architecture

Micro-services:
- 1 Application to collect the data (Python, Beautiful Soup) and store them (NoSQL/MongoDB) - Script to be run as a CRON job
- 1 Application to access the data (API) (Python: Flask-RESTful) - Not required, but personal goalNLTK
- 1 Application to analyse and display the analytics (Python: Flask, NLTK (Natural Language Processing), Pandas/Mathplotlib (or DC/C3 or Highcharts?))

# To-do

- Build `scrap.Website' class
- Create MongoDB acccount
- Script storing data on MongoDB
