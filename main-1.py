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
import math
import wave
import struct
import uuid 

import utils.parse as parse
import utils.DTMF as DTMF
from utils.Token import Token
import utils.convert as convert 

in_fn = "tests/scom-w1tkz.txt"
#in_fn = "tests/w1dx-5k.txt"
#out_fn = "d:/demo.wav"
out_fn = "./demo.wav"

#samplerate = 44100
sample_rate = 8000
mag = 32767.0 / 2.0
tone_dur = 0.075
gap_dur = 0.075

script = []

# Add special constants
constants = dict()
constants["MPW"] = [ Token("99") ]
constants["CPW"] = [ Token("98") ]
constants["APW"] = [ Token("98") ]
constants["RBPW"] = [ Token("98") ]

row = 1
token_count = 0

# Read a SCOM Programmer file
with open(in_fn, 'r') as f:
    lines = f.readlines()
    for line in lines:
        tokens = parse.tokenize_line(line.strip(), row)
        if len(tokens) > 0:
            script.append(tokens)
            token_count = token_count + len(tokens)
        row = row + 1

print("There are", len(script), "lines of tokens")
print("There are", token_count, "tokens")

try:
    # Convert the script to DTMF symbols
    dtmf_symbols = convert.convert_script_to_dtmf_symbols(constants, script, True, False)
    print("There are", len(dtmf_symbols), "DTMF symbols")
    # Convert DTMF symbols to PCM tone data
    wav_data = DTMF.gen_dtmf_seq(dtmf_symbols, sample_rate, tone_dur, gap_dur, mag / 2)
except Exception as ex:
    print("Program execution failure", ex)

print("Result: ", dtmf_symbols)

# Dump PCM to .WAV
with wave.open(out_fn, "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(sample_rate)
    f.setnframes(len(wav_data))
    f.writeframesraw(struct.pack("<{}h".format(len(wav_data)), *wav_data))
