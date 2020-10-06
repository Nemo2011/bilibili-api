from flask import *
from docs import bp
import utils

app = Flask(__name__, static_url_path='/bilibili_api/static', static_folder='./static')
app.register_blueprint(bp)


@app.route('/bilibili_api', methods=['GET'])
def index():
    readme = utils.markdown2html(utils.get_readme())
    return render_template('index.html', version=utils.get_version(), readme=readme)


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)