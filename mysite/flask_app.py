from flask import *
import json
import sys
from os import path

project_home = path.abspath('../..')
project_home = project_home + '\python-play\mysite\src'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path
    print(sys.path)

from check_blog_src import getPosts

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_blog')
def check():
    print('OK')
    context = {}
    return render_template('check_blog/check.html', context=context)

@app.route('/result_blog')
def result_blog():
    blog_id = request.args.get('blog_id')
    page = request.args.get('page')
    result = getPosts.naver_blog_list(blog_id, page)
    json_result = json.loads(result)
    return {'blog_id':blog_id, 'all_page':json_result['all_page'], 'page':page, 'output':json_result['html']}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
