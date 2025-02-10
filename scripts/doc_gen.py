# Recommend cpython 3.13

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
    "json2srt",
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


def parse(data: dict, indent: int = 0, root: bool = False):
    if data.get("cross_ref") and not root:
        return
    elif data.get("cross_ref"):
        file = "/".join(data["cross_ref"].split(".")[:-1])
        jsons = json.load(
            open(
                os.path.join(
                    ".mypy_cache", f"{sys.version_info.major}.{sys.version_info.minor}"
                )
                + "/"
                + file
                + ".data.json"
            )
        )
        parse(jsons["names"][data["cross_ref"].split(".")[-1]], indent, root=True)
        return
    if data["node"][".class"] == "TypeInfo":
        if data["node"]["defn"]["name"] in ignored_classes:
            return
        if not data["node"]["defn"]["name"].startswith("Request"):
            funcs.append(
                [
                    data["node"]["defn"]["name"],
                    data["node"]["defn"]["fullname"],
                    "class",
                    data["node"]["bases"][0],
                    indent,
                ]
            )
            if data["node"]["metadata"].get("dataclass"):
                funcs[-1][3] = "@dataclasses.dataclass"
    elif data["node"][".class"] == "FuncDef":
        if data["node"]["name"] in ignored_funcs:
            return
        funcs.append(
            [
                data["node"]["name"],
                data["node"]["fullname"],
                "async def" if "is_coroutine" in data["node"]["flags"] else "def",
                "",
                indent,
            ]
        )
    elif (
        data["node"][".class"] == "Decorator"
        and "is_static" in data["node"]["func"]["flags"]
    ):
        funcs.append(
            [
                data["node"]["func"]["name"],
                data["node"]["func"]["fullname"],
                (
                    "async def"
                    if "is_coroutine" in data["node"]["func"]["flags"]
                    else "def"
                ),
                "@staticmethod",
                indent,
            ]
        )
    elif (
        data["node"][".class"] == "Var"
        and not "is_suppressed_import" in data["node"]["flags"]
    ):
        if data["node"]["name"] in ignored_vars:
            return
        if indent != 1:
            return
        funcs.append(
            (
                data["node"]["name"],
                data["node"]["fullname"],
                "const",
                "",
                indent,
            )
        )
    else:
        return
    if not "names" in data["node"]:
        return
    if data["node"]["bases"][0] == "enum.Enum":
        return
    for key in data["node"]["names"].keys():
        if (not str(key).startswith("_") and key != ".class") or str(key) == "__init__":
            parse(data["node"]["names"][key], indent + 1)


modules = os.listdir(
    f".mypy_cache/{sys.version_info.major}.{sys.version_info.minor}/bilibili_api"
)
modules.sort()
for module in modules:
    if module.find("settings") != -1:
        continue
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

funcs = []
funcs.append(("bilibili_api", "bilibili_api", "MODULE", 1))
data = json.load(
    open(
        os.path.join(
            ".mypy_cache",
            f"{sys.version_info.major}.{sys.version_info.minor}",
            "bilibili_api",
            "__init__.data.json",
        )
    )
)
for key in data["names"].keys():
    if key != ".class" and not key.startswith("_"):
        if os.path.exists(
            os.path.join(
                ".mypy_cache",
                f"{sys.version_info.major}.{sys.version_info.minor}",
                "bilibili_api",
                key + ".data.json",
            )
        ):
            continue
        if key == "request_log":
            funcs.append(("request_log", "bilibili_api.request_log", "var", "AsyncEvent", 2))
            parse(json.load(open(os.path.join(
                ".mypy_cache",
                f"{sys.version_info.major}.{sys.version_info.minor}",
                "bilibili_api",
                "utils",
                "network.data.json"
            )))["names"]["RequestLog"], 2)
        elif key == "request_settings":
            funcs.append(("request_settings", "bilibili_api.request_settings", "var", "builtins.object", 2))
            parse(json.load(open(os.path.join(
                ".mypy_cache",
                f"{sys.version_info.major}.{sys.version_info.minor}",
                "bilibili_api",
                "utils",
                "network.data.json"
            )))["names"]["RequestSettings"], 2)
        elif key == "HEADERS":
            funcs.append(("HEADERS", "bilibili_api.HEADERS", "var", "builtins.object", 2))
        else:
            parse(data["names"][key], 2, root=True)
all_funcs.append(funcs)


