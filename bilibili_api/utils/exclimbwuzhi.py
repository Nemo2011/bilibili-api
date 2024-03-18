import time
import random
import struct
import io
import json


MOD = 1 << 64


def get_time_milli() -> int:
    return int(time.time() * 1000)


def rotate_left(x: int, k: int) -> int:
    bin_str = bin(x)[2:].rjust(64, "0")
    return int(bin_str[k:] + bin_str[:k], base=2)


def gen_uuid_infoc() -> str:
    t = get_time_milli() % 100000
    mp = list("123456789ABCDEF") + ["10"]
    pck = [8, 4, 4, 4, 12]
    gen_part = lambda x: "".join([random.choice(mp) for _ in range(x)])
    return "-".join([gen_part(l) for l in pck]) + str(t).ljust(5, "0") + "infoc"


def gen_b_lsid() -> str:
    ret = ""
    for _ in range(8):
        ret += hex(random.randint(0, 15))[2:].upper()
    ret = f"{ret}_{hex(get_time_milli())[2:].upper()}"
    return ret


def gen_buvid_fp(key: str, seed: int):
    source = io.BytesIO(bytes(key, "ascii"))
    m = murmur3_x64_128(source, seed)
    return "{}{}".format(hex(m & (MOD - 1))[2:], hex(m >> 64)[2:])


def murmur3_x64_128(source: io.BufferedIOBase, seed: int) -> str:
    C1 = 0x87C3_7B91_1142_53D5
    C2 = 0x4CF5_AD43_2745_937F
    C3 = 0x52DC_E729
    C4 = 0x3849_5AB5
    R1, R2, R3, M = 27, 31, 33, 5
    h1, h2 = seed, seed
    processed = 0
    while 1:
        read = source.read(16)
        processed += len(read)
        if len(read) == 16:
            k1 = struct.unpack("<q", read[:8])[0]
            k2 = struct.unpack("<q", read[8:])[0]
            h1 ^= rotate_left(k1 * C1 % MOD, R2) * C2 % MOD
            h1 = ((rotate_left(h1, R1) + h2) * M + C3) % MOD
            h2 ^= rotate_left(k2 * C2 % MOD, R3) * C1 % MOD
            h2 = ((rotate_left(h2, R2) + h1) * M + C4) % MOD
        elif len(read) == 0:
            h1 ^= processed
            h2 ^= processed
            h1 = (h1 + h2) % MOD
            h2 = (h2 + h1) % MOD
            h1 = fmix64(h1)
            h2 = fmix64(h2)
            h1 = (h1 + h2) % MOD
            h2 = (h2 + h1) % MOD
            return (h2 << 64) | h1
        else:
            k1 = 0
            k2 = 0
            if len(read) >= 15:
                k2 ^= int(read[14]) << 48
            if len(read) >= 14:
                k2 ^= int(read[13]) << 40
            if len(read) >= 13:
                k2 ^= int(read[12]) << 32
            if len(read) >= 12:
                k2 ^= int(read[11]) << 24
            if len(read) >= 11:
                k2 ^= int(read[10]) << 16
            if len(read) >= 10:
                k2 ^= int(read[9]) << 8
            if len(read) >= 9:
                k2 ^= int(read[8])
                k2 = rotate_left(k2 * C2 % MOD, R3) * C1 % MOD
                h2 ^= k2
            if len(read) >= 8:
                k1 ^= int(read[7]) << 56
            if len(read) >= 7:
                k1 ^= int(read[6]) << 48
            if len(read) >= 6:
                k1 ^= int(read[5]) << 40
            if len(read) >= 5:
                k1 ^= int(read[4]) << 32
            if len(read) >= 4:
                k1 ^= int(read[3]) << 24
            if len(read) >= 3:
                k1 ^= int(read[2]) << 16
            if len(read) >= 2:
                k1 ^= int(read[1]) << 8
            if len(read) >= 1:
                k1 ^= int(read[0])
            k1 = rotate_left(k1 * C1 % MOD, R2) * C2 % MOD
            h1 ^= k1


def fmix64(k: int) -> int:
    C1 = 0xFF51_AFD7_ED55_8CCD
    C2 = 0xC4CE_B9FE_1A85_EC53
    R = 33
    tmp = k
    tmp ^= tmp >> R
    tmp = tmp * C1 % MOD
    tmp ^= tmp >> R
    tmp = tmp * C2 % MOD
    tmp ^= tmp >> R
    return tmp


