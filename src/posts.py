import re
# import os
# from PIL import Image
# import requests
# from bs4 import BeautifulSoup
# from googleapiclient.discovery import build
# from google.oauth2 import service_account

# SCOPES = ["https://www.googleapis.com/auth/documents.readonly", "https://www.googleapis.com/auth/drive.readonly"]
# SERVICE_ACCOUNT_FILE = 'service_account.json'

# creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# drive_service = build('drive', 'v3', credentials=creds)
# docs_service = build('docs', 'v1', credentials=creds)

def extract_doc_id(url):
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    else:
        return None


# def get_whole_text(link):


#     doc = docs_service.documents().get(documentId=extract_doc_id(link)).execute()

#     print("[DEBUG] Document fetched")
#     print("[DEBUG] Document structure:", doc)

#     text = ''
#     for element in doc.get('body').get('content', []):
#         paragraph = element.get('paragraph')
#         if not paragraph:
#             continue
#         for run in paragraph.get('elements', []):
#             text_run = run.get('textRun')
#             if text_run:
#                 text += text_run.get('content')

#     return text

# def get_summary(link):

#     prompt = "You are a copywriter for a social media team creating an Instagram carousel about a major space tech launch. Summarize the following announcement into exactly 6 Instagram carousel slides. Slide 1 should be a bold, punchy headline that grabs attention. Each slide must be concise, clear, and feel impactful — like a story being told one post at a time. Emphasize relevance, urgency, and potential impact. Slides 2–6 should explain the event, its importance, and what’s next, with one key point per slide. No emojis, no hashtags. Write it like a well-paced, news-style carousel aimed at an informed, curious teen/young adult audience."

#     url = "https://ai.hackclub.com/chat/completions"
#     headers = {
#         "Content-Type": "application/json"
#     }
#     data = {
#         "messages": [
#             {"role": "user", "content": f"{prompt} shorten each pointer to ~25words or less optimize for it to sound human generated surround each bold keyword with **{get_whole_text(link)}"}
#         ]
#     }

#     response = requests.post(url, headers=headers, json=data)

#     if response.status_code != 200:
#         print(f"Error: {response.status_code} - {response.text}")
#     else:
#         content = response.json()
#         with open(".txt", 'w') as f:
#             f.write(content['choices'][0]['message']['content'])

# def export_doc_as_html(link):

#     file_id = extract_doc_id(link)
#     if not file_id:
#         print("Invalid doc link.")
#         return

#     response = drive_service.files().export(fileId=file_id, mimeType='text/html').execute()

#     with open("doc.html", 'wb') as f:
#         f.write(response)

# def extract_and_download_images(html_file, output_dir='assets/images'):
#     os.makedirs(output_dir, exist_ok=True)

#     with open(html_file, 'r', encoding='utf-8') as file:
#         soup = BeautifulSoup(file, 'html.parser')

#     img_tags = soup.find_all('img')

#     print(f"Found {len(img_tags)} image(s).")

#     for i, img in enumerate(img_tags):
#         src = img.get('src')

#         if src and src.startswith('https://lh7-rt.googleusercontent.com/'):
#             try:
#                 response = requests.get(src, stream=True)
#                 response.raise_for_status()

#                 img_path = os.path.join(output_dir, f'image_{i+1}.png')
#                 with open(img_path, 'wb') as f:
#                     for chunk in response.iter_content(1024):
#                         f.write(chunk)

#                 print(f"Downloaded image_{i+1}.png")
#             except Exception as e:
#                 print(f"Error downloading image {i+1}: {e}")
#         else:
#             print(f"Skipped image {i+1}: Invalid or missing src")
    
#     os.remove("doc.html")

# def center_crop_all(folder_path="assets/images", output_folder="cropped"):
#     os.makedirs(output_folder, exist_ok=True)

#     new_width, new_height = 1080, 1350

#     for filename in os.listdir(folder_path):
#         img_path = os.path.join(folder_path, filename)
#         if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # skip non-images
#             continue

#         im = Image.open(img_path)
#         width, height = im.size

#         left = (width - new_width)/2
#         top = (height - new_height)/2
#         right = (width + new_width)/2
#         bottom = (height + new_height)/2

#         im = im.crop((left, top, right, bottom))

#         top_crop = int(height * (2 / 3))
#         bottom_crop = height
#         crop_box = (0, top_crop, width, bottom_crop)

#         output_path = os.path.join(output_folder, f"cropped_{filename}")
#         im.save(output_path)
#         print(f"Saved: {output_path}")