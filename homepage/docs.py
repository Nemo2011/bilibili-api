from flask import *
import utils

bp = Blueprint('docs', __name__, url_prefix='/bilibili_api/docs')


@bp.route('/', methods=['GET'])
def index():
    settings = get_article('README.md')
    return render_template('article.html', settings=settings)


@bp.route('/<path:path>', methods=['GET'])
def docs(path):
    settings = get_article(path)
    return render_template('article.html', settings=settings)


def get_article(path):
    catalog = utils.get_doc_catalog()
    cata = {
        "name": "bilibili_api",
        "homepage": "/bilibili_api",
        "github": "https://github.com/Passkou/bilibili_api",
        "banner": "https://res.passkou.com/image/20200812011335.png",
        "desc": "[Python]bilibili_api的开发文档，该模块可以方便地调用b站各种API"
    }
    if path == "README.md":
        title = f"{cata['name']} 开发文档"
        content = utils.markdown2html(utils.get_readme())
    else:
        path = path.split('/')
        t = path.copy()
        t.reverse()
        title = f"{' - '.join(t)} - {cata['name']} 开发文档"
        content = utils.get_doc_content("/".join(path))
        if content is None:
            abort(404)
        content = utils.markdown2html(content)
    settings = {
        "title": title,
        "content": content,
        "catalog": catalog,
        "region": cata["name"],
        "homepage": cata["homepage"],
        "github": cata["github"]
    }
    return settings