def get_payload(uuid: str) -> str:
    content = {
        "3064": 1,
        "5062": get_time_milli(),
        "03bf": "https%3A%2F%2Fwww.bilibili.com%2F",
        "39c8": "333.788.fp.risk",
        "34f1": "",
        "d402": "",
        "654a": "",
        "6e7c": "839x959",
        "3c43": {
            "2673": 0,
            "5766": 24,
            "6527": 0,
            "7003": 1,
            "807e": 1,
            "b8ce": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
            "641c": 0,
            "07a4": "en-US",
            "1c57": "not available",
            "0bd0": 8,
            "748e": [900, 1440],
            "d61f": [875, 1440],
            "fc9d": -480,
            "6aa9": "Asia/Shanghai",
            "75b8": 1,
            "3b21": 1,
            "8a1c": 0,
            "d52f": "not available",
            "adca": "MacIntel",
            "80c9": [
                [
                    "PDF Viewer",
                    "Portable Document Format",
                    [["application/pdf", "pdf"], ["text/pdf", "pdf"]],
                ],
                [
                    "Chrome PDF Viewer",
                    "Portable Document Format",
                    [["application/pdf", "pdf"], ["text/pdf", "pdf"]],
                ],
                [
                    "Chromium PDF Viewer",
                    "Portable Document Format",
                    [["application/pdf", "pdf"], ["text/pdf", "pdf"]],
                ],
                [
                    "Microsoft Edge PDF Viewer",
                    "Portable Document Format",
                    [["application/pdf", "pdf"], ["text/pdf", "pdf"]],
                ],
                [
                    "WebKit built-in PDF",
                    "Portable Document Format",
                    [["application/pdf", "pdf"], ["text/pdf", "pdf"]],
                ],
            ],
            "13ab": "0dAAAAAASUVORK5CYII=",
            "bfe9": "QgAAEIQAACEIAABCCQN4FXANGq7S8KTZayAAAAAElFTkSuQmCC",
            "a3c1": [
                "extensions:ANGLE_instanced_arrays;EXT_blend_minmax;EXT_color_buffer_half_float;EXT_float_blend;EXT_frag_depth;EXT_shader_texture_lod;EXT_texture_compression_bptc;EXT_texture_compression_rgtc;EXT_texture_filter_anisotropic;EXT_sRGB;KHR_parallel_shader_compile;OES_element_index_uint;OES_fbo_render_mipmap;OES_standard_derivatives;OES_texture_float;OES_texture_float_linear;OES_texture_half_float;OES_texture_half_float_linear;OES_vertex_array_object;WEBGL_color_buffer_float;WEBGL_compressed_texture_astc;WEBGL_compressed_texture_etc;WEBGL_compressed_texture_etc1;WEBGL_compressed_texture_pvrtc;WEBKIT_WEBGL_compressed_texture_pvrtc;WEBGL_compressed_texture_s3tc;WEBGL_compressed_texture_s3tc_srgb;WEBGL_debug_renderer_info;WEBGL_debug_shaders;WEBGL_depth_texture;WEBGL_draw_buffers;WEBGL_lose_context;WEBGL_multi_draw",
                "webgl aliased line width range:[1, 1]",
                "webgl aliased point size range:[1, 511]",
                "webgl alpha bits:8",
                "webgl antialiasing:yes",
                "webgl blue bits:8",
                "webgl depth bits:24",
                "webgl green bits:8",
                "webgl max anisotropy:16",
                "webgl max combined texture image units:32",
                "webgl max cube map texture size:16384",
                "webgl max fragment uniform vectors:1024",
                "webgl max render buffer size:16384",
                "webgl max texture image units:16",
                "webgl max texture size:16384",
                "webgl max varying vectors:30",
                "webgl max vertex attribs:16",
                "webgl max vertex texture image units:16",
                "webgl max vertex uniform vectors:1024",
                "webgl max viewport dims:[16384, 16384]",
                "webgl red bits:8",
                "webgl renderer:WebKit WebGL",
                "webgl shading language version:WebGL GLSL ES 1.0 (1.0)",
                "webgl stencil bits:0",
                "webgl vendor:WebKit",
                "webgl version:WebGL 1.0",
                "webgl unmasked vendor:Apple Inc.",
                "webgl unmasked renderer:Apple GPU",
                "webgl vertex shader high float precision:23",
                "webgl vertex shader high float precision rangeMin:127",
                "webgl vertex shader high float precision rangeMax:127",
                "webgl vertex shader medium float precision:23",
                "webgl vertex shader medium float precision rangeMin:127",
                "webgl vertex shader medium float precision rangeMax:127",
                "webgl vertex shader low float precision:23",
                "webgl vertex shader low float precision rangeMin:127",
                "webgl vertex shader low float precision rangeMax:127",
                "webgl fragment shader high float precision:23",
                "webgl fragment shader high float precision rangeMin:127",
                "webgl fragment shader high float precision rangeMax:127",
                "webgl fragment shader medium float precision:23",
                "webgl fragment shader medium float precision rangeMin:127",
                "webgl fragment shader medium float precision rangeMax:127",
                "webgl fragment shader low float precision:23",
                "webgl fragment shader low float precision rangeMin:127",
                "webgl fragment shader low float precision rangeMax:127",
                "webgl vertex shader high int precision:0",
                "webgl vertex shader high int precision rangeMin:31",
                "webgl vertex shader high int precision rangeMax:30",
                "webgl vertex shader medium int precision:0",
                "webgl vertex shader medium int precision rangeMin:31",
                "webgl vertex shader medium int precision rangeMax:30",
                "webgl vertex shader low int precision:0",
                "webgl vertex shader low int precision rangeMin:31",
                "webgl vertex shader low int precision rangeMax:30",
                "webgl fragment shader high int precision:0",
                "webgl fragment shader high int precision rangeMin:31",
                "webgl fragment shader high int precision rangeMax:30",
                "webgl fragment shader medium int precision:0",
                "webgl fragment shader medium int precision rangeMin:31",
                "webgl fragment shader medium int precision rangeMax:30",
                "webgl fragment shader low int precision:0",
                "webgl fragment shader low int precision rangeMin:31",
                "webgl fragment shader low int precision rangeMax:30",
            ],
            "6bc5": "Apple Inc.~Apple GPU",
            "ed31": 0,
            "72bd": 0,
            "097b": 0,
            "52cd": [0, 0, 0],
            "a658": [
                "Andale Mono",
                "Arial",
                "Arial Black",
                "Arial Hebrew",
                "Arial Narrow",
                "Arial Rounded MT Bold",
                "Arial Unicode MS",
                "Comic Sans MS",
                "Courier",
                "Courier New",
                "Geneva",
                "Georgia",
                "Helvetica",
                "Helvetica Neue",
                "Impact",
                "LUCIDA GRANDE",
                "Microsoft Sans Serif",
                "Monaco",
                "Palatino",
                "Tahoma",
                "Times",
                "Times New Roman",
                "Trebuchet MS",
                "Verdana",
                "Wingdings",
                "Wingdings 2",
                "Wingdings 3",
            ],
            "d02f": "124.04345259929687",
        },
        "54ef": '{"in_new_ab":true,"ab_version":{"remove_back_version":"REMOVE","login_dialog_version":"V_PLAYER_PLAY_TOAST","open_recommend_blank":"SELF","storage_back_btn":"HIDE","call_pc_app":"FORBID","clean_version_old":"GO_NEW","optimize_fmp_version":"LOADED_METADATA","for_ai_home_version":"V_OTHER","bmg_fallback_version":"DEFAULT","ai_summary_version":"SHOW","weixin_popup_block":"ENABLE","rcmd_tab_version":"DISABLE","in_new_ab":true},"ab_split_num":{"remove_back_version":11,"login_dialog_version":43,"open_recommend_blank":90,"storage_back_btn":87,"call_pc_app":47,"clean_version_old":46,"optimize_fmp_version":28,"for_ai_home_version":38,"bmg_fallback_version":86,"ai_summary_version":466,"weixin_popup_block":45,"rcmd_tab_version":90,"in_new_ab":0},"pageVersion":"new_video","videoGoOldVersion":-1}',
        "8b94": "https%3A%2F%2Fwww.bilibili.com%2F",
        "df35": uuid,
        "07a4": "en-US",
        "5f45": None,
        "db46": 0,
    }
    return json.dumps(
        {"payload": json.dumps(content, separators=(",", ":"))},
        separators=(",", ":"),
    )
