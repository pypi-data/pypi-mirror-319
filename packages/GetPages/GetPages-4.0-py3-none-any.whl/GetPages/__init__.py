import importlib

# 动态导入模块
get_pages_module = importlib.import_module("GetPages")

# 将模块中的类或函数暴露给外部
PageGetter = get_pages_module.PageGetter
get_page_info = get_pages_module.get_page_info

# 可选：定义包的版本号
__version__ = "3.0.0"