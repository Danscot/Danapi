from rest_framework.decorators import api_view

from rest_framework.response import Response

from rest_framework.exceptions import ValidationError

from rest_framework import status

from .hanime import Hanime

hn = Hanime()

@api_view(["GET"])
def search(request):

	query = request.query_params.get('query')

	if not query:

		return Response({

			"status": "failed",

			"message": "This api requires query as a parameter"
			})

	try:

		result = hn.search(query)

		print(result)

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

