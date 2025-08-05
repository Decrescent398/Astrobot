import requests
import os
import datetime
import json
from termcolor import colored
from PIL import Image
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from particlescraper.particlescraper.spiders.newsscraper import NewsScraper

# def news():
#     for post in os.listdir("data/out/json/"):
#         os.remove("data/out/json/"+post)
#     for image in os.listdir("data/out/articles/"):
#         os.remove("data/out/articles/"+image)
#     print(colored(f"News files from {(datetime.date.today() - datetime.timedelta(1)).strftime("%d %b %Y")} deleted", "red"))
#     print(colored("Started news", "blue"))
#     process = CrawlerProcess(get_project_settings())
#     process.crawl(NewsScraper)
#     process.start()

def get_mains():

    articles = []

    with open(f"data/out/json/news-output-{datetime.date.today()}.json") as f:
        for line in f:
            articles.append(json.loads(line))

    for article in articles:

        url = "https://ai.hackclub.com/chat/completions"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "messages": [
                {"role": "user", "content": f"""Surround each necessary or bold keyword with **
                                              make sure it is as accurate as possible pretend that 
                                              you're a media writer for a large news corp: {article["points"]}"""}
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
        else:
            content = response.json()
            article["points"] = content['choices'][0]['message']['content']

    with open(f"data/out/json/news-output-{datetime.date.today()}.json", 'w') as f:
        f.write('')
    
    with open(f"data/out/json/news-output-{datetime.date.today()}.json", 'a') as f:
        for article in articles:
            f.write(json.dumps(article + '\n'))

    return articles

def create_slide():
    
    articles = get_mains()

    with open(f"data/out/json/news-output-{datetime.date.today()}.json") as f:
        for line in f:
            articles.append(json.loads(line))