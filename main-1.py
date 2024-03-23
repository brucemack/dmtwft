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
import scipy.io.wavfile as wavfile
import numpy as np

import utils.parse as parse
import utils.DTMF as DTMF
from utils.Token import Token
import utils.convert as convert 

def gen_audio_seq(symbols):
    result = np.array([])
    for symbol in symbols:
        _, data = wavfile.read("sounds/" + symbol + ".wav")
        result = np.append(result, data)
    return result

out_fn = "d:/demo.wav"

#samplerate = 44100
sample_rate = 8000
mag = 32767.0 / 2.0

script = []

# Add special constants
constants = dict()
constants["MPW"] = [ Token("99") ]
constants["CPW"] = [ Token("98") ]
constants["APW"] = [ Token("98") ]
constants["RBPW"] = [ Token("98") ]

# Read a SCOM Programmer file
with open('tests/sample-from-scom-resources.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        tokens = parse.tokenize_line(line.strip())
        if len(tokens) > 0:
            script.append(tokens)

try:
    # Convert the script to DTMF symbols
    dtmf_symbols = convert.convert_script_to_dtmf_symbols(constants, script, True, False)
    # Convert DTMF symbols to PCM tone data
    wav_data = DTMF.gen_dtmf_seq(dtmf_symbols, sample_rate, 0.075, mag / 2)
except Exception as ex:
    print("Program execution failure", ex)

print("Result: ", dtmf_symbols)

# Dump PCM to .WAV
wavfile.write(out_fn, sample_rate, wav_data.astype(np.int16))
