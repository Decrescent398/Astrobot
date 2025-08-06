import requests
import os
import datetime
import json
from termcolor import colored
from PIL import Image
import urllib.request
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

    with open(f"data/out/json/news-output-{datetime.date.today()}-p.json") as f:
        for line in f:
            articles.append(json.loads(line))

    # for article in articles:

    #     url = "https://ai.hackclub.com/chat/completions"
    #     headers = {
    #         "Content-Type": "application/json"
    #     }
    #     data = {
    #         "messages": [
    #             {"role": "user", "content": f"""Surround each necessary or bold keyword with **
    #                                           make sure it is as accurate as possible pretend that 
    #                                           you're a media writer for a large news corp: {article["points"]}"""}
    #         ]
    #     }

    #     response = requests.post(url, headers=headers, json=data)

    #     if response.status_code != 200:
    #         print(f"Error: {response.status_code} - {response.text}")
    #     else:
    #         content = response.json()
    #         article["points"] = content['choices'][0]['message']['content']

    with open(f"data/out/json/news-output-{datetime.date.today()}-p.json", 'w') as f:
        f.write('')
    
    with open(f"data/out/json/news-output-{datetime.date.today()}-p.json", 'a') as f:
        for article in articles:
            f.write(json.dumps(article) + '\n')

    return articles

def create_slide():
    
    articles = get_mains()

    def download_image(url, name):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as response:
                with open(f'data/out/images/{name}.jpg', 'wb') as file:
                    file.write(response.read())
        except urllib.error.HTTPError as e:
            print(colored(f"Error occured {e} while downloading {url}", "red"))

    index = 0
    for article in articles:
        for image in article["image-links"]:
            name = f"{index}"
            if index%2!=0: name+="-icon"
            download_image(image, name)
            index += 1

create_slide()