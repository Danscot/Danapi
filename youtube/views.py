from rest_framework.decorators import api_view

from rest_framework.response import Response

from rest_framework.exceptions import ValidationError

from rest_framework import status

from .youtube import Youtube

yt = Youtube()

@api_view(["GET"])
def search(request):

	query = request.query_params.get('query')

	if not query:

		return Response({

			"status": "failed",

			"message": "This api requires query as a parameter"
			})

	try:

		result = yt.search(query)

		return Response({

			"status": "ok",

			"message":f"search results for {query}",

			"results": result

			})

	except Exception as e:

		print(e)

		return Response({

			"status": "failed",

			"error_message": str(e)
			})


@api_view(["GET"])
def downloader(request):

	fmt = request.query_params.get("fmt")

	url = request.query_params.get("url")

	if not url:

		return Response({

			"status": "failed",

			"message": "This api requires url as a parameter"

			})

	if not fmt:

		return Response({

			"status": "failed",

			"message": "This api requires a format",

			"audio_format_available": 'mp3, m4a, WAV',

			"video_format_available": '1080, 720, 480, 360, 144'

		})

	try:

		result = yt.downloader(url, fmt)

		return Response({

			"creator": "Danscot",

			"status": "ok",

			"message":f"download results for {url}",

			"results": result

			})

	except Exception as e:

		print(e)

		return Response({

			"status": "failed",

			"error_message": str(e)
			})



