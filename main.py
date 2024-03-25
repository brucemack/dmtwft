"""
* Copyright (C) 2024, Bruce MacKinnon KC1FSZ
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*
* NOT FOR COMMERCIAL USE WITHOUT PERMISSION.
"""
import time    
from typing import Union, Annotated
import struct
import wave
import io
import uuid 
import logging

import starlette.status as status
from fastapi import FastAPI, Request, Response, UploadFile, Form, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

# Other parts of this project
import utils.parse as parse
import utils.DTMF as DTMF
from utils.Token import Token
import utils.convert as convert 
import utils.sessions as sessions

VERSION = "0.3"

app = FastAPI()
app.mount("/assets", StaticFiles(directory="www/assets"), name="static")
templates = Jinja2Templates(directory="www/templates")
logger = logging.getLogger(__name__)

logger.info("Version %s", VERSION)

def get_default_session():
    s = dict()
    s["url_file"] = ""
    s["contents"] = None
    s["mpw"] = "99"
    s["cpw"] = "99"
    s["apw"] = "99"
    s["rbpw"] = "99"
    s["warminit"] = "on"
    s["tone_dur"] = "75"
    s["gap_dur"] = "75"
    s["sound"] = None
    s["message"] = None
    return s

def load_url(session):
    if session["url_file"]:
        # Load the URL
        try:
            response = requests.get(session["url_file"])
            if response.status_code == 200:
                contents = response.content.decode("utf8")
                session["contents"] = contents
            else:
                session["contents"] = None
                session["message"] = "URL not found"
        except Exception as ex:
            session["contents"] = None
            session["message"] = "Unable to load URL"

def generate_dtmf(session: dict):

    sample_rate = 8000
    mag = 32767.0 / 2.0
    script = []

    # Add special constants
    constants = dict()
    constants["MPW"] = [ Token(session["mpw"]) ]
    constants["CPW"] = [ Token(session["cpw"]) ]
    constants["APW"] = [ Token(session["apw"]) ]
    constants["RBPW"] = [ Token(session["rbpw"]) ]
    # Get parameters
    warm_init = session["warminit"] == "on"
    tone_dur = float(session["tone_dur"]) / 1000
    gap_dur = float(session["gap_dur"]) / 1000

    row = 1
    for line in session["contents"].splitlines():
        tokens = parse.tokenize_line(line.strip(), row)
        if len(tokens) > 0:
            script.append(tokens)
        row = row + 1

    try:
        # Convert the script to DTMF symbols
        dtmf_symbols = convert.convert_script_to_dtmf_symbols(constants, script, warm_init, False)
        # Convert DTMF symbols to PCM tone data
        wav_data = DTMF.gen_dtmf_seq(dtmf_symbols, sample_rate, tone_dur, gap_dur, mag / 2)
    except Exception as ex:
        print("Exception", ex)
        session["message"] = "Unable to process file: " + str(ex)
        return       

    # Dump PCM to .WAV.  
    with io.BytesIO() as of:
        with wave.open(of, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            wav.setnframes(len(wav_data))
            wav.writeframesraw(struct.pack("<{}h".format(len(wav_data)), *wav_data))
        # Load temp .WAV file into a byte array in the session
        of.seek(0)
        session["sound"] = of.read()

    logger.info("DTMF generation was successful. Samples: %d", len(wav_data))

# ===== Application Routes ====================================================

# The "main" screen:
@app.get("/robot", response_class=HTMLResponse)
async def robot_render(request: Request, 
                       demo: Union[str, None] = None,
                       session_key: Union[str, None] = Cookie(None)):
    
    session = sessions.get_session(session_key, get_default_session)

    # Look for the case where a demo URL was provided that pre-loads some
    # contents
    if demo:
        session["url_file"] = demo
        load_url(session)

    if session["contents"] == None:
        contents = ""
    else:
        contents = session["contents"]

    if session["message"] == None:
        message = ""
    else:
        message = session["message"]

    if session["sound"] == None:
        sound = "none"
    else:
        sound = "good"

    # Stage data for Jinja2 template
    context = { 
        "version": VERSION,
        "url_file": session["url_file"],
        "contents": contents,
        "mpw": session["mpw"],
        "cpw": session["cpw"],
        "apw": session["apw"],
        "rbpw": session["rbpw"],
        "tone_dur": session["tone_dur"],
        "gap_dur": session["gap_dur"],
        "warminit": session["warminit"],
        "message": message,
        "sound": sound
    }

    # These are one-time messages, so clear it after it's been used
    session["message"] = None

    t = templates.TemplateResponse(request=request, name="index.html", context=context)
    t.set_cookie(key="session_key", value=session["key"])
    return t

# Used when someone uploads a script file (POST)
@app.post("/robot-form-1a", response_class=HTMLResponse)
async def robot_post_1a(upload_file: UploadFile,
                     session_key: Union[str, None] = Cookie(None)):  

    session = sessions.get_session(session_key)
    session["contents"] = None
    contents = await upload_file.read()
    session["contents"] = contents.decode("utf8")
    # Always clear sound when the session is changed
    session["sound"] = None
   
    # Go back to the normal GET
    return RedirectResponse(
        '/robot', 
        status_code=status.HTTP_302_FOUND)    

# Used when someone changes the URL. This forces a re-load of the content
# by doing an HTTP GET from the specified location.
@app.post("/robot-form-1b", response_class=HTMLResponse)
async def robot_post_1b(url_file: Annotated[str, Form()] = "",
                     session_key: Union[str, None] = Cookie(None)):  

    session = sessions.get_session(session_key)
    session["url_file"] = url_file
    session["contents"] = None
    # Always clear sound when the session is changed
    session["sound"] = None    

    load_url(session)

    # Go back to the normal GET
    return RedirectResponse(
        '/robot', 
        status_code=status.HTTP_302_FOUND)    

# This is used when someone presses the Generate button
@app.post("/robot-form-2", response_class=HTMLResponse)
async def robot_post_2(mpw: Annotated[str, Form()], 
                       cpw: Annotated[str, Form()],
                       apw: Annotated[str, Form()],
                       rbpw: Annotated[str, Form()],
                       tone_dur: Annotated[str, Form()],
                       gap_dur: Annotated[str, Form()],
                       # Watch out, checkboxes don't get sent when unchecked
                       warminit: Annotated[str, Form()] = "off",
                       session_key: Union[str, None] = Cookie(None)):                        
    
    # Update session
    session = sessions.get_session(session_key)
    session["mpw"] = mpw
    session["cpw"] = cpw
    session["apw"] = apw
    session["rbpw"] = rbpw
    session["tone_dur"] = tone_dur
    session["gap_dur"] = gap_dur
    session["warminit"] = warminit
    # Always clear sound when the session is changed
    session["sound"] = None

    # Re-generate the sound
    generate_dtmf(session)

    # Add a sleep to improve ergonomics
    time.sleep(5)    

    # Go back to the normal GET
    return RedirectResponse(
        '/robot', 
        status_code=status.HTTP_302_FOUND)    

# This is what the audio player uses to pull the DTMF stream
@app.get("/robot/sound", response_class=Response)
async def robot_sound(session_key: Union[str, None] = Cookie(None)):
    session = sessions.get_session(session_key)
    if session["sound"] == None:
         raise HTTPException(status_code=404, detail="Item not found")
    else:
        headers = { "Cache-Control": "no-cache, max-age=0" }
        return Response(content=session["sound"], media_type="audio/wav", headers=headers)    
