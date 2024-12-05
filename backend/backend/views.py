import random
import jieba
import matplotlib.pyplot as plt
import pymysql
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection  # 用于执行原始 SQL 查询
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from selenium.common.exceptions import NoSuchElementException
from django.core.mail import send_mail
import urllib
from pyquery import PyQuery as pq
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import re  # 用于提取价格中的数字
from urllib.parse import urljoin, urlparse, urlencode, parse_qs
from datetime import datetime
from django.conf import settings


@api_view(['POST'])
def newChangedGoods(request):
    # 从前端获取 username 参数
    username = request.data.get('username')
    if not username:
        return JsonResponse({'error': 'Username is required'}, status=400)
    all_products = []
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM star_goods where username = %s and ifSeen = 0""", [username])
        products = cursor.fetchall()
        # 格式化商品数据
        for product in products:
            if isinstance(product[9], datetime):  # 检查是否是 datetime 对象
                update_date = product[9].strftime('%Y-%m-%d %H:%M:%S')  # 将 DATETIME 转换为字符串
            else:
                update_date = None  # 如果不是 datetime 对象，返回 None
            product_info = {
                "id": product[0],
                "title": product[3],
                "price": product[1],
                "deal": product[2],
                "shop": product[4],
                "location": product[5],
                "postFree": product[6],
                "product_url": product[7],
                "img_url": product[8],
                "update_date":update_date
            }
            all_products.append(product_info)
    with connection.cursor() as cursor:
        cursor.execute("""UPDATE star_goods set ifSeen = 1 where username = %s""", [username])
    # 返回所有商品数据
    return Response({
        "total_products": len(all_products),
        "goods": all_products
    })

@api_view(['POST'])
def oldChangedGoods(request):
    # 从前端获取 username 参数
    username = request.data.get('username')
    if not username:
        return JsonResponse({'error': 'Username is required'}, status=400)
    all_products = []
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM star_goods where username = %s and ifSeen = 1""", [username])
        products = cursor.fetchall()
        # 格式化商品数据
        for product in products:
            # 如果 product[9] 是 datetime 类型
            if isinstance(product[9], datetime):  # 检查是否是 datetime 对象
                update_date = product[9].strftime('%Y-%m-%d %H:%M:%S')  # 将 DATETIME 转换为字符串
            else:
                update_date = None  # 如果不是 datetime 对象，返回 None
            product_info = {
                "id": product[0],
                "title": product[3],
                "price": product[1],
                "deal": product[2],
                "shop": product[4],
                "location": product[5],
                "postFree": product[6],
                "product_url": product[7],
                "img_url": product[8],
                "update_date":update_date
            }
            all_products.append(product_info)
    # 返回所有商品数据
    return Response({
        "total_products": len(all_products),
        "goods": all_products
    })


@api_view(['POST'])
def get_unseen_goods_count(request):
    # 从前端获取 username 参数
    username = request.data.get('username')

    if not username:
        return JsonResponse({'error': 'Username is required'}, status=400)

    # 执行数据库查询，查找 ifSeen = 0 且 username 匹配的记录数
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM star_goods 
            WHERE username = %s AND ifSeen = 0
        """, [username])
        count = cursor.fetchone()[0]
    print(count)
    # 返回结果给前端
    return JsonResponse({'unseen_count': count})

# 登录处理函数
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", [username, password])
        user = cursor.fetchone()
    if user:
        # 用户存在，删除当前文件夹下的cookie文件
        cookie_file = os.path.join(os.getcwd(), f'cookie_jingdong_{username}.txt')  # 获取当前工作目录
        if os.path.exists(cookie_file):
            os.remove(cookie_file)
        cookie_file = os.path.join(os.getcwd(), f'cookie_manmanbuy_{username}.txt')  # 获取当前工作目录
        if os.path.exists(cookie_file):
            os.remove(cookie_file)
        cookie_file = os.path.join(os.getcwd(), f'cookie_taobao_{username}.txt')  # 获取当前工作目录
        if os.path.exists(cookie_file):
            os.remove(cookie_file)
        cookie_file = os.path.join(os.getcwd(), f'cookie_weipinhui_{username}.txt')  # 获取当前工作目录
        if os.path.exists(cookie_file):
            os.remove(cookie_file)
        return Response({'message': '登录成功', 'token': username})
    else:
        return Response({'message': '登录失败，用户名或密码错误，或者账号不存在'})


@api_view(['POST'])
def register_user(request):

    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if len(username) < 6:
        return Response({'message': '用户名要大于等于六字节'})
    if len(password) < 6:
        return Response({'message': '密码要大于等于六字节'})
    if(len(email) <= 0):
        return Response({'message': '邮箱不能为空'})

    # 检查用户名和邮箱的唯一性
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", [username])
        if cursor.fetchone()[0] > 0:
            return Response({'message': '用户名已存在，请更换用户名'})

        cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", [email])
        if cursor.fetchone()[0] > 0:
            return Response({'message': '邮箱已存在，请更换邮箱'})

        # 插入新用户信息
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
            [username, password, email]
        )

        # 检查用户名和邮箱的唯一性
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO UserApps (username, UserApps) VALUES (%s, 'taobao')",
                [username]
            )
    return Response({'message': '注册成功'})


@api_view(['POST'])
def send_sms_code(request):
    """
    发送邮箱验证码
    :param to_email: 发到这个邮箱
    :return: 成功：0 失败 -1
    """
    to_email = request.data.get('to_email')  # 确保参数名与前端一致
    sms_code = '%06d' % random.randint(0, 999999)
    EMAIL_FROM = "2519639200@qq.com"  # 邮件发送方
    email_title = '邮箱激活'
    email_body = "您的邮箱注册验证码为：{0}，该验证码有效时间为两分钟，请及时进行验证。".format(sms_code)

    send_status = send_mail(email_title, email_body, EMAIL_FROM, [to_email])

    return Response({'ifsend': send_status, 'sms_code': sms_code})


# 类别到表的映射
category_to_table = {
    '电脑': 'Computer',
    '配件': 'Accessories',
    '办公': 'Office',
    '文具': 'Stationery',
    '工业': 'Industrial',
    '商业': 'Business',
    '农业': 'Agriculture',
    '家电': 'HomeAppliance',
    '手机': 'MobilePhone',
    '通信': 'Telecom',
    '数码': 'Digital',
    '家具': 'Furniture',
    '家装': 'HomeDecoration',
    '家居': 'HomeLiving',
    '厨具': 'Kitchenware',
    '女装': 'WomenClothing',
    '男装': 'MenClothing',
    '内衣': 'Underwear',
    '配饰': 'Accessories',
    '女鞋': 'WomenShoes',
    '男鞋': 'MenShoes',
    '运动': 'Sports',
    '户外': 'Outdoor',
    '汽车': 'Automobile',
    '珠宝': 'Jewelry',
    '文玩': 'Collectibles',
    '箱包': 'Luggage',
    '食品': 'Food',
    '生鲜': 'FreshFood',
    '酒类': 'Alcohol',
    '健康': 'Health',
    '母婴': 'MotherBaby',
    '童装': 'KidsClothing',
    '玩具': 'Toys',
    '宠物': 'Pets',
    '美妆': 'Beauty',
    '个户': 'Personal',
    '家清': 'Household',
    '香氛': 'Fragrance',
    '娱乐': 'Entertainment',
    '图书': 'Books',
    '乐器': 'MusicalInstruments',
    '鲜花': 'Flowers'
}


@api_view(['POST'])
def get_goods(request):
    username = request.data.get('username')

    if not username:
        return Response({"error": "Username is required"}, status=400)

    # 查找用户的喜好类别
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT category FROM user_preferences WHERE username = %s
        """, [username])
        categories = cursor.fetchall()

    if not categories:
        return Response({"error": "No preferences found for this user"}, status=404)

    # 获取每个类别的商品信息
    all_products = []

    for category_tuple in categories:
        category = category_tuple[0]
        table_name = category_to_table.get(category)

        if table_name:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table_name}")
                products = cursor.fetchall()

                # 格式化商品数据
                for product in products:
                    product_info = {
                        "id": product[0],
                        "title": product[3],
                        "price": product[1],
                        "deal": product[2],
                        "shop": product[4],
                        "location": product[5],
                        "postFree": product[6],
                        "product_url": product[7],
                        "img_url": product[8]
                    }
                    all_products.append(product_info)
    # 随机打乱商品列表
    random.shuffle(all_products)
    # 返回所有商品数据
    return Response({
        "total_products": len(all_products),
        "goods": all_products
    })

