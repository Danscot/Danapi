import requests

from bs4 import BeautifulSoup


class Tiktok:

	def __init__(self):

		self.base_url = "https://musicaldown.com/en"

		self.post_url = "https://musicaldown.com/download"

		self.session = requests.Session()

		self.session.headers.update({

			"User-Agent": "Mozilla/5.0"
		})

	def __get_token(self):

		resp = self.session.get(self.base_url)

		soup = BeautifulSoup(resp.text, "lxml")

		url_input = soup.find("input", {"id": "link_url"})
		
		hidden_inputs = soup.find_all("input", {"type": "hidden"})

		token_data = {

			"url_field": url_input["name"],

			"token_field": None,

			"token_value": None
		}

		for inp in hidden_inputs:

			if inp.get("name") != "verify":

				token_data["token_field"] = inp["name"]

				token_data["token_value"] = inp["value"]

		return token_data

	def downloader(self, url):

		token = self.__get_token()

		clean_url = url.strip().replace('"', '').replace("'", "")

		payload = {

			token["url_field"]: clean_url,

			token["token_field"]: token["token_value"],

			"verify": "1"
		}

		r = self.session.post(self.post_url, data=payload)

		soup = BeautifulSoup(r.text, "lxml")

		results = []

		for a in soup.find_all("a", href=True):

			href = a["href"]

			event = a.get("data-event")

			if href.startswith("https://fastdl.muscdn.app"):

				results.append({

					"type": event.replace("_download_click", "") if event else "unknown",

					"label": a.get_text(strip=True),
					
					"url": href
				})

		return results
