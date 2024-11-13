import random

import pymysql
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection  # 用于执行原始 SQL 查询
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pyquery import PyQuery as pq
from selenium.webdriver.chrome.options import Options

# 登录处理函数
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", [username, password])
        user = cursor.fetchone()
    if user:
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
    return Response({'message': '注册成功'})

from django.core.mail import send_mail
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
    username = request.data.get('data')

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
                return JsonResponse({'success': False, 'message': '用户名和喜好不能为空'})

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

# # 修复 ChromeOptions 错误
# options = Options()  # 使用 Options 替代 ChromeOptions
# options.add_experimental_option("excludeSwitches", ['enable-automation'])
# options.add_argument("--disable-blink-features=AutomationControlled")  # 模拟人类用户行为
# # MySQL 数据库连接配置,根据自己的本地数据库修改
# db_config = {
#     'host': 'localhost',
#     'port': 3306,
#     'user': 'root',
#     'password': 'kSY13630945535',
#     'database': 'django',
#     'charset': 'utf8mb4',
# }
#
# # 创建 MySQL 连接对象
# conn = pymysql.connect(**db_config)
# cursor = conn.cursor()
#
# # 把chrome设为selenium驱动的浏览器代理；
# driver = webdriver.Chrome(options=options)
# # 在页面加载之前，设置 navigator.webdriver 为 undefined
# driver.execute_cdp_cmd(
#     "Page.addScriptToEvaluateOnNewDocument",
#     {
#         "source": """
#         Object.defineProperty(navigator, 'webdriver', {
#             get: () => undefined
#         });
#         """
#     }
# )
# # 窗口最大化
# driver.maximize_window()
#
# def save_to_mysql(result):
#     try:
#         # 获取表名
#         table_name = 'wyh'
#         # 生成 SQL 语句
#         sql = f"INSERT INTO {table_name} (price, deal, title, shop, location, postFree, product_url, img_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#         print(sql)
#         cursor.execute(sql, (
#             result['price'],
#             result['deal'],
#             result['title'],
#             result['shop'],
#             result['location'],
#             result['isPostFree'],
#             result['product_url'],
#             result['img_url']
#         ))
#         conn.commit()
#         print(f'存储到MySQL成功: {result}')
#     except Exception as e:
#         print('存储到MySQL出错: ', result, e)
#
#
# # 修改下滑和上滑逻辑
# def human_like_scroll(direction="down", min_scroll=200, max_scroll=600, min_pause=1, max_pause=3):
#     """模仿人类行为进行缓慢的滑动。"""
#     scroll_length = random.randint(min_scroll, max_scroll)
#     scroll_pause = random.uniform(min_pause, max_pause)
#     if direction == "up":
#         scroll_length = -scroll_length  # 上滑设置为负数
#     driver.execute_script(f"window.scrollBy(0, {scroll_length});")
#     time.sleep(scroll_pause)  # 随机暂停
#
#
# def scroll_to_top():
#     """模仿人类缓慢地滑动到页面顶部。"""
#     current_position = driver.execute_script("return window.scrollY;")
#     while current_position > 0:
#         # 每次上滑一小段距离，模拟人类的缓慢滑动
#         scroll_amount = random.randint(100, 300)
#         driver.execute_script(f"window.scrollBy(0, {-scroll_amount});")
#         time.sleep(random.uniform(0.5, 1.5))  # 每次滑动后暂停
#         current_position = driver.execute_script("return window.scrollY;")
#     print("已返回页面顶部")
#
# def random_sleep(timeS, timeE):
#     # 生成一个S到E之间的随机等待时间
#     random_sleep_time = random.uniform(timeS, timeE)
#     time.sleep(random_sleep_time)
#
#
# # 搜索框查询函数
# @api_view(['POST'])
# def search(request):
#     searchQuery = request.data.get('searchQuery')
#     driver = webdriver.Chrome()
#     url = f"https://s.taobao.com/search?q={searchQuery}"
#     driver.get(url)
#     count = 1  # 从 data-spm=1 开始逐一抓取商品
#     # 循环点击“下一页”按钮，爬取多个页面
#     for page in range(5):
#         print(f"正在抓取第 {page + 1} 页内容...")
#         index = 1  # data-spm 从 1 开始
#         random_sleep(2, 4)  # 随机休眠模拟人类操作
#
#         start_time = time.time()  # 记录查找的开始时间
#
#         # 不断查找当前页面的数据
#         while True:
#             html = driver.page_source
#             doc = pq(html)
#             item = doc(f'a[data-spm="{index}"]')
#
#             if item:
#                 # 找到目标元素时可以对其进行操作
#                 print(f"找到 data-spm 为 {index} 的商品")
#                 # 提取商品信息
#                 title = item.find('.title--qJ7Xg_90 span').text()
#                 product_url = item.attr('href')
#
#                 # 等待图片 src 出现，如果没有出现则下滑页面
#                 img_url = None
#                 img_element = item.find('.mainPicWrapper--qRLTAeii img')
#                 max_wait_time = 5  # 最大等待时间（秒）
#                 wait_time = 0  # 当前等待时间
#
#                 while not img_url and wait_time < max_wait_time:
#                     img_url = img_element.attr('src')
#                     if not img_url:
#                         print(f"图片 src 未加载，等待 {wait_time + 1} 秒后再尝试...")
#                         time.sleep(1)
#                         # 随机下滑像素
#                         scroll_pixels = random.randint(400, 600)
#                         driver.execute_script(f"window.scrollBy(0, {scroll_pixels});")
#                         wait_time += 1
#                         html = driver.page_source
#                         doc = pq(html)
#                         item = doc(f'a[data-spm="{index}"]')  # 更新 item 元素
#                         img_element = item.find('.mainPicWrapper--qRLTAeii img')  # 重新获取图片元素
#
#                 if not img_url:  # 如果图片 src 依然未加载，则设置为空
#                     img_url = ''
#
#                 try:
#                     # 提取价格，支持包含非数字字符的情况
#                     price_int = item.find('.priceInt--yqqZMJ5a').text() or ""
#                     price_float = item.find('.priceFloat--XpixvyQ1').text() or ""
#
#                     # 拼接 price 为字符串
#                     price = f"{price_int}.{price_float}" if price_float else price_int
#
#                     # 如果价格中有两个连续的小数点，则去掉一个
#                     if '..' in price:
#                         price = price.replace('..', '.')
#
#                     print(f"处理后的价格: {price}")
#
#                 except Exception as e:
#                     print(f"价格处理错误: {e}")
#                     price = ""
#
#                 # 其他信息
#                 deal = item.find('.realSales--XZJiepmt').text()
#                 location = item.find('.procity--wlcT2xH9').text()
#                 shop = item.find('.shopInfo--Kmh31boz').text().replace("旺旺在线", "").strip()  # 去除旺旺在线
#                 # 检查 subIconWrapper--V18zAdQn 的 title 属性中是否包含“包邮”
#                 post_icon = item.find('.subIconWrapper--Vl8zAdQn ')
#                 post_text = post_icon.attr('title') if post_icon else ""
#                 print(post_text)
#                 isPostFree = 1 if "包邮" in post_text else 0
#
#                 # 构建商品数据字典
#                 product = {
#                     'title': title,
#                     'price': price,
#                     'deal': deal,
#                     'location': location,
#                     'shop': shop,
#                     'isPostFree': isPostFree,
#                     'product_url': product_url,
#                     'img_url': img_url
#                 }
#
#                 # 调用写入数据库的函数
#                 save_to_mysql(product)
#
#                 print(f"商品 {index} 已成功抓取并保存到数据库：{product}")
#                 index += 1  # 商品计数器
#
#                 # 当达到 100 个商品时退出抓取
#                 if count >= 101:
#                     break
#                 if index >= 101:
#                     break
#             else:
#                 # 未找到元素时进行下滑，检查是否超时
#                 if time.time() - start_time > 5:
#                     print("超过 5 秒未找到 data-spm 元素，跳转到下一页")
#                     next_button = WebDriverWait(driver, 10).until(
#                         EC.element_to_be_clickable(
#                             (By.CSS_SELECTOR, ".next-btn.next-medium.next-btn-normal.next-pagination-item.next-next"))
#                     )
#                     time.sleep(2)
#                     if next_button:
#                         next_button.click()
#                         print(f"已点击第 {page + 1} 页的“下一页”按钮")
#                         count += index
#                         time.sleep(3)  # 确保页面加载
#                         break  # 跳出当前页面的查找循环
#                     else:
#                         print("未找到‘下一页’按钮，结束爬取")
#
#                 print(f"未找到 data-spm 为 {index} 的商品，正在下滑页面...")
#                 human_like_scroll(direction="down")  # 调用模拟人类下滑的函数
#                 time.sleep(1)  # 等待页面加载
#                 # 更新页面HTML并再次检查目标元素
#                 html = driver.page_source
#                 doc = pq(html)
#                 item = doc(f'a[data-spm="{index}"]')
#
#     # 关闭浏览器
#     driver.quit()


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