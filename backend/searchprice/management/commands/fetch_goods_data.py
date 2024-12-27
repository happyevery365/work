# your_app/management/commands/fetch_goods_data.py
import threading
import time
from django.core.management.base import BaseCommand
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

# 发送邮箱验证码
EMAIL_HOST = "smtp.qq.com"     # 服务器
EMAIL_PORT = 25                 # 一般情况下都为25
EMAIL_HOST_USER = "2519639200@qq.com"     # 账号
EMAIL_HOST_PASSWORD = "ornbnlnvkcjmeabe"     # （上面保存的授权码）
EMAIL_USE_TLS = True       # 一般都为False
EMAIL_FROM = "2519639200@qq.com"      # 邮箱来自
email_title = '邮箱激活'

import re


# 用于去除单个价格中的重复数字（例如 '2297.11 2297.11'）
def remove_duplicates_from_price(price):
    # 用正则去除重复的数字，保留第一个
    price_parts = price.split()  # 假设价格是以空格分隔的
    unique_price = " ".join(sorted(set(price_parts), key=price_parts.index))  # 去重并保留顺序
    return unique_price


# 对 all_price 列表中的每个价格进行去重处理
def remove_duplicates_from_price_list(price_list):
    unique_prices = []  # 存储最终去重后的价格列表

    for price in price_list:
        # 如果价格是有效的（非 "未找到商品价格"）
        if price != "未找到商品价格":
            price = remove_duplicates_from_price(price)  # 去重处理
            unique_prices.append(price)
        else:
            unique_prices.append(price)

    return unique_prices
def extract_number(price_str):
    """从字符串中提取数字并返回"""
    match = re.search(r'\d+(\.\d+)?', price_str)
    if match:
        return float(match.group(0))  # 转换为浮动数字
    return 0  # 如果没有找到数字，返回 0