@api_view(['POST'])
def get_preferrence_goods(request):
    username = request.data.get('username')
    all_products = []
    try:
        # 插入数据
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select * from star_goods where username = %s
                """,
                [username]
            )
            products = cursor.fetchall()
        # 格式化商品数据
        for product in products:
            product_info = {
                "id": product[0],
                "title": product[3],
                "price": product[1],
                "deal": product[2],
                "shop": product[4],
                "location": product[5],
                "postFree": product[6],
                "product_url": product[7],
                "img_url": product[8]
            }
            all_products.append(product_info)
        # 返回所有商品数据
        return Response({
            "total_products": len(all_products),
            "goods": all_products
        })
    except Exception as e:
        return JsonResponse({'message': '数据库错误', 'error': str(e)}, status=500)

# 获取用户是否已有喜好
@api_view(['POST'])
def check_user_preferences(request):
    username = request.data.get('username')
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT category FROM user_preferences WHERE username = %s
        """, [username])
        preferences = cursor.fetchall()

    # 返回用户喜好
    if preferences:
        categories = [item[0] for item in preferences]
        return JsonResponse({'has_preferences': True, 'preferences': categories})
    else:
        return JsonResponse({'has_preferences': False})


# 保存用户喜好
@api_view(['POST'])
def save_user_preferences(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            preferences = data.get('preferences')

            if not username or not preferences:
                return JsonResponse({'success': False, 'message': '喜好不能为空'})

            # 验证类别是否在允许的类别内
            allowed_categories = [
                '电脑', '配件', '办公', '文具', '工业', '商业', '农业', '家电', '手机', '通信',
                '数码', '家具', '家装', '家居', '厨具', '女装', '男装', '内衣', '配饰', '女鞋', '男鞋',
                '运动', '户外', '汽车', '珠宝', '文玩', '箱包', '食品', '生鲜', '酒类', '健康', '母婴',
                '童装', '玩具', '宠物', '美妆', '个户', '家清', '香氛', '娱乐', '图书', '乐器', '鲜花'
            ]

            invalid_preferences = [pref for pref in preferences if pref not in allowed_categories]
            if invalid_preferences:
                return JsonResponse({'success': False, 'message': f'无效的喜好类别: {", ".join(invalid_preferences)}'})
            # 清除原有喜好，保存新的喜好
            with connection.cursor() as cursor:
                # 首先删除该用户之前的所有喜好记录
                cursor.execute("DELETE FROM user_preferences WHERE username = %s", [username])

                # 插入新的喜好记录
                for pref in preferences:
                    cursor.execute("""
                        INSERT INTO user_preferences (username, category)
                        VALUES (%s, %s)
                    """, [username, pref])

            return JsonResponse({'success': True, 'message': '喜好保存成功'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'保存失败: {str(e)}'})
    else:
        return JsonResponse({'success': False, 'message': '请求方法错误'})

@api_view(['POST'])
def change_preferences(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        preferences = data.get('preferences')

        if not username or not preferences:
            return JsonResponse({'success': False, 'message': '喜好不能为空'})

        # 验证类别是否在允许的类别内
        allowed_categories = [
            '电脑', '配件', '办公', '文具', '工业', '商业', '农业', '家电', '手机', '通信',
            '数码', '家具', '家装', '家居', '厨具', '女装', '男装', '内衣', '配饰', '女鞋', '男鞋',
            '运动', '户外', '汽车', '珠宝', '文玩', '箱包', '食品', '生鲜', '酒类', '健康', '母婴',
            '童装', '玩具', '宠物', '美妆', '个户', '家清', '香氛', '娱乐', '图书', '乐器', '鲜花'
        ]

        invalid_preferences = [pref for pref in preferences if pref not in allowed_categories]
        if invalid_preferences:
            return JsonResponse({'success': False, 'message': f'无效的喜好类别: {", ".join(invalid_preferences)}'})
        # 清除原有喜好，保存新的喜好
        with connection.cursor() as cursor:
            # 首先删除该用户之前的所有喜好记录
            cursor.execute("DELETE FROM user_preferences WHERE username = %s", [username])

            # 插入新的喜好记录
            for pref in preferences:
                cursor.execute("""
                    INSERT INTO user_preferences (username, category)
                    VALUES (%s, %s)
                """, [username, pref])

        return JsonResponse({'success': True, 'message': '喜好保存成功'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'保存失败: {str(e)}'})

@api_view(['GET'])
def fetchAppImages(request):
    try:
        # 从 APP_img 表中查询所有应用名称和图片 URL
        with connection.cursor() as cursor:
            cursor.execute("SELECT appname, img_url FROM APP_img")
            rows = cursor.fetchall()

        # 将查询结果格式化为 JSON 结构
        app_images = [{'appname': row[0], 'img_url': row[1]} for row in rows]
        print(app_images)

        return JsonResponse({'success': True, 'appImages': app_images})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'获取应用图片失败: {str(e)}'})

