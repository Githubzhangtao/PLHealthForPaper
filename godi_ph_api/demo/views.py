from django.shortcuts import render

from rest_framework.views import APIView
from utils.Response import JsonResponse


# Create your views here.

class TestView(APIView):
    def get(self, *args, **kwargs):
        ret = [{"name": "zs", "age": 12}, {"name": "ls", "age": 23}]
        return JsonResponse(0, '查询成功', ret)