class Command(BaseCommand):  # 将类名改为 Command
    help = '每12小时从数据库中提取用户名和商品链接并更新商品价格'

    def handle(self, *args, **options):
        # 线程函数，每12小时执行一次
        def fetch_and_print():
            while True:
                print('开始新一次价格更新')
                with connection.cursor() as cursor:
                    cursor.execute("SELECT username, product_url, price, title FROM star_goods")
                    result = cursor.fetchall()

                    # 获取所有的product_url
                product_urls = [row[1] for row in result]
                # 调用get_product_price获取所有的价格
                price_list = self.get_product_price(product_urls)  # 返回的价格数组
                print('price_list', price_list)
                # 更新价格
                for idx, row in enumerate(result):
                    username = row[0]
                    product_url = row[1]
                    price = row[2]
                    title = row[3]
                    newprice = price_list[idx]  # 从price_list获取对应的价格

                    if newprice == "未找到商品价格":
                        continue
                    if price != newprice:
                        print(price)
                        print(newprice)
                        # 提取 newprice 和 price 中的数字
                        new_price_value = extract_number(newprice)
                        price_value = extract_number(price)

                        # 条件：newprice 提取出的数字不为 0，且 newprice 提取出的数字小于 price 提取出的数字
                        if new_price_value != 0 and new_price_value < price_value:
                            with connection.cursor() as cursor:
                                cursor.execute(
                                    "UPDATE star_goods SET price = %s, update_date = NOW(), ifSeen = 0 WHERE username = %s and product_url = %s",
                                    (newprice, username, product_url))
                            with connection.cursor() as cursor:
                                cursor.execute("SELECT email from users WHERE username = %s", (username,))
                                email = cursor.fetchone()
                                print(email[0])
                            self.send_email(product_url, title, price, email[0])  # 发送邮件
                print('价格更新完成')
                # 每12小时运行一次
                time.sleep(12 * 60 * 60)  # 12小时

        # 启动线程
        thread = threading.Thread(target=fetch_and_print)
        thread.daemon = True  # 守护线程，主程序结束时线程自动结束
        thread.start()

        self.stdout.write(self.style.SUCCESS('定时任务已启动，正在每12小时提取数据...'))

    def get_product_price(self, all_product_url):
        all_price = []
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
        cookie_file_taobao = f'cookie_taobao.txt'
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

        jingdong_url = 'https://passport.jd.com/new/login.aspx'
        cookie_file_jingdong = f'cookie_jingdong.txt'
        if not os.path.exists(cookie_file_jingdong):
            driver.get(jingdong_url)
            # 等待手动登录完成
            time.sleep(60)
            # 获取当前的 cookies 并保存到文件
            cookies = driver.get_cookies()
            with open(cookie_file_jingdong, 'w') as f:
                json.dump(cookies, f)
            print("Cookies 已保存到文件：cookie_file_weipinhui.txt")
        else:
            print("cookie_file_jingdong.txt 已存在，跳过登录步骤。")
            driver.get('https://www.jd.com/')
            with open(cookie_file_jingdong, 'r') as f:
                cookies = json.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)

        cookie_file_weipinhui = f'cookie_weipinhui.txt'
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
        for shop in all_product_url:
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
            # 访问指定 URL
            driver.get(shop)
            time.sleep(2)  # 验证
            # 获取页面的实际地址
            shop = driver.current_url
            print(shop)
            time.sleep(0.5)
            if 'item.taobao.com' in shop or 'detail.tmall.com' in shop:
                html = driver.page_source
                doc = pq(html)
                item = doc(f'.highlightPrice--OOP9oDP8')
                if not item:
                    print(f"未找到商品价格")
                    item = doc(f'.originPrice--UnZ18wCd')
                    if not item:
                        print(f"未找到商品价格")
                        all_price.append("未找到商品价格")
                    else:
                        try:
                            price = item.find('.priceText--gdYzG_l_').eq(0).text()
                            print(price)
                            all_price.append(price)
                        except Exception as e:
                            print(f"商品抓取失败: {e}")
                            all_price.append("未找到商品价格")
                else:
                    try:
                        price = item.find('.text--fZ9NUhyQ').text()
                        print(price)
                        all_price.append(price)
                    except Exception as e:
                        print(f"商品抓取失败: {e}")
                        all_price.append("未找到商品价格")

            # elif 'item.jd.com' in shop:
            #     html = driver.page_source
            #     doc = pq(html)
            #     item = doc(f'.p-price')
            #     if not item:
            #         print(f"未找到商品价格")
            #         item = doc(f'.summary-price J-summary-price')
            #         if not item:
            #             print(f"未找到商品价格")
            #             all_price.append("未找到商品价格")
            #         try:
            #             price = item.find('.price').eq(0).text()
            #             print(price)
            #         except Exception as e:
            #             print(f"商品抓取失败: {e}")
            #         all_price.append(price)
            #     try:
            #         price = item.find('.text--fZ9NUhyQ').text()
            #         print(price)
            #     except Exception as e:
            #         print(f"商品抓取失败: {e}")
            #     all_price.append(price)
            #     try:
            #         price = item.find('.price').text().eq(0).text()
            #         print(price)
            #     except Exception as e:
            #         print(f"商品抓取失败: {e}")
            #     all_price.append(price)
            else:
                all_price.append("未找到商品价格")
        # 在最后对 all_price 进行处理，去掉重复的价格
        all_price = remove_duplicates_from_price_list(all_price)
        print('all_price')
        print(all_price)
        return all_price

    def send_email(self, product_url, title, price, email):
        """
        发送价格更新邮件
        :param product_url: 商品的URL
        :param title: 商品标题
        :param price: 商品当前价格
        :param email: 收件人邮箱
        :return: 成功：0 失败：-1
        """
        EMAIL_FROM = "2519639200@qq.com"  # 邮件发送方（设置为发件人的邮箱）
        if product_url.startswith('//'):
            product_url = 'https:' + product_url
        email_title = f'降价提醒：{title}'  # 邮件主题，包含商品标题
        email_body = f"""
           您关注的商品 {title} 价格发生了变化！

           当前价格: {price} 元

           商品链接：{product_url}

           如果您有任何疑问，请联系2519639200@qq.com。
           """

        try:
            # 发送邮件
            send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
            if send_status > 0:
                return 0  # 发送成功
            else:
                return -1  # 邮件发送失败
        except Exception as e:
            print(f"发送邮件时发生错误: {e}")
            return -1  # 发送失败