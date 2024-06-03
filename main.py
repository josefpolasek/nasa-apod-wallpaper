import os
import requests
from dotenv import load_dotenv
import dropbox
from dropbox.exceptions import ApiError
from dropbox.files import WriteMode
from bs4 import BeautifulSoup
from pythumb import Thumbnail

# Load the environment variables from .env file
load_dotenv()

# Get the NASA API key and Dropbox access token from the environment
NASA_API_KEY = os.getenv("NASA_API_KEY")
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

# Construct the URL for NASA's APOD API
url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
response = requests.get(url)
data = response.json()

# Extract the relevant information
title = data.get("title")
date = data.get("date")
description = data.get("explanation")
media_type = data.get("media_type")
media_url = data.get("url")

# # Print the results
# print("NASA Astronomy Picture of the Day")
# print(f"Title: {title}")
# print(f"Date: {date}")
# print(f"Description: {description}")

# Create a Dropbox object using the access token
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)


# Dropbox target path
def dropbox_target_path(filename):
    return f"/{filename}"


# Check if the file exists in Dropbox
def file_exists_in_dropbox(target_path):
    dbx.files_get_metadata(target_path)
    return True


# Extract the YouTube video URL from a given webpage
def extract_youtube_url(page_url: str) -> str:
    try:
        response = requests.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for the first YouTube link in the page
        for link in soup.find_all('a', href=True):
            if 'youtube.com/watch' in link['href']:
                return link['href']
    except Exception as e:
        print(f'Error extracting YouTube URL: {e}')
        return None


def get_title(page_url: str) -> str | None:
    """Extract the title of the page"""
    try:
        response = requests.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for the title tag in the page
        return soup.title.string
    except Exception as e:
        print(f'Error extracting title: {e}')
        return None


# Handle image media type
if media_type == "image":
    print(f"Image URL: {media_url}")
    # Download the image content
    image_response = requests.get(media_url)
    image_content = image_response.content

    # Upload the file to Dropbox
    target_path = dropbox_target_path(f"{title}.png")
    try:
        if file_exists_in_dropbox(target_path):
            print(f"File '{title}.png' already exists in Dropbox.")
        else:
            dbx.files_upload(image_content, target_path, mode=WriteMode('add'))
            print("File uploaded successfully!")
    except Exception as e:
        print(f"Failed to upload file: {e}")

# Handle video media type
elif media_type == "video":
    print(f"Video URL: {media_url}")

    # Extract the YouTube URL from the provided video URL
    youtube_url = extract_youtube_url(media_url)
    if youtube_url:
        print(f"YouTube URL: {youtube_url}")

        # Get the video title
        video_title = get_title(youtube_url)
        if video_title:
            print(f"Video Title: {video_title}")

            # Fetch the thumbnail
            try:
                t = Thumbnail(youtube_url)
                t.fetch()
                thumbnail_content = t.get_binary()

                # Upload the thumbnail to Dropbox
                target_path = dropbox_target_path(f"{video_title}.jpg")
                if file_exists_in_dropbox(target_path):
                    print(f"File '{video_title}.jpg' already exists in Dropbox.")
                else:
                    dbx.files_upload(thumbnail_content, target_path, mode=WriteMode('add'))
                    print("Thumbnail uploaded successfully!")
            except Exception as e:
                print(f"Failed to fetch or upload thumbnail: {e}")
    else:
        print("Failed to extract YouTube URL.")
else:
    print("The media type is not supported.")