@api_view(['POST'])
def searchIfStarred(request):
    username = request.data.get('username')
    product_url = request.data.get('product_url')

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM star_goods WHERE username = %s AND product_url = %s",
                (username, product_url)
            )
            result = cursor.fetchone()
        if result is None:
            return JsonResponse({'isStarred': False})
        return JsonResponse({'isStarred': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': '数据库错误', 'details': str(e)}, status=500)

@api_view(['POST'])
def change_password(request):
    username = request.data.get('username')
    oldpassword = request.data.get('oldpassword')
    newpassword = request.data.get('newpassword')

    if not username or not oldpassword or not newpassword:
        return JsonResponse({'success': False, 'message': '缺少必要字段'}, status=400)

    try:
        # 验证原密码
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, oldpassword)
            )
            result = cursor.fetchone()
        if result is None:
            return JsonResponse({'success': False, 'message': '原密码错误'}, status=400)

        # 更新密码
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET password = %s WHERE username = %s",
                (newpassword, username)
            )
        return JsonResponse({'success': True, 'message': '修改密码成功'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': '数据库错误', 'details': str(e)}, status=500)

@api_view(['POST'])
def star_goods(request):
    username = request.data.get('username')
    product = request.data.get('product')
    price = product.get('price')
    deal = product.get('deal')
    title = product.get('title')
    shop = product.get('shop')
    location = product.get('location')
    postFree = product.get('postFree')
    product_url = product.get('product_url')
    img_url = product.get('img_url')
    try:
        # 验证原密码
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO star_goods (username, price, deal, title, shop, location, postFree, product_url, img_url, update_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                """,
                [username, price, deal, title, shop, location, postFree, product_url, img_url]
            )
        return JsonResponse({'message': ''})
    except Exception as e:
        return JsonResponse({'success': False, 'message': '数据库错误', 'details': str(e)}, status=500)

@api_view(['POST'])
def unstar_goods(request):
    username = request.data.get('username')
    product = request.data.get('product')
    price = product.get('price')
    deal = product.get('deal')
    title = product.get('title')
    shop = product.get('shop')
    location = product.get('location')
    postFree = product.get('postFree')
    product_url = product.get('product_url')
    img_url = product.get('img_url')
    try:
        # 验证原密码
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM star_goods
                WHERE username = %s AND product_url = %s
                """,
                [username, product_url]
            )
        return JsonResponse({'message': ''})
    except Exception as e:
        return JsonResponse({'success': False, 'message': '数据库错误', 'details': str(e)}, status=500)



@api_view(['POST'])
def search(request):
    username = request.data.get('username')
    searchQuery = request.data.get('searchQuery')
    goods = []
    words = jieba.lcut(searchQuery)  # 返回一个列表
    print("分词结果:", words)
    # 如果需要用空格连接分词结果
    searchQuery = " ".join(words)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT app FROM UserApps WHERE username = %s", [username])
            result = cursor.fetchone()

        if result:
            if(result[0] == 'taobao'):
                # 配置Selenium选项
                options = Options()
                options.add_experimental_option("excludeSwitches", ['enable-automation'])
                driver = webdriver.Chrome(options=options)
                driver.maximize_window()
                wait = WebDriverWait(driver, 15)
                """抓取商品信息"""
                encoded_keyword = urllib.parse.quote(searchQuery)
                base_url = f"https://uland.taobao.com/sem/tbsearch?clk1=b27114e13eaf50a5b4b3472c3265ec77&keyword={encoded_keyword}&localImgKey=&q={encoded_keyword}&refpid=mm_2898300158_3078300397_115665800437&tab=all&upsId=b27114e13eaf50a5b4b3472c3265ec77"
                page = 1
                total_count = 0  # 用于统计已抓取的商品数

                while total_count < 1:  # 限制总共抓取 1000 个商品
                    url = f"{base_url}&page={page}"
                    print(f"正在抓取第 {page} 页: {url}")
                    driver.get(url)
                    count = 1  # 每页商品从 data-spm=1 开始

                    while total_count < 1000:  # 每页抓取商品
                        html = driver.page_source
                        doc = pq(html)
                        item = doc(f'a[data-spm="{count}"]')

                        if not item:
                            print(f"未找到商品 {count}，滚动页面加载...")
                            driver.execute_script("window.scrollBy(0, 600);")
                            time.sleep(0.5)
                            html = driver.page_source
                            doc = pq(html)
                            item = doc(f'a[data-spm="{count}"]')
                            if not item:
                                print("到达页面底部")
                                break  # 跳出当前页面的循环，尝试下一页

                        try:
                            # 提取商品信息
                            title = item.find('.Title--title--jCOPvpf').text()
                            product_url = item.attr('href')
                            img_url = item.find('img').attr('src') or ''
                            price_int = item.find('.Price--priceInt--ZlsSi_M').text() or "0"
                            price_float = item.find('.Price--priceFloat--h2RR0RK').text() or "00"
                            price = f"{price_int}.{price_float}"
                            location = item.find('.Price--procity--_7Vt3mX').text()
                            shop = item.find('.ShopInfo--shopName--rg6mGmy').text()
                            post_text = item.find('.SalesPoint--subIconWrapper--s6vanNY').attr('title') or ""
                            isPostFree = 1 if "包邮" in post_text else 0

                            product = {
                                'title': title,
                                'price': price,
                                'location': location,
                                'shop': shop,
                                'isPostFree': isPostFree,
                                'product_url': product_url,
                                'img_url': img_url
                            }
                            goods.append(product)
                            print(f"商品 {total_count + 1} 数据已保存: {product}")
                            total_count += 1

                        except Exception as e:
                            print(f"商品 {count} 抓取失败: {e}")

                        count += 1  # 尝试抓取下一个商品

                    if count <= 1:  # 如果第一页没有商品，则说明没有更多页面
                        print("未能获取任何商品，停止抓取。")
                        break

                    page += 1  # 切换到下一页
                    if page > 30:
                        break

                print(f"已抓取完成，总共抓取了 {total_count} 个商品。")
                driver.quit()
                return Response({
                    "total_goods": len(goods),
                    "goods": goods
                })
            elif (result[0] == 'jingdong'):
                # 配置Selenium选项
                options = Options()
                options.add_experimental_option("excludeSwitches", ['enable-automation'])
                driver = webdriver.Chrome(options=options)
                driver.maximize_window()
                wait = WebDriverWait(driver, 15)
                """抓取商品信息"""
                base_url = f"https://re.jd.com/search?keyword={searchQuery}&enc=utf-8"
                page = 1
                total_count = 0  # 用于统计已抓取的商品数

                while total_count < 1000:  # 限制总共抓取 1000 个商品
                    url = f"{base_url}&page={page}"
                    print(url)
                    print(f"正在抓取第 {page} 页: {url}")
                    driver.get(url)

                    time.sleep(3)  # 等待页面加载
                    html = driver.page_source
                    doc = pq(html)

                    # 提取每个商品信息
                    items = doc('.li_cen').items()
                    for item in items:
                        try:
                            # 提取商品信息
                            title = item.find('.commodity_tit').text()
                            product_url = item.find('.pic a').attr('href')
                            if product_url and not product_url.startswith("http"):
                                product_url = "https:" + product_url

                            img_url = item.find('.pic img.img_k').attr('src') or ''
                            if img_url and not img_url.startswith("http"):
                                img_url = "https:" + img_url

                            price = item.find('.price').text().replace('¥', '').strip() or "0"
                            isPostFree = 1  # 假设所有商品包邮（可以根据实际逻辑修改）
                            shop = "京东商城"  # 假设来源固定为京东
                            location = "未知"  # 网页中未提供位置字段

                            product = {
                                'title': title,
                                'price': price,
                                'location': location,
                                'shop': shop,
                                'isPostFree': isPostFree,
                                'product_url': product_url,
                                'img_url': img_url
                            }
                            goods.append(product)
                            print(f"商品 {total_count + 1} 数据已保存: {product}")
                            total_count += 1

                            if total_count >= 1000:
                                break  # 达到抓取限制，停止

                        except Exception as e:
                            print(f"商品抓取失败: {e}")

                    page += 1  # 切换到下一页
                    if page > 30:
                        break

                print(f"已抓取完成，总共抓取了 {total_count} 个商品。")
                driver.quit()
                return Response({
                    "total_goods": len(goods),
                    "goods": goods
                })
            elif (result[0] == 'weipinhui'):
                # 配置Selenium选项
                options = Options()
                options.add_experimental_option("excludeSwitches", ['enable-automation'])
                driver = webdriver.Chrome(options=options)
                driver.maximize_window()
                wait = WebDriverWait(driver, 15)
                print("开始抓取商品信息...")
                weipinhui_url = 'https://passport.vip.com/login?src=https%3A%2F%2Fcategory.vip.com%2Fsuggest.php%3Fkeyword%3D%25E7%258E%25A9%25E5%2585%25B7%26ff%3D235%257C12%257C1%257C1%26page%3D10%26tfs_url%3D%252F%252Fmapi.vip.com%252Fvips-mobile%252Frest%252Fshopping%252Fpc%252Fsearch%252Fproduct%252Frank'
                cookie_file_weipinhui = f'cookie_weipinhui_{username}.txt'
                if not os.path.exists(cookie_file_weipinhui):
                    driver.get(weipinhui_url)
                    # 等待手动登录完成
                    time.sleep(60)
                    # 获取当前的 cookies 并保存到文件
                    cookies = driver.get_cookies()
                    with open(cookie_file_weipinhui, 'w') as f:
                        json.dump(cookies, f)
                    print("Cookies 已保存到文件：cookie_file_weipinhui.txt")
                else:
                    print("cookie_file_weipinhui.txt 已存在，跳过登录步骤。")
                    driver.get(weipinhui_url)
                    with open(cookie_file_weipinhui, 'r') as f:
                        cookies = json.load(f)
                    for cookie in cookies:
                        driver.add_cookie(cookie)

                base_url = f"https://category.vip.com/suggest.php?keyword={searchQuery}"
                page = 1
                total_count = 0  # 统计已抓取的商品数

                while total_count < 1000:  # 限制总共抓取 1000 个商品
                    url = f"{base_url}&page={page}"
                    print(f"正在抓取第 {page} 页: {url}")
                    driver.get(url)
                    time.sleep(3)  # 等待页面加载

                    # 解析页面 HTML
                    html = driver.page_source
                    doc = pq(html)

                    # 提取商品信息
                    items = doc('.c-goods-item').items()
                    for item in items:
                        try:
                            # 提取标题
                            title = (
                                    item.find('.c-goods-item_name').text() or
                                    item.find('.J-goods-item__img').attr('alt') or
                                    '未知商品'
                            ).strip()

                            # 提取价格
                            price = (
                                    item.find('.c-goods-item__sale-price').text() or "0"
                            ).replace('¥', '').strip()

                            # 提取商品链接
                            product_url = item.find('a').attr('href')
                            if product_url and not product_url.startswith("http"):
                                product_url = "https:" + product_url

                            # 提取图片链接
                            img_url = item.find('.J-goods-item__img').attr('data-original') or item.find(
                                '.J-goods-item_img').attr('src')
                            if img_url and not img_url.startswith("http"):
                                img_url = "https:" + img_url

                            # 设置包邮信息为 0（未提供包邮信息）
                            isPostFree = 0

                            # 设置店铺和位置默认值
                            shop = "唯品会"
                            location = "未知"

                            # 组合商品信息
                            product = {
                                'title': title,
                                'price': price,
                                'location': location,
                                'shop': shop,
                                'isPostFree': isPostFree,
                                'product_url': product_url,
                                'img_url': img_url
                            }
                            goods.append(product)
                            print(f"商品 {total_count + 1} 数据已保存: {product}")
                            total_count += 1

                            if total_count >= 1000:
                                break  # 达到抓取限制，停止

                        except Exception as e:
                            print(f"商品抓取失败: {e}")

                    page += 1  # 切换到下一页
                    if page > 30:
                        break

                print(f"已抓取完成，总共抓取了 {total_count} 个商品。")
                driver.quit()
            return Response({
                "total_goods": len(goods),
                "goods": goods
            })
        else:
            return Response({'error': 'Username not found'}, status=404)
    except Exception as e:
        # 捕获并返回错误信息
        return Response({'error': 'Database error', 'details': str(e)}, status=500)
# 找到价格最小的商品
def find_cheapest_good(goods_list, source):
    """将价格最小的商品与来源封装"""
    cheapest = None
    for item in goods_list:
        try:
            price = float(item['price'])  # 转换为浮点数
            if cheapest is None or price < cheapest['price']:
                cheapest = {
                    'good': item,
                    'price': price,
                    'source': source
                }
        except ValueError:
            print(f"商品价格无法转换为数字: {item['price']}")
    return cheapest
@api_view(['POST'])
def price_compare(request):
    searchQuery = request.data.get('searchQuery')
    username = request.data.get('username')
    goods_taobao = []
    goods_jingdong = []
    goods_weipinhui = []
    try:
        options = Options()
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        wait = WebDriverWait(driver, 5)
        """抓取商品信息"""
        encoded_keyword = urllib.parse.quote(searchQuery)
        base_url = f"https://uland.taobao.com/sem/tbsearch?clk1=b27114e13eaf50a5b4b3472c3265ec77&keyword={encoded_keyword}&localImgKey=&q={encoded_keyword}&refpid=mm_2898300158_3078300397_115665800437&tab=all&upsId=b27114e13eaf50a5b4b3472c3265ec77"
        page = 1
        total_count = 0  # 用于统计已抓取的商品数

        while total_count < 10:
            url = f"{base_url}&page={page}"
            print(f"正在抓取第 {page} 页: {url}")
            driver.get(url)
            count = 1  # 每页商品从 data-spm=1 开始

            while total_count < 10:  # 每页抓取商品
                html = driver.page_source
                doc = pq(html)
                item = doc(f'a[data-spm="{count}"]')

                if not item:
                    print(f"未找到商品 {count}，滚动页面加载...")
                    driver.execute_script("window.scrollBy(0, 600);")
                    time.sleep(0.5)
                    html = driver.page_source
                    doc = pq(html)
                    item = doc(f'a[data-spm="{count}"]')
                    if not item:
                        print("到达页面底部")
                        break  # 跳出当前页面的循环，尝试下一页

                try:
                    # 提取商品信息
                    title = item.find('.Title--title--jCOPvpf').text()
                    product_url = item.attr('href')
                    img_url = item.find('img').attr('src') or ''
                    price_int = item.find('.Price--priceInt--ZlsSi_M').text() or "0"
                    price_float = item.find('.Price--priceFloat--h2RR0RK').text() or "00"
                    price = f"{price_int}.{price_float}".replace("..", ".")
                    location = item.find('.Price--procity--_7Vt3mX').text()
                    shop = item.find('.ShopInfo--shopName--rg6mGmy').text()
                    post_text = item.find('.SalesPoint--subIconWrapper--s6vanNY').attr('title') or ""
                    isPostFree = 1 if "包邮" in post_text else 0

                    product = {
                        'title': title,
                        'price': price,
                        'location': location,
                        'shop': shop,
                        'isPostFree': isPostFree,
                        'product_url': product_url,
                        'img_url': img_url
                    }
                    if "?" not in price:
                        goods_taobao.append(product)
                        print(f"商品 {total_count + 1} 数据已保存: {product}")
                        total_count += 1

                except Exception as e:
                    print(f"商品 {count} 抓取失败: {e}")

                count += 1  # 尝试抓取下一个商品

            if count <= 1:  # 如果第一页没有商品，则说明没有更多页面
                print("未能获取任何商品，停止抓取。")
                break

            page += 1  # 切换到下一页
            if page > 30:
                break

        print(f"已抓取完成，总共抓取了 {total_count} 个商品。")

        """抓取商品信息"""
        base_url = f"https://re.jd.com/search?keyword={searchQuery}&enc=utf-8"
        page = 1
        total_count = 0  # 用于统计已抓取的商品数

        while total_count < 10:  # 限制总共抓取 1000 个商品
            url = f"{base_url}&page={page}"
            print(url)
            print(f"正在抓取第 {page} 页: {url}")
            driver.get(url)

            time.sleep(3)  # 等待页面加载
            html = driver.page_source
            doc = pq(html)

            # 提取每个商品信息
            items = doc('.li_cen').items()
            for item in items:
                try:
                    # 提取商品信息
                    title = item.find('.commodity_tit').text()
                    product_url = item.find('.pic a').attr('href')
                    if product_url and not product_url.startswith("http"):
                        product_url = "https:" + product_url

                    img_url = item.find('.pic img.img_k').attr('src') or ''
                    if img_url and not img_url.startswith("http"):
                        img_url = "https:" + img_url

                    price = item.find('.price').text().replace('￥', '').strip() or "0"
                    isPostFree = 1  # 假设所有商品包邮（可以根据实际逻辑修改）
                    shop = "京东商城"  # 假设来源固定为京东
                    location = "未知"  # 网页中未提供位置字段

                    product = {
                        'title': title,
                        'price': price,
                        'location': location,
                        'shop': shop,
                        'isPostFree': isPostFree,
                        'product_url': product_url,
                        'img_url': img_url
                    }
                    goods_jingdong.append(product)
                    print(f"商品 {total_count + 1} 数据已保存: {product}")
                    total_count += 1

                    if total_count >= 10:
                        break  # 达到抓取限制，停止

                except Exception as e:
                    print(f"商品抓取失败: {e}")

            page += 1  # 切换到下一页
            if page > 30:
                break

        print(f"已抓取完成，总共抓取了 {total_count} 个商品。")
        print("开始抓取商品信息...")
        weipinhui_url = 'https://passport.vip.com/login?src=https%3A%2F%2Fcategory.vip.com%2Fsuggest.php%3Fkeyword%3D%25E7%258E%25A9%25E5%2585%25B7%26ff%3D235%257C12%257C1%257C1%26page%3D10%26tfs_url%3D%252F%252Fmapi.vip.com%252Fvips-mobile%252Frest%252Fshopping%252Fpc%252Fsearch%252Fproduct%252Frank'
        cookie_file_weipinhui = f'cookie_weipinhui_{username}.txt'
        if not os.path.exists(cookie_file_weipinhui):
            driver.get(weipinhui_url)
            # 等待手动登录完成
            time.sleep(60)
            # 获取当前的 cookies 并保存到文件
            cookies = driver.get_cookies()
            with open(cookie_file_weipinhui, 'w') as f:
                json.dump(cookies, f)
            print("Cookies 已保存到文件：cookie_file_weipinhui.txt")
        else:
            print("cookie_file_weipinhui.txt 已存在，跳过登录步骤。")
            driver.get(weipinhui_url)
            with open(cookie_file_weipinhui, 'r') as f:
                cookies = json.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)

        base_url = f"https://category.vip.com/suggest.php?keyword={searchQuery}"
        page = 1
        total_count = 0  # 统计已抓取的商品数

        while total_count < 10:  # 限制总共抓取 10 个商品
            url = f"{base_url}&page={page}"
            print(f"正在抓取第 {page} 页: {url}")
            driver.get(url)
            time.sleep(3)  # 等待页面加载

            # 解析页面 HTML
            html = driver.page_source
            doc = pq(html)

            # 提取商品信息
            items = doc('.c-goods-item').items()
            for item in items:
                try:
                    # 提取标题
                    title = (
                            item.find('.c-goods-item_name').text() or
                            item.find('.J-goods-item__img').attr('alt') or
                            '未知商品'
                    ).strip()

                    # 提取价格
                    price = (
                            item.find('.c-goods-item__sale-price').text() or "0"
                    ).replace('¥', '').strip()

                    # 提取商品链接
                    product_url = item.find('a').attr('href')
                    if product_url and not product_url.startswith("http"):
                        product_url = "https:" + product_url

                    # 提取图片链接
                    img_url = item.find('.J-goods-item__img').attr('data-original') or item.find(
                        '.J-goods-item_img').attr('src')
                    if img_url and not img_url.startswith("http"):
                        img_url = "https:" + img_url

                    # 设置包邮信息为 0（未提供包邮信息）
                    isPostFree = 0

                    # 设置店铺和位置默认值
                    shop = "唯品会"
                    location = "未知"

                    # 组合商品信息
                    product = {
                        'title': title,
                        'price': price,
                        'location': location,
                        'shop': shop,
                        'isPostFree': isPostFree,
                        'product_url': product_url,
                        'img_url': img_url
                    }
                    goods_weipinhui.append(product)
                    print(f"商品 {total_count + 1} 数据已保存: {product}")
                    total_count += 1

                    if total_count >= 10:
                        break  # 达到抓取限制，停止

                except Exception as e:
                    print(f"商品抓取失败: {e}")

            page += 1  # 切换到下一页
            if page > 30:
                break

        print(f"已抓取完成，总共抓取了 {total_count} 个商品。")
        driver.quit()
        cheapest_goods = [
            find_cheapest_good(goods_taobao, '淘宝'),
            find_cheapest_good(goods_jingdong, '京东'),
            find_cheapest_good(goods_weipinhui, '唯品会')
        ]

        # 去掉空值并找到最便宜的商品
        cheapest_goods = [good for good in cheapest_goods if good is not None]
        if cheapest_goods:
            cheapest_good = min(cheapest_goods, key=lambda x: x['price'])
        else:
            cheapest_good = None
        cheapest_good_2 = []
        cheapest_good_2.append(cheapest_good['good'])
        return Response({
            "goods_taobao": goods_taobao,
            "goods_jingdong": goods_jingdong,
            "goods_weipinhui": goods_weipinhui,
            "cheapest_good": cheapest_good_2,
            "cheapest_good_source": cheapest_good['source']
        })
    except Exception as e:
        # 捕获并返回错误信息
        return Response({'error': 'Database error', 'details': str(e)}, status=500)

@api_view(['POST'])
def get_category(request):
    # 获取分类名称
    english_name = request.data.get('data')  # Use `data.get()` for POST data in DRF
    print(english_name)

    if not english_name:
        return Response({"error": "Category name is required"}, status=400)

    # 构建 SQL 查询
    table_name = english_name  # Assuming the table name corresponds directly to the category
    query = f"SELECT * FROM {table_name}"

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)  # Execute the SQL query
            goods = cursor.fetchall()

        # 商品数据转换为字典形式
        goods_list = []
        for item in goods:
            goods_dict = {
                "id": item[0],
                "title": item[3],
                "price": item[1],
                "deal": item[2],
                "shop": item[4],
                "location": item[5],
                "postFree": item[6],
                "product_url": item[7],
                "img_url": item[8]
            }
            goods_list.append(goods_dict)
        return Response({
            "total_goods": len(goods_list),
            "goods": goods_list
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)
@api_view(['POST'])
def starGood(request):

    return True

@api_view(['POST'])
def notStarGood(request):
    return True




# 获取历史价格数据并返回图表
@api_view(['POST'])
def fetchPriceData(request):
    shop = request.data.get('product_url')  # 使用 request.data 获取 POST 数据
    username = request.data.get('username')
    print(shop)
    # 修复相对路径并确保正确编码
    parsed_url = urlparse(shop)
    if not parsed_url.scheme:
        shop = urljoin("https:", shop)
        parsed_url = urlparse(shop)
    # 确保查询参数正确编码
    query_params = parse_qs(parsed_url.query)
    encoded_query = urlencode(query_params, doseq=True)
    shop = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{encoded_query}"

    # 打印修复后的 URL
    print("修复后的 URL:", shop)
    # 检查 cookie 文件是否存在
    cookie_file = f'cookie_manmanbuy_{username}.txt'

    # 设置 Chrome 启动选项
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 如果你想不打开浏览器界面，可以启用这一行
    # 禁用检测 WebDriver 的标志
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # 伪装 User-Agent
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 创建 WebDriver 实例
    driver = webdriver.Chrome(options=chrome_options)
    # 创建 WebDriver 实例
    Action = ActionChains(driver)
    # 在页面加载之前，设置 navigator.webdriver 为 undefined
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            """
        }
    )

    taobao_url = 'https://login.taobao.com/'
    cookie_file_taobao = f'cookie_taobao_{username}.txt'
    if not os.path.exists(cookie_file_taobao):
        driver.get(taobao_url)
        # 等待手动登录完成
        time.sleep(60)
        # 获取当前的 cookies 并保存到文件
        cookies = driver.get_cookies()
        with open(cookie_file_taobao, 'w') as f:
            json.dump(cookies, f)
        print("Cookies 已保存到文件：cookie_file_weipinhui.txt")
    else:
        print("cookie_file_taobao.txt 已存在，跳过登录步骤。")
        driver.get(taobao_url)
        with open(cookie_file_taobao, 'r') as f:
            cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)

    # jingdong_url = 'https://passport.jd.com/new/login.aspx'
    # cookie_file_jingdong = f'cookie_jingdong_{username}.txt'
    # if not os.path.exists(cookie_file_jingdong):
    #     driver.get(jingdong_url)
    #     # 等待手动登录完成
    #     time.sleep(60)
    #     # 获取当前的 cookies 并保存到文件
    #     cookies = driver.get_cookies()
    #     with open(cookie_file_jingdong, 'w') as f:
    #         json.dump(cookies, f)
    #     print("Cookies 已保存到文件：cookie_file_weipinhui.txt")
    # else:
    #     print("cookie_file_jingdong.txt 已存在，跳过登录步骤。")
    #     driver.get('https://www.jd.com/')
    #     with open(cookie_file_jingdong, 'r') as f:
    #         cookies = json.load(f)
    #     for cookie in cookies:
    #         driver.add_cookie(cookie)

    cookie_file_weipinhui = f'cookie_weipinhui_{username}.txt'
    weipinhui_url = 'https://passport.vip.com/login?src=https%3A%2F%2Fcategory.vip.com%2Fsuggest.php%3Fkeyword%3D%25E7%258E%25A9%25E5%2585%25B7%26ff%3D235%257C12%257C1%257C1%26page%3D10%26tfs_url%3D%252F%252Fmapi.vip.com%252Fvips-mobile%252Frest%252Fshopping%252Fpc%252Fsearch%252Fproduct%252Frank'
    if not os.path.exists(cookie_file_weipinhui):
        driver.get(weipinhui_url)
        # 等待手动登录完成
        time.sleep(60)
        # 获取当前的 cookies 并保存到文件
        cookies = driver.get_cookies()
        with open(cookie_file_weipinhui, 'w') as f:
            json.dump(cookies, f)
        print("Cookies 已保存到文件：cookie_file_weipinhui.txt")
    else:
        print("cookie_file_weipinhui.txt 已存在，跳过登录步骤。")
        driver.get(weipinhui_url)
        with open(cookie_file_weipinhui, 'r') as f:
            cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
    # 访问指定 URL
    driver.get(shop)
    time.sleep(10) # 验证
    # 获取页面的实际地址
    shop = driver.current_url
    print(shop)
    # 如果 cookie 文件不存在，则执行登录操作
    if not os.path.exists(cookie_file):
        # 启动浏览器并打开登录页面
        driver.get('https://home.manmanbuy.com/login.aspx')

        # 等待页面加载
        time.sleep(60)

        # 获取当前的 cookies 并保存到文件
        cookies = driver.get_cookies()
        with open(cookie_file, 'w') as f:
            json.dump(cookies, f)

        print("Cookies 已保存到文件：cookie_manmanbuy.txt")
    else:
        print("cookie_manmanbuy.txt 已存在，跳过登录步骤。")
        # 启动浏览器并打开登录页面
        driver.get('https://home.manmanbuy.com/login.aspx')

        # 等待页面加载
        time.sleep(2)
        # 读取保存的 cookies
        with open(cookie_file, 'r') as f:
            cookies = json.load(f)
        # 添加 cookies
        for cookie in cookies:
            driver.add_cookie(cookie)

    # 启动浏览器并打开历史最低价格页面
    driver.get(
        f'http://tool.manmanbuy.com/HistoryLowest.aspx')
    # 等待页面加载
    time.sleep(2)

    # 定位搜索框并清空内容
    search_box = driver.find_element(By.ID, "historykey")
    search_box.clear()

    # 将 shop 字符串插入搜索框
    search_box.send_keys(shop)
    time.sleep(2)  # 等待查询结果加载

    # 定位查询按钮并点击
    search_button = driver.find_element(By.ID, "searchHistory")
    search_button.click()
    time.sleep(2)  # 等待查询结果加载

    # 滑动到底部以确保所有数据加载完成
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    try:
        # 尝试查找 "暂未收录" 元素
        no_data_element = driver.find_element(By.XPATH, "//*[contains(text(), '暂未收录')]")
        if no_data_element:
            print("该商品未收录，停止图表查找操作。")
            driver.quit()
            return JsonResponse({'success': False, 'message': '暂未收录'})
    except NoSuchElementException:
        # 如果没有找到元素，继续执行后续代码
        print("未找到 '暂未收录' 元素，继续操作。")

    # 确定趋势图画布的容器位置
    canvas = driver.find_element(By.ID, "container")  # 根据容器 ID 定位
    canvas_location = canvas.location
    canvas_size = canvas.size

    # 爬取历史价格数据
    data = []

    # 设置画布范围并爬取数据
    for offset_x in range(-canvas_size['width'] // 2, canvas_size['width'] // 2, 36):
        Action.move_to_element(canvas).perform()
        Action.move_by_offset(offset_x, 0).perform()
        time.sleep(1)
        try:
            # 从趋势图中提取文本
            text_element = driver.find_element(By.XPATH,
                                               "//*[contains(@class, 'trend-box')]//div[contains(@style, 'position: absolute')]")
            text = text_element.text
            if text:  # 如果文本不为空
                first_space_index = text.find(' ')  # 找到第一个空格的位置
                if first_space_index != -1:
                    date = text[:first_space_index].strip()  # 提取日期部分
                    price_str = text[first_space_index + 1:].strip()  # 提取价格部分
                    # 如果日期中包含 "第一次收录"，则跳过当前数据
                    if "第一次收录" in date:
                        continue
                    # 提取价格中的数字部分
                    price_match = re.search(r'\d+(\.\d+)?', price_str)
                    if price_match:
                        price = float(price_match.group())  # 转为浮点数
                        data.append((date, price))  # 将日期和价格存储为元组
            with open('price.txt', 'a', encoding='utf-8') as f:
                f.write(text + '\n')
        except Exception as err:
            print(f"数据提取失败: {err}")

    # 关闭浏览器
    driver.quit()
    print("提取到的数据：")
    # 假设 `data` 是存储日期和价格的元组列表
    for i, entry in enumerate(data):
        # 修改 data 中的日期格式
        formatted_date = format_date(entry[0])  # 将日期格式化
        data[i] = (formatted_date, entry[1])  # 更新 data 中的日期部分
    for entry in data:
        print(f"日期: {entry[0]}, 价格: {entry[1]}")

    # 如果没有找到历史价格数据
    if not data:
        return JsonResponse({'success': False, 'message': '没有找到历史价格数据'})

    return JsonResponse({'success': True, 'data': data, 'message':''})

# 将日期从 "2024年8月20日" 格式转换为 "2024-8-20" 格式
def format_date(date_str):
    match = re.match(r"(\d{4})年(\d{1,2})月(\d{1,2})日", date_str)
    if match:
        year, month, day = match.groups()
        return f"{year}-{int(month)}-{int(day)}"
    return date_str  # 如果无法匹配，返回原始日期