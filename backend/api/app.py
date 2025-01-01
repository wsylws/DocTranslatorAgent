# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : app.py
# Time       ：2025/1/1 21:13
# Author     ：vince
# Description：
"""
import asyncio

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from core.service_map import reader_map, translator_map
from core.vo import TranslateRequest

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.post('/get_text_block')
def get_text_block(
    file: UploadFile = File(...),
    reader_name: str = Form(...)
):
    # Check file type
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type is not allowed")

    if file:
        res = reader_map.get(reader_name)(file.file).read()
        return JSONResponse(content=jsonable_encoder(res))

@app.post('/translate')
async def translate(
    request: Request,
    translate_request: TranslateRequest
):
    translator = translator_map.get(translate_request.translator)()
    async def event_stream():
        try:
            async for event in translator.async_translate(texts=translate_request.texts,
                                                          source_lang=translate_request.source_lang,
                                                          target_lang= translate_request.target_lang):
                if await request.is_disconnected():
                    break
                data = f'{event.model_dump_json()}'
                yield data
        except asyncio.CancelledError:
            pass

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get('/readers')
def get_readers():
    return JSONResponse(content=jsonable_encoder(list(reader_map.keys())))

@app.get('/translators')
def get_translators():
    return JSONResponse(content=jsonable_encoder(list(translator_map.keys())))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)