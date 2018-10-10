from django.apps import AppConfig


class StarkConfig(AppConfig):
    # 这里是本组件的名称，修改这里需要大幅改动源码，需谨慎操作
    name = 'stark'

    def ready(self):
        from django.utils.module_loading import autodiscover_modules
        # 当程序启动时，去每个app目录下找stark.py并加载。
        # 此步骤发生在生成URL前
        autodiscover_modules('stark')
