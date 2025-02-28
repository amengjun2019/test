from django.http import HttpResponse
 
def hello(request):
    return HttpResponse("Hello world ! ")

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from aliyuncode import alisendcode
from llm_invoke import main
import random,json
from django.middleware.csrf import get_token
from custommodel.models import Message,CustomUser,LoginRecord
import pytz 
import datetime

from django.http import StreamingHttpResponse
    

def login(request):
    if request.method=='GET':
        tel=request.GET.get('tel')
        code=request.GET.get('code')
        try:
            
            if LoginRecord.objects.filter(phone_number=tel).exists():
                user_login=LoginRecord.objects.order_by('-sendtime').first()
                # 验证码5分钟有效
                now=datetime.datetime.now()
                now=now.astimezone(pytz.UTC)
                if (now-user_login.sendtime).seconds/60>500:
                        return JsonResponse({'flag':0,'msg':'验证码已失效，请重新获取！'})
                if code==user_login.verify_code:
                    # 如果首次登录 添加新用户
                    if not CustomUser.objects.filter(phone_number=tel).exists():
                        CustomUser.objects.create(phone_number=tel)
                    user=CustomUser.objects.get(phone_number=tel)
                    data={
                        'flag':1,
                        'user':{
                            'tel':user.phone_number
                        },
                        'csrf_token':get_token(request)
                    }
                    
                    return JsonResponse(data)
            return JsonResponse({'flag':0,'msg':'验证码输入错误！'})

        except Exception as e:
            return JsonResponse({'flag':0,'msg':'您还未获取登录验证码！'})

    

def get_csrf_token(request):
    # 手动生成 CSRF 令牌
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})

# 视图函数示例
def my_json_view(request):
    data = {
        'message': 'Hello, World!',
        'status': 'success',
        'data': {
            'user_id': 1,
            'username': 'john_doe'
        }
    }
    return JsonResponse(data)

@csrf_exempt
def json_post(request):
    data = {
        'message': 'This is a my csrf POST request',
        'status': 'success'
    }
    return JsonResponse(data)

# 类视图示例
class MyJsonView(View):
    def get(self, request, *args, **kwargs):
        data = {
            'message': 'This is a GET request',
            'status': 'success'
        }
        return JsonResponse(data)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = {
            'message': 'This is a POST request',
            'status': 'success'
        }
        return JsonResponse(data)
    
def get_code(request):
    if request.method=='GET':
        if 'tel' in request.GET and request.GET['tel']:
            tel=request.GET['tel']
            print(tel)
            digits = list(range(10))
            random.shuffle(digits)
            verify_code = ''.join(str(digit) for digit in digits[:4])

    #         alisendcode.Sample.main([
    #     tel,'阿里云短信测试','SMS_154950909','{"code":'+verify_code+'}'
    # ])
            print(verify_code)

        # 检查是否存在符合条件的记录
        # if LoginRecord.objects.filter(phone_number=tel).exists():
        #     print("记录存在")
        # else:
            LoginRecord.objects.create(phone_number=tel,verify_code=verify_code)

            now  =datetime.datetime.now()
            data={
                    'code':verify_code,
                    'sendtime':now.strftime("%Y-%m-%d %H:%M:%S")
            }
            return JsonResponse(data)
    
def query(request):
    if request.method=='POST':
         try:
             # 解析前端发送的 JSON 数据
            data = json.loads(request.body)
            usermsg=data.get('content')
            modeltype=data.get('modeltype')
            modelname=data.get('modelname')
            uuid=data.get('uuid')
            tel=data.get('tel')
            # 记录用户输入
            Message.objects.create(
                message_id=uuid,
                content=usermsg,
                phone_number=tel,
                user_flag=True

            )
            # msg=[
            #     {"role": "system", "content": "You are a helpful assistant"},
            #     {"role": "user", "content": 'who are you?'},
            # ]
            messages = Message.objects.filter(
                message_id=uuid
            ).order_by('timestamp')

            message_list = [{"role": "system", "content": "You are a helpful assistant"}]
            for message in messages:
                message_list.append({
                    'role': 'user' if message.user_flag else 'system',
                    'content': message.content,
                })

            result= main.llm_invoke(modeltype,modelname,message_list)
            # 记录模型输出
            Message.objects.create(
                message_id=uuid,
                content=result,
                phone_number=tel

            )
    

            data={
                'result':result
            }
            return JsonResponse(data)
         except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
@csrf_exempt
def query_stream(request):
    if request.method=='POST':
         try:
             # 解析前端发送的 JSON 数据
            data = json.loads(request.body)
            usermsg=data.get('content')
            modeltype=data.get('modeltype')
            modelname=data.get('modelname')
            uuid=data.get('uuid')
            tel=data.get('tel')
            # 记录用户输入
            Message.objects.create(
                message_id=uuid,
                content=usermsg,
                phone_number=tel,
                user_flag=True

            )

            
            # msg=[
            #     {"role": "system", "content": "You are a helpful assistant"},
            #     {"role": "user", "content": 'who are you?'},
            # ]
            messages = Message.objects.filter(
                message_id=uuid
            ).order_by('timestamp')

            message_list = [{"role": "system", "content": "You are a helpful assistant"}]
            for message in messages:
                message_list.append({
                    'role': 'user' if message.user_flag else 'system',
                    'content': message.content,
                })
             # 记录模型输出,由于是流式输出，等完整输出后更新content为空的行
            Message.objects.create(
                message_id=uuid,
                # content=result,
                phone_number=tel

            )
            return StreamingHttpResponse(main.stream_llm_response_record(modeltype,modelname,message_list,uuid), content_type="text/plain")
         except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt 
def llm_stream_view(request):
    # 获取用户输入的提示词
    # prompt = request.GET.get("prompt", "Hello, how are you?")
    if request.method=='POST':
         try:
            #  解析前端发送的 JSON 数据
            data = json.loads(request.body)
            usermsg=data.get('content')
            modeltype=data.get('modeltype')
            modelname=data.get('modelname')
            prompt= [{"role": "system", "content": "You are a helpful assistant"},
                     {"role":"user","content":usermsg}]
    # 返回流式响应
            return StreamingHttpResponse(main.stream_llm_response(modeltype,modelname,prompt), content_type="text/plain")
         except:
             return JsonResponse({'error': 'Method not allowed'}, status=405)
         
         