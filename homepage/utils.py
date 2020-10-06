import os
import markdown
import re


def get_version():
    from setup import version
    return version


def markdown2html(markdown_content):
    html = markdown.markdown(markdown_content, output_format="html5", tab_length=4, extensions=['extra'])
    content = re.sub("~~(.*?)~~", "<s>\g<1></s>", html)
    content = content.replace(r"\~", "~")
    return content


def get_readme():
    with open('../README.md', encoding='utf8') as f:
        return f.read()


def get_doc_catalog():
    catalog = []
    for root, folders, files in os.walk('..\\docs'):
        for file in files:
            path = os.path.join(root, file).replace('..\\docs\\', '')
            catalog.append(path.replace('\\', '/'))
    return catalog


def get_doc_content(doc_path):
    try:
        path = os.path.join('..\\docs', doc_path.replace('..', '').replace('/', '\\'))
    except:
        return None
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf8') as f:
        return f.read()