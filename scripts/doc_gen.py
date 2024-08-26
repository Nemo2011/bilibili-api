import os
import sys
import json

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))

os.system("stubgen bilibili_api -o .doc_cache/ --include-docstrings")

all_funcs = []
funcs = []

ignored_classes = [
    "AnchorNode",
    "ArticleCardNode",
    "BangumiCardNode",
    "BlockquoteNode",
    "BoldNode",
    "CodeNode",
    "ColorNode",
    "ComicCardNode",
    "DelNode",
    "FontSizeNode",
    "HeadingNode",
    "ImageNode",
    "ItalicNode",
    "LatexNode",
    "LiNode",
    "LiveCardNode",
    "MusicCardNode",
    "Node",
    "OlNode",
    "ParagraphNode",
    "SeparatorNode",
    "ShopCardNode",
    "TextNode",
    "UlNode",
    "UnderlineNode",
    "VideoCardNode",
    "node_info",
    "ServerThreadModel",
    "Datapack",
]

ignored_funcs = [
    "export_ass_from_json",
    "export_ass_from_srt",
    "export_ass_from_xml",
    "app_signature",
    "encrypt",
    "id_",
    "photo",
    "is_destroy",
    "login_key",
    "make_qrcode",
    "parse_credential_url",
    "parse_tv_resp",
    "photo",
    "qrcode_image",
    "start",
    "update_qrcode_data",
    "update_tv_qrcode_data",
    "verify_tv_login_status",
    "generate_clickPosition",
    "BAD_FOR_YOUNGS",
    "CANNOT_CHARGE",
    "CLICKBAIT",
    "COVID_RUMORS",
    "GAMBLED_SCAMS",
    "ILLEGAL",
    "LEAD_WAR",
    "OTHER",
    "PERSONAL_ATTACK",
    "POLITICAL_RUMORS",
    "PRON",
    "SOCIAL_RUMORS",
    "UNREAL_EVENT",
    "VIOLENT",
    "VULGAR",
    "set_aid_e",
    "set_bvid_e",
    "get_geetest",
    "get_safecenter_geetest",
    "login_with_key",
]

ignored_vars = [
    "API",
    "API_USER",
    "API_video",
    "countries_list",
    "cheese_video_meta_cache",
    "fes_id",
    "credential",
    "API_rank",
    "DATAPACK_TYPE_HEARTBEAT",
    "DATAPACK_TYPE_HEARTBEAT_RESPONSE",
    "DATAPACK_TYPE_NOTICE",
    "DATAPACK_TYPE_VERIFY",
    "DATAPACK_TYPE_VERIFY_SUCCESS_RESPONSE",
    "PROTOCOL_VERSION_BROTLI_JSON",
    "PROTOCOL_VERSION_HEARTBEAT",
    "PROTOCOL_VERSION_RAW_JSON",
    "STATUS_CLOSED",
    "STATUS_CLOSING",
    "STATUS_CONNECTING",
    "STATUS_ERROR",
    "STATUS_ESTABLISHED",
    "STATUS_INIT",
    "err_reason",
    "logger",
    "max_retry",
    "retry_after",
    "room_display_id",
    "app_signature",
    "captcha_key",
    "check_url",
    "geetest_result",
    "tmp_token",
    "yarl_url",
    "captcha_id",
    "API_audio",
    "API_ARTICLE",
    "handler",
    "logger",
    "LINES_INFO",
    "watch_room_bangumi_cache",
]


def parse(data: dict, indent: int = 0):
    if data.get("cross_ref"):
        return
    if data["node"][".class"] == "TypeInfo":
        if data["node"]["defn"]["name"] in ignored_classes:
            return
        funcs.append(
            (
                data["node"]["defn"]["name"],
                data["node"]["defn"]["fullname"],
                f'class({data["node"]["bases"][0]})',
                indent,
            )
        )
    elif data["node"][".class"] == "FuncDef":
        if data["node"]["name"] in ignored_funcs:
            return
        funcs.append(
            (
                data["node"]["name"],
                data["node"]["fullname"],
                "async def" if "is_coroutine" in data["node"]["flags"] else "def",
                indent,
            )
        )
    elif (
        data["node"][".class"] == "Var"
        and not "is_suppressed_import" in data["node"]["flags"]
    ):
        if data["node"]["name"] in ignored_vars:
            return
        if indent != 1:
            return
        funcs.append((data["node"]["name"], data["node"]["fullname"], "const", indent))
    else:
        return
    if not "names" in data["node"]:
        return
    if data["node"]["bases"][0] == "enum.Enum":
        return
    for key in data["node"]["names"].keys():
        if not str(key).startswith("_") and key != ".class":
            parse(data["node"]["names"][key], indent + 1)


