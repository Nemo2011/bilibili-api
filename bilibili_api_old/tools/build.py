import cssutils
import json


def build_article_style_json():
    css = cssutils.parseFile("./article_style.css")
    result = {}
    for rule in css:
        styles = {}
        for style in rule.style:
            v = style.value
            styles[style.name] = v
        for selector in rule.selectorList:
            text = selector.selectorText.replace(".article-holder ", "").lstrip(".")
            result[text] = styles

    with open("../data/article_style.json", "w", encoding="utf8") as f:
        f.write(json.dumps(result, indent=4, ensure_ascii=False))

