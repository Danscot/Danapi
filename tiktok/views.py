from rest_framework.decorators import api_view

from rest_framework.response import Response

from rest_framework.exceptions import ValidationError

from rest_framework import status

from .tiktok import Tiktok

tik = Tiktok()

@api_view(["GET"])
def downloader(request):

	url = request.query_params.get("url")

	if not url:

		return Response({

			"status": "failed",

			"message": "This api requires url as a parameter"

			})

	try:

		result = tik.downloader(url)

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