modules = os.listdir(
    f".mypy_cache/{sys.version_info.major}.{sys.version_info.minor}/bilibili_api"
)
modules.sort()
for module in modules:
    if module.find("data.json") != -1 and module != "__init__.data.json":
        funcs = []
        data = json.load(
            open(
                os.path.join(
                    ".mypy_cache",
                    f"{sys.version_info.major}.{sys.version_info.minor}",
                    "bilibili_api",
                    module,
                )
            )
        )
        funcs.append((module[:-10], "bilibili_api." + module[:-10], "MODULE", 1))
        for key in data["names"].keys():
            if key != ".class" and not key.startswith("_"):
                parse(data["names"][key], 2)
        all_funcs.append(funcs)


def parse_docstring(doc: str):
    doc = doc.replace("    ", "")
    doc = doc.lstrip("\n")
    info = ""
    table = []
    ret = ""
    note = ""
    state = 0
    for line in doc.split("\n"):
        if line.startswith("Attribute") or line.startswith("Args"):
            state = 1
        elif line.startswith("Return"):
            state = 2
        else:
            if state == 0:
                info += line + "\n"
            elif state == 1:
                if line == "":
                    continue
                arginfo = line.split(":")[1].lstrip()
                argname = line.split("(")[0].rstrip()
                argtype = line[len(argname) : len(line.split(":")[0])]
                argtype = argtype.lstrip(" ").rstrip(" ")[1:-1]
                if argtype.startswith("Optional"):
                    argtype = f"Union[{argtype.split(' ')[1].rstrip()}, None]"
                if argtype.endswith("optional"):
                    argtype = (
                        f"Union[{argtype.split(' ')[0].rstrip(',').rstrip()}, None]"
                    )
                argtype = (
                    argtype.replace("(", "[")
                    .replace(")", "]")
                    .replace("tuple", "Tuple")
                    .replace("list", "List")
                    .replace("dict", "Dict")
                    .replace("union", "Union")
                    .replace("|", "\|")
                )
                table.append((argname, argtype, arginfo))
            elif state == 2:
                ret += line + "\n"
                state = 3
            else:
                note += line + "\n"
    if ret.replace(" ", "").replace("\n", "") == "":
        ret = "None\n"
    ret = "**Returns:** " + ret
    mdstring = f"{info}\n"
    if table != []:
        mdstring += "| name | type | description |\n| - | - | - |\n"
        for arg in table:
            mdstring += f"| {arg[0]} | {arg[1]} | {arg[2]} |\n"
    mdstring += f"\n{ret}\n{note}\n\n"
    return mdstring


def parse_docstring1(doc: str):
    doc = doc.replace("    ", "")
    doc = doc.lstrip("\n")
    info = ""
    table = []
    ret = ""
    note = ""
    state = 0
    for line in doc.split("\n"):
        if line.startswith("Attribute") or line.startswith("Args"):
            state = 1
        else:
            if state == 0:
                info += line + "\n"
            elif state == 1:
                if line == "":
                    continue
                arginfo = line.split(":")[1].lstrip()
                argname = line.split("(")[0].rstrip()
                argtype = line[len(argname) : len(line.split(":")[0])]
                argtype = argtype.lstrip(" ").rstrip(" ")[1:-1]
                if argtype.startswith("Optional") or argtype.startswith("optional"):
                    argtype = f"Union[{argtype.split(' ')[1].rstrip()}, None]"
                if argtype.endswith("optional") or argtype.endswith("Optional"):
                    argtype = (
                        f"Union[{argtype.split(' ')[0].rstrip(',').rstrip()}, None]"
                    )
                argtype = (
                    argtype.replace("(", "[")
                    .replace(")", "]")
                    .replace("tuple", "Tuple")
                    .replace("list", "List")
                    .replace("dict", "Dict")
                    .replace("union", "Union")
                    .replace("|", "\|")
                )
                table.append((argname, argtype, arginfo))
    mdstring = f"{info}\n"
    if table != []:
        mdstring += "| name | type | description |\n| - | - | - |\n"
        for arg in table:
            mdstring += f"| {arg[0]} | {arg[1]} | {arg[2]} |\n"
    mdstring += f"\n\n"
    return mdstring


import bilibili_api

for module in all_funcs:
    docs_dir = "./docs/modules/" + module[0][0] + ".md"
    file = open(docs_dir, "w+")
    file.write(
        f"# Module {module[0][0]}.py\n\n{eval(f'{module[0][1]}.__doc__')}\n\n``` python\nfrom bilibili_api import {module[0][0]}\n```\n\n"
    )
    for func in module[1:]:
        print("PROCESS", func[1])
        file.write("#" * func[3] + " ")
        if func[2].find("class") != -1:
            file.write(
                f"class {func[0]}\n\n**Extend: {func[2].split('(')[1][:-1]}**\n\n"
            )
            file.write(parse_docstring1(eval(f"{func[1]}.__doc__")))
        else:
            file.write(f"{func[2]} {func[0]}()\n\n")
            file.write(parse_docstring(eval(f"{func[1]}.__doc__")))
    file.close()
    print("DONE", docs_dir)
