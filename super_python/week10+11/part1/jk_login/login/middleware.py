from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

class Middle1(MiddlewareMixin):
    def process_request(self,request):
         print(f'中间件请求 {request}')
 
    def process_view(self, request, callback, callback_args, callback_kwargs):
         print(f'中间件视图 {request}')
 
    def process_exception(self, request, exception):
         print(f'中间件异常 {request}')
 
    def process_response(self, request, response):
         print(f'中间件响应 {request}')
         return response