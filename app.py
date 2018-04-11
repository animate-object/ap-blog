from chalice import Chalice
from chalicelib.methods import get_post, list_posts

app = Chalice(app_name='ablog')


@app.route('/ping')
def index():
    return {'a': 'blog'}


@app.route('/posts', methods=['GET'])
def post_list():
    return list_posts()


@app.route('/posts/{post_id}', methods=['GET'])
def post_by_id():
    return get_post(post_id)
