from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection  # 用于执行原始 SQL 查询
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@api_view(['GET', 'POST'])
def get_data(request):
    if request.method == 'GET':
        data = {'message': 'Hello from Django!'}
    elif request.method == 'POST':
        received_data = request.data.get('data', '')
        data = {'message': f'Server received: {received_data}'}
    return Response(data)

# 新增的处理函数
@api_view(['GET', 'POST'])
def process_data(request):
    if request.method == 'GET':
        return Response({'message': 'Welcome to process_data API!'})

    elif request.method == 'POST':
        received_data = request.data.get('data', '')
        # 模拟数据处理逻辑
        processed_result = received_data.upper()  # 简单的例子：将数据转换为大写
        return Response({'message': 'Data processed successfully', 'processed_data': processed_result})



@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    with connection.cursor() as cursor:
        # 使用原生 SQL 查询用户信息
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", [username, password])
        user = cursor.fetchone()

    if user:
        return Response({'message': '登录成功'})
    else:
        return Response({'message': '登录失败，用户名或密码错误'})


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        # 验证用户名和密码长度
        if len(username) < 6:
            return JsonResponse({'error': '用户名要大于等于六字节'})
        if len(password) < 6:
            return JsonResponse({'error': '密码要大于等于六字节'})

        # 检查用户名和邮箱的唯一性
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", [username])
            if cursor.fetchone()[0] > 0:
                return JsonResponse({'error': '用户名已存在，请更换用户名'})

            cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", [email])
            if cursor.fetchone()[0] > 0:
                return JsonResponse({'error': '邮箱已存在，请更换邮箱'})

            # 插入新用户信息
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                [username, password, email]
            )
        return JsonResponse({'success': '注册成功'})
    return JsonResponse({'error': '请求方式错误'}, status=400)


@api_view(['POST'])
def search_product(request):

    return True


