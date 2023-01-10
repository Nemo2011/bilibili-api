# bilibili_api.article
from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException
from bilibili_api import note
from .common import get_credential

public_note = note.Note(cvid=15160286, note_type=note.NoteType.PUBLIC, credential=get_credential())

async def test_a_Article_markdown_get_content():
    await public_note.fetch_content()

    md = public_note.markdown()

    return md


async def test_b_Article_json_get_content():
    await public_note.fetch_content()

    js = public_note.json()

    return js

async def test_c_Article_get_info():
    return await public_note.get_info()
