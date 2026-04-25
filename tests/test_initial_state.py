from urllib.parse import quote

from bilibili_api.utils.initial_state import _parse_detected_content


async def test_a_parse_plain_json():
    data = _parse_detected_content('{"a":1,"b":"x"}</script>')
    assert data["a"] == 1
    assert data["b"] == "x"


async def test_b_parse_percent_encoded_json():
    encoded = quote('{"access_id":"abc","n":"5"}')
    data = _parse_detected_content(encoded + "</script>")
    assert data["access_id"] == "abc"
    assert data["n"] == "5"
