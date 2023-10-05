import requests
from bs4 import BeautifulSoup
import re, time, random
from urllib import parse
import math
import json
from check_blog import searchPost

def get_total_cnt(blog_id):
    url = f'https://blog.naver.com/PostList.naver?blogId={blog_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find_all(class_='category_title pcol2')
    cnt = title[0].text.strip().split('전체보기 ')[1].split('개의 글')[0]
    return cnt

def naver_blog_list(blog_id, page):

    count_per_page = 30
    tot_count = int(get_total_cnt(blog_id))
    all_page = math.ceil(tot_count/count_per_page)
    blog_list_html = ''

    print('총 ', all_page, '페이지 조회 시작 ( 포스트개수:', tot_count, ')')

    count = 0
    url = f'https://blog.naver.com/PostTitleListAsync.naver?blogId={blog_id}&viewdate=&currentPage={page}&categoryNo=&parentCategoryNo=&countPerPage={count_per_page}'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    print(f'page{page} > START')

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    url_str = parse.unquote(response.text)

    p = re.compile('"logNo":"\d+"')
    logNos = p.findall(url_str)
    blognos = []
    for log in logNos:
        blognos.append(log.split(':"')[1][:-1])

    for blog_no in blognos:
        blog_url = f'https://blog.naver.com/PostView.naver?blogId={blog_id}&logNo={blog_no}'
        time.sleep(random.uniform(0.1, 0.5))
        response = requests.get(blog_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        post_body = soup.find('table', id='printPost1') #find('div', id='postListBody')

        if blog_tit := post_body.find('div', class_= 'pcol1'):
            if blog_tit.find('span'):
                blog_title = blog_tit.find('span').text.strip().replace('\n','')
            else:
                blog_title = blog_tit.find('h3').text.strip().replace('/n','')
                blog_title = re.sub('"  "|\t|\r|\n\n', '', blog_title).replace(u'\u200b', '')

        count += 1
        status = searchPost.search(blog_id, blog_title)
        print('[OK]' if status == 1 else '[누락]', ' > ', blog_title)
        blog_list_html += f'<tr><td><a href="{blog_url}" target="_blanc"> {blog_title}</a></td><td style="text-align:center;">'+('<span style="color:green">OK</span>' if status == 1 else '<span style="color:red">FAIL</span>')+'</td></tr>';

    print('page', page, ' > END')

    return json.dumps({"html": blog_list_html, "all_page":all_page})
