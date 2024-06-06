import logging
import os
from dotenv import load_dotenv
import requests
from utils import get_apod, generate_access_token, upload_image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    # Load the environment variables from .env file
    load_dotenv()
    nasa_api_key = os.environ["NASA_API_KEY"]
    app_key = os.environ["DROPBOX_APP_KEY"]
    app_secret = os.environ["DROPBOX_APP_SECRET"]
    refresh_token = os.environ["DROPBOX_REFRESH_TOKEN"]

    # Get the Astronomy Picture of the Day
    media_type, url, apod_error = get_apod(nasa_api_key)
    if apod_error:
        raise Exception(f"Error fetching APOD: {apod_error}")

    # Get Dropbox Access Token
    access_token = generate_access_token(app_key, app_secret, refresh_token)

    # Upload the image to Dropbox
    if media_type == "image":
        file_name = url.split("/")[-1]
        image_content: bytes = requests.get(url).content
        upload_message, upload_error = upload_image(image_content, file_name, access_token)
        if upload_error:
            raise Exception(f"Error uploading image: {upload_error}")
        logging.info(upload_message)

    # Upload the video to Dropbox
    elif media_type == "video":
        logging.info("APOD is a video. No action taken.")
        # ToDo: Handle video content

    else:
        raise Exception(f"Unknown media type: {media_type}")

    logging.info("Process completed successfully.")
except Exception as e:
    logging.error(f"An error occurred: {e}")
