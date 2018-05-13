from rest_framework.views import APIView
from rest_framework.response import Response


class BannerGeneratorView(APIView):
    def get(self, request, city, price):
        return Response(data={
            'city': city,
            'price': price,
        })
