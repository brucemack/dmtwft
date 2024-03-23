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

def gen_audio_seq(symbols):
    result = np.array([])
    for symbol in symbols:
        _, data = wavfile.read("sounds/" + symbol + ".wav")
        result = np.append(result, data)
    return result

def convert_script_to_dtmf_symbols(constants, script, in_warm_init, in_cold_init):

    local_constants = dict(constants)

    warm_state = False
    cold_state = False
    skip_state = False
    dtmf_symbols = ""

    for tokens in script:  
        # Look for special commands
        if tokens[0].text == "$WARMINIT":
            warm_state = True
        elif tokens[0].text == "$ENDWARMINIT":
            warm_state = False
        elif tokens[0].text == "$SKIP":
            skip_state = True
        elif tokens[0].text == "$ENDSKIP":
            skip_state = False
        elif tokens[0].text == "$PLAY":
            pass
        # Look for assignments
        elif tokens[1].text == "=" and len(tokens) >= 3:
            # Here we pull off the first two tokens and everything else is the value
            # of the token.
            local_constants[tokens[0].text] = tokens[2:]
        # Everything else is a normal command line
        else:
            if skip_state:
                continue
            # Resolve all named constants
            expanded_tokens = parse.expand_tokens(local_constants, tokens)
            # Convert to DTMF
            for token in expanded_tokens:
                for s in parse.convert_token_to_dtmf_symbols(token):
                    dtmf_symbols = dtmf_symbols + s
    
    return dtmf_symbols

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
    dtmf_symbols = convert_script_to_dtmf_symbols(constants, script, True, False)
    # Convert DTMF symbols to PCM tone data
    wav_data = DTMF.gen_dtmf_seq(dtmf_symbols, sample_rate, 0.075, mag / 2)
except Exception as ex:
    print("Program execution failure", ex)

print("Result: ", dtmf_symbols)

# Dump PCM to .WAV
wavfile.write(out_fn, sample_rate, wav_data.astype(np.int16))


