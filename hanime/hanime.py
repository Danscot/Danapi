
import requests

from bs4 import BeautifulSoup

import re

class Hanime:

	def __init__(self):

		self.base_url = "https://hentai.tv"

		self.s_url = f'{self.base_url}/?s='

	def search(self, query):

		url = f'{self.s_url}{query}'

		print(url)

		html = requests.get(url).text

		parser = BeautifulSoup(html, 'lxml')

		image_list = parser.select('div.crsl-slde img')

		href_list = parser.select('div.crsl-slde a')

		result = []

		href = []

		for r in href_list:

			lk =  r.get("href")

			data_link = re.sub(r"-episode(?=-|$)", "", lk)

			streaming_link = data_link.rstrip('/').split('/')[-1]

			href.append({

				"title": r.get_text(),

				"link": lk,

				"streaming_link": f'https://r2.1hanime.com/{streaming_link}.mp4'

				})

		return href