def parse_docstring(doc: str):
    if not doc:
        doc = ""
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
                argtype = (
                    argtype.replace("(", "[")
                    .replace(")", "]")
                    .replace("tuple", "Tuple")
                    .replace("list", "List")
                    .replace("dict", "Dict")
                    .replace("union", "Union")
                    .replace("|", "\|")
                )
                # print(line)
                # assert argtype != ""
                table.append((argname, argtype, arginfo))
            elif state == 2:
                ret += line + "\n"
                state = 3
            else:
                note += line + "\n"
    if ret.replace(" ", "").replace("\n", "") != "":
        rettype = ret.split(":")[0]
        retdesc = "".join(ret.split(":")[1:])
        # print(ret.split(":"))
        # assert retdesc != ""
        ret = f"**Returns:** `{rettype}`: {retdesc}"
    else:
        ret = ""
    mdstring = f"{info}\n"
    if table != []:
        mdstring += "| name | type | description |\n| - | - | - |\n"
        for arg in table:
            mdstring += f"| `{arg[0]}` | `{arg[1]}` | {arg[2]} |\n"
    mdstring += f"\n{ret}\n{note}\n\n"
    return mdstring


def parse_docstring1(doc: str):
    if not doc:
        doc = ""
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
                if line.find(":") == -1:
                    state = 0
                    info += line + "\n"
                    continue
                arginfo = line.split(":")[1].lstrip()
                argname = line.split("(")[0].rstrip()
                argtype = line[len(argname) : len(line.split(":")[0])]
                argtype = argtype.lstrip(" ").rstrip(" ")[1:-1]
                argtype = (
                    argtype.replace("(", "[")
                    .replace(")", "]")
                    .replace("tuple", "Tuple")
                    .replace("list", "List")
                    .replace("dict", "Dict")
                    .replace("union", "Union")
                    .replace("|", "\|")
                )
                # print(line)
                # assert argtype != ""
                table.append((argname, argtype, arginfo))
    mdstring = f"{info}\n"
    if table != []:
        mdstring += "| name | type | description |\n| - | - | - |\n"
        for arg in table:
            mdstring += f"| `{arg[0]}` | `{arg[1]}` | {arg[2]} |\n"
    mdstring += f"\n\n"
    return mdstring


import bilibili_api

for module in all_funcs:
    docs_dir = "./docs/modules/" + module[0][0] + ".md"
    file = open(docs_dir, "w+")
    print("BEGIN", module[0][0])
    if module[0][0] != "bilibili_api":
        file.write(
            f"# Module {module[0][0]}.py\n\n{eval(f'{module[0][1]}.__doc__')}\n\n``` python\nfrom bilibili_api import {module[0][0]}\n```\n\n"
        )
    else:
        file.write(f"# Module bilibili_api\n\n{eval(f'{module[0][1]}.__doc__')}\n\n``` python\nfrom bilibili_api import ...\n```\n\n")
    print("GENERATING TOC")
    last_data_class = -114514
    for idx, func in enumerate(module[1:]):
        if idx == last_data_class + 1:
            # don't show __init__ of dataclass and ApiException
            continue
        if func[3] == "@dataclasses.dataclass" or func[1].count("exceptions") == 1 or func[0].startswith("request_"):
            last_data_class = idx
        file.write(
            "  " * (func[4] - 2)
            + f"- [{func[2]} {func[0].replace("_", "\\_")}{["()", ""][func[2] == "var"]}](#{func[2].replace(' ', '-')}-{func[0].replace("_", "\\_")})\n"
        )
    file.write("\n")
    last_data_class = -114514
    for idx, func in enumerate(module[1:]):
        if idx == last_data_class + 1:
            # don't show __init__ of dataclass and ApiException
            continue
        if func[1].count("exceptions") == 1:
            func[1] = ".".join(func[1].split(".")[:2] + func[1].split(".")[3:])
        print("PROCESS", func[1])
        if func[4] == 2:
            file.write("---\n\n")
        if func[3].startswith("@"):
            file.write(f"**{func[3]}** \n\n")
        if func[3] == "@dataclasses.dataclass" or func[1].count("exceptions") == 1 or func[0].startswith("request_"):
            last_data_class = idx
        if func[0] == "__init__":
            func[0] = "\\_\\_init\\_\\_"
        file.write("#" * func[4] + f" {func[2]} {func[0]}{["()", ""][func[2] == "var"]}\n\n")
        if func[0] == "HEADERS":
            continue
        if func[2] == "class" or func[2] == "var":
            if not func[3].startswith("@") and func[3] != "builtins.object":
                file.write(f"**Extend: {func[3]}**\n\n")
            if func[0] in ["request_log", "BiliAPIClient"]:
                doc = eval(f"{func[1]}.__doc__")
                for line in doc.split("\n"):
                    file.write(line + "\n")
                file.write("\n\n")
            else:
                file.write(parse_docstring1(eval(f"{func[1]}.__doc__")))
        else:
            if func[0] == "\\_\\_init\\_\\_":
                file.write(parse_docstring1(eval(f"{func[1]}.__doc__")))
            else:
                file.write(parse_docstring(eval(f"{func[1]}.__doc__")))
    file.close()
    print("DONE", docs_dir)
