from chalice import Chalice
from chalicelib.methods import get_post, list_posts
from chalicelib.utils import handle_errors

app = Chalice(app_name='ablog')


@app.route('/ping')
def index():
    return {'a': 'blog'}


@app.route('/posts', methods=['GET'])
@handle_errors
def post_list():
    return list_posts()


@app.route('/posts/{post_id}', methods=['GET'])
@handle_errors
def post_by_id(post_id):
    return get_post(post_id)
