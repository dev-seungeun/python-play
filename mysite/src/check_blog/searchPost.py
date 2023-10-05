import re
import json
import urllib.request

def search_api(blog_id, search_text, start) :
    client_id = '1o99LYrimcFbrZ_ZyR0i'
    client_secret = 'mpMkqSfXL3'
    encText = urllib.parse.quote('"'+search_text+'"')
    url = f"https://openapi.naver.com/v1/search/blog.json?start={start}&display=100&query=" + encText
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)

    return parse_result(response, blog_id, search_text, start)

def search(blog_id, blog_title):
    only_BMP_pattern = re.compile("["u"\U00010000-\U0010FFFF""]+", flags=re.UNICODE)
    search_text = only_BMP_pattern.sub(r'', blog_title)

    return search_api(blog_id, search_text, 1)

def parse_result(response, blog_id, search_text, start) :
    rescode = response.getcode()
    if rescode == 200 :
        response_body = response.read()
        result = response_body.decode('utf-8')
        json_object = json.loads(result)
        tot_cnt = int(json_object["total"])
        for item in json_object["items"]:
            if item["bloggerlink"] == 'blog.naver.com/'+blog_id:
                return 1
        if tot_cnt > start*100 and start <= 5 :
            start += 1
            search_api(blog_id, search_text, start)

        return 0
    else:
        print("Error Code:" + rescode)