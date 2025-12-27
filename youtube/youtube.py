import requests

import os

import time

class Youtube:

    def __init__(self):

        self.api_key = os.getenv("YOUTUBE_API")

        self.copy_right = 0

        self.format = ["mp3", "m4a", "WAV", "1080", "720", "480", "360", "144"]

        self.scrape_api = "dfcb6d76f2f6a9894gjkege8a4ab232222"

        self.base_url = "https://p.savenow.to/ajax/download.php?"

    def search(self, q, limit=10):

        url = "https://www.googleapis.com/youtube/v3/search"

        params = {

            "part": "snippet",

            "q": q,

            "type": "video",

            "maxResults": limit + 5,

            "key": self.api_key,
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:

            raise Exception(f"Failed to fetch data: {response.text}")

        print(response)

        data = response.json()

        videos = []

        for item in data.get("items", []):
            
            if item["id"].get("kind") != "youtube#video":

                continue 

            video_id = item["id"].get("videoId")

            if not video_id:

                continue

            snippet = item["snippet"]

            videos.append({

                "title": snippet["title"],

                "url": f"https://www.youtube.com/watch?v={video_id}",

                "thumbnail": snippet["thumbnails"]["high"]["url"],

                "channel": snippet["channelTitle"],

                "description": snippet.get("description", ""),
            })

            print(len(videos))

            if len(videos) == limit:

                break

            return videos

    def downloader(self, url, fmt):

        fmt = str(fmt.strip().replace('"', '').replace("'", ""))

        if fmt not in self.format:

            error = (
                f"Available formats: {self.format}"
            )

            raise Exception(error)

        endpoint = (

            f"{self.base_url}"

            f"copyright={self.copy_right}&"

            f"format={fmt}&"

            f"url={url}&"

            f"api={self.scrape_api}"
        )

        response = requests.get(endpoint)

        data = response.json()

        if data.get("success") != True:

            raise Exception("Download initialization failed")

        info = data["info"]

        title = info.get("title")

        thumb = info.get("image")

        progress_url = data.get("progress_url")

        download_url = self.get_file(progress_url)

        results = {

            "title": title,

            "thumb": thumb,

            "download_url": download_url
        }

        return results

    def get_file(self, progress_url, retries=10):

        for _ in range(retries):

            response = requests.get(progress_url)

            data = response.json()

            if data.get("success") == 1:

                return data.get("download_url")

            time.sleep(1)

        raise Exception("Failed to get download URL")