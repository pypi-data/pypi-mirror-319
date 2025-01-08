import json
import os
import re
import time
import requests
import retrying
from fake_useragent import UserAgent
from loguru import logger
from urllib.parse import urljoin
from lxml import etree




def get_page_info(url, page_param=None, step=1, first_num=1, mode='direct', 
                 max_attempts=10, use_cache=False, cache_file=None, proxy=None,stop_max_attempt_number=3,sleep=1):
    """
    获取页面信息，支持直接解析和二分查找两种模式
    :param url: 初始URL
    :param page_param: 页码参数名
    :param step: 页码步长,如果页码不是连续的，可以设置步长
    :param first_num: 起始页码
    :param mode: 模式选择，'direct'（直接解析）或 'binary'（二分查找）
    :param max_attempts: 二分查找最大尝试次数
    :param use_cache: 是否使用缓存，默认关闭
    :param cache_file: 缓存文件名
    :param proxy: 代理设置
    :return: 页面链接列表, 总页数
    :stop_max_attempt_number: 重试次数
    :sleep: 重试间隔

    """
    headers = {'user-agent': str(UserAgent().random)}
    if not cache_file:
        cache_file = 'total_pages_cache.json'
    def extract_base_url(url, page_param):
        if page_param.startswith('/'):
            pattern = rf'(.*{page_param})\d+'
        else:
            pattern = rf'(.*[?&]{page_param}=)\d+'
        match = re.search(pattern, url)
        return match.group(1) if match else url.split('?')[0]


    @retrying.retry(stop_max_attempt_number=stop_max_attempt_number, 
                   retry_on_exception=lambda e: isinstance(e, requests.RequestException))
    def get_html(url):
        try:
            response = requests.get(url, headers=headers, proxies=proxy, timeout=10, verify=False)
            response.raise_for_status()  
            return response.text
        except requests.RequestException as e:
            logger.warning(f"请求失败，正在重试: {url}，错误: {str(e)}...")  
            raise  

    # 缓存处理
    def load_cache():
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_cache(cache):
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=4)

    # 检查缓存
    if use_cache:
        cache = load_cache()
        base_url=extract_base_url(url, page_param)
        cached_data = cache.get(base_url) or cache.get(url)
        if cached_data:
            logger.success(f"从缓存中读取: \nbase_url={base_url}\n总页数={cached_data['total_pages']}\n链接：{cached_data['all_pages_link'][:3]}...")
            return cached_data['all_pages_link'],cached_data['total_pages'],
        else:
            logger.info("缓存中没有找到数据")

    if mode == 'direct':
        # 直接解析模式
        response =get_html(url)
        body = etree.HTML(response)
        page_url = body.xpath("//*[text()='尾页' or text()='末页']/@href")

        if not page_url:
            logger.info("未找到尾页链接")
            return [url], 1

        full_url = urljoin(url, page_url[0])

        # 处理不同参数模式
        if page_param:
            pattern = rf'(.*{page_param})(\d+)' if page_param.startswith('/') else rf'(.*[?&]{page_param}=)(\d+)'
            match = re.search(pattern, full_url)
            if match:
                base_path = match.group(1)
                last_page_number = match.group(2)
                all_pages_link = [
                    f"{base_path}{(int(last_page_number) - i) * step + first_num}"
                    for i in range(int(last_page_number) - 1, -1, -1)
                ]
                logger.success(f"基本路径: {base_path}, 页码: {last_page_number}")
                return all_pages_link, last_page_number

        # 默认处理逻辑
        match = re.match(r'(.*/)([^/]*?_)?(\d+)(_\d+)?(\.html)?', full_url)
        if match:
            base_path = f"{match.group(1)}{match.group(2) or ''}{match.group(3)}_{{}}{match.group(5) or ''}"
            last_page_number = match.group(4)[1:] if match.group(4) else '1'
            all_pages_link = [
                base_path.format(page) for page in range(2, int(last_page_number) + 1)
            ]
            all_pages_link.append(url)
            logger.success(f"\n✅ 基本路径: {base_path}, 页码: {last_page_number}")

            if use_cache:
                cache = load_cache()
                cache['base_url'] = {
                    'total_pages': last_page_number,
                    'all_pages_link': all_pages_link
                }
            save_cache(cache)
            logger.success(f"结果已保存到缓存文件: {cache_file}")
            return all_pages_link, last_page_number

        logger.info("未能匹配到有效的路径")
        return [url], 1

    else:

        # 二分查找模式
        def is_page_valid(page_url):
            try:
                response = requests.get(page_url, headers=headers, proxies=proxy, timeout=10)
                logger.info(f"📊是否是最后一页呢?: {page_url}")
                return response.status_code == 200
            except requests.RequestException:
                return False



        def get_page_url(base_url, page_num, page_param):
            return f"{base_url}{page_num}" if page_param.startswith('/') else f"{base_url}{page_num}"

        # 提取base_url
        base_url = extract_base_url(url, page_param)

        # 动态扩展范围
        left, right = 1, 100
        attempts = 0
        while attempts < max_attempts:
            attempts += 1
            if is_page_valid(get_page_url(base_url, right, page_param)):
                left = right
                right *= 2
            else:
                break

        # 二分查找
        while left < right:
            mid = (left + right) // 2
            if is_page_valid(get_page_url(base_url, mid, page_param)):
                left = mid + 1
            else:
                right = mid
            time.sleep(sleep)

        total_pages = left - 1
        all_pages_link = [get_page_url(base_url, i, page_param) for i in range(1, total_pages + 1)]

        # 保存到缓存
        if use_cache:
            cache = load_cache()
            cache[f'{base_url}'] = {
                'total_pages': total_pages,
                'all_pages_link': all_pages_link
            }
            save_cache(cache)
            logger.success(f"🎉最后一页:{get_page_url(base_url, right, page_param)}")
            logger.success(f"✅ 结果已保存到缓存文件: {cache_file}，总页数: {total_pages}")


        return all_pages_link, total_pages


