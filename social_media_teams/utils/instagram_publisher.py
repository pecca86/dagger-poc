import requests
import http.server
import socketserver
import threading
import subprocess
import time
import json
import re
import logging

logger = logging.getLogger(__name__)

from configs.app_config import AppConfig

app_config = AppConfig()

class InstagramPublisher:
    saved_data = []
    def __init__(self) -> None:
        self.config = AppConfig()

    def publish(self, filename: str, caption: str) -> None:
        """
        Publish an image to instagram
        """

        cleaned_caption = re.sub('^"|"$', '', caption) #cleans the double quotes from the tweet

        # # Start a simple HTTP server in a new thread
        PORT = 8000
        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", PORT), Handler)
        thread = threading.Thread(target=httpd.serve_forever)
        thread.start()

        # Start ngrok
        ngrok = subprocess.Popen(["ngrok", "http", str(PORT)], stdout=subprocess.PIPE)

        # Give ngrok time to start up
        time.sleep(2)

        # Get the public URL from ngrok
        resp = requests.get("http://localhost:4040/api/tunnels")
        public_url = resp.json()["tunnels"][0]["public_url"]

        # Now you can use the public URL to access your local images
        image_url = f"{public_url}/instagram_images/{filename}"

        access_token = self.config.instagram_long_term_access_token

        # get media container id
        media_container_id = self.create_media_container(
            access_token, image_url, cleaned_caption
        )
        response = self.publish_photo(access_token, media_container_id)

        print("Saved data: ", self.saved_data)
        logging.info("Saved data: ", self.saved_data)
        # Remember to stop ngrok and the HTTP server when you're done
        ngrok.terminate()
        httpd.shutdown()

        return response

    def create_media_container(self, access_token, image_url, cleaned_caption):
        url = (
            f"https://graph.facebook.com/v18.0/{app_config.meta_instagram_app_id}/media"
        )
        payload = {
            "image_url": image_url,
            "caption": cleaned_caption,
            "access_token": access_token,
        }
        response = requests.post(url, params=payload)
        data = response.json()
        self.saved_data.append(data)
        return data["id"]

    def publish_photo(self, access_token, creation_id):
        url = f"https://graph.facebook.com/v18.0/{app_config.meta_instagram_app_id}/media_publish"
        payload = {"creation_id": creation_id, "access_token": access_token}
        response = requests.post(url, params=payload)
        data = response.json()
        self.saved_data.append(data)
        return data
