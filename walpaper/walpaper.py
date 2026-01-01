import requests

from bs4 import BeautifulSoup

class Walpaper:

	BASE_HEADERS = {

		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
	}

	RESOLUTIONS_PRIORITY = [
		"3840x2160", "2560x1440", "2560x1080",
		"1920x1200", "1920x1080",
		"1680x1050", "1600x900",
		"1536x864", "1440x900",
		"1366x768", "1280x720"
	]

	def __init__(self, timeout=2):

		self.timeout = timeout

	def _head_exists(self, url):

		try:

			r = requests.head(

				url,

				headers=self.BASE_HEADERS,

				timeout=self.timeout,

				allow_redirects=True
			)

			return r.status_code == 200

		except requests.RequestException:

			return False

	def _build_download_url(self, page_url, resolution):

		return f"{page_url}/download/{resolution}"

	def _pick_resolutions(self, page_url, default_res):

		selected = []

		if default_res:

			selected.append({

				"resolution": default_res,

				"url": self._build_download_url(page_url, default_res)
			})

		for res in self.RESOLUTIONS_PRIORITY:

			if len(selected) >= 5:

				break

			if res == default_res:

				continue

			url = self._build_download_url(page_url, res)

			if self._head_exists(url):

				selected.append({

					"resolution": res,

					"url": url
				})

		return selected

	def parse_gallery_html(self, url):

		html = requests.get(url, headers=self.BASE_HEADERS).text

		soup = BeautifulSoup(html, "lxml")

		items = soup.select("ul#gallery li[itemprop='associatedMedia']")

		results = []

		for item in items:

			page = item.select_one("a[itemprop='url']")

			img = item.select_one("img.lazy")

			res = item.select_one("span.res")

			caption = item.select_one("figcaption")

			if not page or not img:

				continue

			page_url = page["href"]

			preview_url = img.get("data-src")

			default_res = res.text.strip().replace("px", "") if res else None

			title = caption.text.strip() if caption else None

			resolutions = self._pick_resolutions(page_url, default_res)

			results.append({

				"title": title,

				"preview": preview_url,

				"page_url": page_url,

				"resolutions": resolutions
			})

		return results

	def downlaoder(self, query):

		url = f"https://www.wallpaperflare.com/search?wallpaper={query}"

		r = self.parse_gallery_html(url)

		print(r)

		return r	