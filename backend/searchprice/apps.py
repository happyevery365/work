from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'searchprice'

    def ready(self):
        # 在应用启动时执行自定义命令
        from django.core.management import call_command
        call_command('fetch_goods_data')  # 调用自定义管理命令
