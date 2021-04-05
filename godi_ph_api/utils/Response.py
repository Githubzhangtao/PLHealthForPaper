from rest_framework.response import Response
from rest_framework.serializers import Serializer

class JsonResponse(Response):
    '''
    normal
    An HttpResponse that allow its data to be renderd into arbitrary media types.
     {
         "code":200,
         "msg": "",
         "data":[]
     }

     '''

    def __init__(self, code=None, msg=None, data=None,
                 status=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        """

        :param code: 状态码
        :param msg: 返回的提示信息
        :param data: 返回的数据
        :param status:
        :param template_name:
        :param headers:
        :param exception:
        :param content_type:
        """
        super(Response, self).__init__(None, status=status)
        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        ## 这里定义格式
        self.data = {"code": code, "msg": msg, "data": data}

        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type
        if headers:
            for name, value in headers.items():
                self[name] = value