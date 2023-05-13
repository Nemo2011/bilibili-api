# bilibili_api.note

from bilibili_api import note, bvid2aid
from .common import get_credential

public_note = note.Note(
    cvid=15160286, note_type=note.NoteType.PUBLIC, credential=get_credential()
)
private_note = note.Note(
    aid=bvid2aid("BV18d4y1L7KB"),
    note_id=39719442425318400,
    note_type=note.NoteType.PRIVATE,
    credential=get_credential(),
)


async def test_a_public_Note_markdown_get_content():
    await public_note.fetch_content()

    md = public_note.markdown()

    return md


async def test_b_public_Note_json_get_content():
    await public_note.fetch_content()

    js = public_note.json()

    return js


async def test_c_public_Note_get_info():
    return await public_note.get_info()


async def test_d_private_Note_markdown_get_content():
    await private_note.fetch_content()

    md = private_note.markdown()

    return md


async def test_e_private_Note_json_get_content():
    await private_note.fetch_content()

    json = private_note.json()

    return json


async def test_f_private_Note_get_info():
    return await public_note.get_info()
