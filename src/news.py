import requests
import re
import os
import datetime
import json
from pathlib import Path
from termcolor import colored
from PIL import Image
import urllib.request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from particlescraper.particlescraper.spiders.newsscraper import NewsScraper

# Output directory paths
OUTPUT_FOLDER = Path("data/out/")
JSON_DATA_PATH = OUTPUT_FOLDER / Path("/json")
ARTICLE_DATA_PATH = OUTPUT_FOLDER / Path("/articles")


def news():
    """Main news function that cleans old files and starts news scraping."""
    # Clean old JSON files
    for json_file in os.listdir(OUTPUT_FOLDER):
        os.remove(JSON_DATA_PATH / Path(json_file))
    
    # Clean old article directories
    for article_dir in os.listdir(ARTICLE_DATA_PATH):
        for item in article_dir:
            os.remove(ARTICLE_DATA_PATH / Path(f"{article_dir}/{item}/"))
    
    yesterday_date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d %b %Y")
    print(colored(f"News files from {yesterday_date} deleted", "red"))
    print(colored("Started news", "green"))
    
    # Start news scraping process
    crawler_process = CrawlerProcess(get_project_settings())
    crawler_process.crawl(NewsScraper)
    crawler_process.start()
    clean_data()


def get_mains():
    """Load articles from JSON file and process them."""
    news_articles = []

    today_date = datetime.date.today()
    json_filename = f"news-output-{today_date}.json"
    
    with open(JSON_DATA_PATH / Path(json_filename)) as json_file:
        for line in json_file:
            news_articles.append(json.loads(line))

    # AI highlighting code (commented out)
    # for article in news_articles:
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

    print(colored("Finished AI highlights", "green"))
    
    # Write processed articles back to file
    with open(JSON_DATA_PATH / Path(json_filename), 'a') as output_file:
        for article in news_articles:
            output_file.write(json.dumps(article) + '\n')

    return news_articles


def clean_data():
    """Clean and organize article data, download images, and create content files."""
    news_articles = get_mains()

    def download_image(image_url, image_name, article_folder):
        """Download an image from URL to specified folder."""
        request_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        image_request = urllib.request.Request(image_url, headers=request_headers)
        
        try:
            with urllib.request.urlopen(image_request) as response:
                image_path = ARTICLE_DATA_PATH / Path(f"{article_folder}/{image_name}.jpg")
                with open(image_path, 'wb') as image_file:
                    image_file.write(response.read())
        except urllib.error.HTTPError as error:
            print(colored(f"Error occurred {error} while downloading {image_url}", "red"))

    print(colored("Starting clean", "green"))

    image_index = 0
    for article in news_articles:
        # Clean title for folder name (remove invalid characters)
        clean_title = re.sub(r'[\/:*?"<>|]', '_', article["title"][0])
        article_folder_path = ARTICLE_DATA_PATH / Path(clean_title)
        os.mkdir(article_folder_path)
        
        # Write article content to file
        content_file_path = article_folder_path / "content.txt"
        with open(content_file_path, 'a') as content_file:
            content_file.write(article["title"][0])
            for content_line in article["points"]:
                content_file.write(content_line + '\n')

        # Download images for this article
        for image_link in article["image-links"]:
            image_name = f"{image_index}"
            if image_index % 2 != 0:
                image_name += "-icon"
            download_image(image_link, image_name, clean_title)
            image_index += 1
