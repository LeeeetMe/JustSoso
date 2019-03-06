import requests
from lxml import etree
import hashlib


root_url = 'http://127.0.0.1:8888/'
base_url = {
    'baidu': {
        'url': 'https://www.baidu.com/s?q1={0}&q2=&pn=0&q3=&q4=&rn=50&lm=0&ct=0&ft=&q5=&q6=&tn=baiduadv',
        'page_num': 50,
        'start_page': 0,
        'step_page': 50,
    }
}
search_xpath = {
    'baidu': {
        'url': '//div[@class="result c-container "]',
        'a': '//h3[@class="t"]//a[1]',
        'digest': '//div[contains(@class,"c-abstract")]'
    },
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
}


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").text


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={0}".format(proxy))


def get_search_url(engine, search_word):
    return base_url[engine]['url'].format(search_word)


def get_html(engine, search_word):
    retry_count = 3
    proxy = get_proxy()
    url = get_search_url(engine, search_word)
    while retry_count > 0:
        try:
            html = requests.get(url,
                                headers=headers,
                                proxies={"http": "http://{0}".format(proxy)})
            # 使用代理访问
            return html.text
        except Exception as e:
            print(e)
            retry_count -= 1
    # 出错3次, 删除代理池中代理
    delete_proxy(proxy)
    return get_html(engine, search_word)


def parse(engine, search_word):
    info_list = list()
    html = get_html(engine, search_word)
    page = etree.HTML(html)
    a_list = page.xpath(search_xpath[engine]['a'])
    digest_list = page.xpath(search_xpath[engine]['digest'])
    if not a_list:
        print('没有搜索到想要的结果')
        return None
    else:
        for a, digest in zip(a_list, digest_list):
            tmp_url = a.xpath('.//@href')[0]
            title = a.xpath('normalize-space(string(.))')
            digest = ''.join(digest.xpath('.//text()'))
            if all([title, tmp_url, digest]):
                md_url = get_md5(tmp_url)
                tmp_url_link = root_url + 'link=' + md_url
                tmp_info = {
                    'url': tmp_url_link,
                    'title': title,
                    'digest': digest,
                }
                info_list.append(tmp_info)
                set_url_to_cache(md_url, tmp_url)
    return info_list


def set_url_to_cache(key, val):
    print('存储数据到Reids中', key, val)
    cache.set(key, val, settings.REDIS_TIMEOUT)


def get_md5(data):
    hash_md5 = hashlib.md5(data.encode("utf-8"))
    md = hash_md5.hexdigest()
    return md


def get_real_url(url):
    try:
        response = requests.head(url, headers=headers)
    except Exception as e_msg:
        print(e_msg)
        return get_real_url(url)
    return response.headers.get('Location')


if __name__ == '__main__':
    info = parse('baidu', '春天的风vvvvvvvvvv')
    for item in info:
        print(item)
