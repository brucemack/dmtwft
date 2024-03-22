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

dtmf = dict()

dtmf["1"] = ( 697, 1209 )
dtmf["2"] = ( 697, 1336 )
dtmf["3"] = ( 697, 1477 )
dtmf["A"] = ( 697, 1633 )

dtmf["4"] = ( 770, 1209 )
dtmf["5"] = ( 770, 1336 )
dtmf["6"] = ( 770, 1477 )
dtmf["B"] = ( 770, 1633 )

dtmf["7"] = ( 852, 1209 )
dtmf["8"] = ( 852, 1336 )
dtmf["9"] = ( 852, 1477 )
dtmf["C"] = ( 852, 1633 )

dtmf["*"] = ( 941, 1209 )
dtmf["0"] = ( 941, 1336 )
dtmf["#"] = ( 941, 1477 )
dtmf["D"] = ( 941, 1633 )

def gen_two_tones(freq_0, freq_1, sample_freq, dur_seconds, mag):
    samples = int(sample_freq * dur_seconds)
    omega_0 = 2.0 * 3.1415926 * (freq_0 / sample_freq)    
    series_0 = np.array([mag * math.cos(x * omega_0) for x in range(0, samples)])
    omega_1 = 2.0 * 3.1415926 * (freq_1 / sample_freq)    
    series_1 = np.array([mag * math.cos(x * omega_1) for x in range(0, samples)])
    return series_0 + series_1

def gen_silence(sample_freq, dur_seconds):
    samples = int(sample_freq * dur_seconds)
    return np.array([0 for _ in range(0, samples)])

def gen_dtmf(button, sample_freq, dur_seconds, mag):
    return gen_two_tones(dtmf[button][0], dtmf[button][1], sample_freq, dur_seconds, mag)

def gen_dtmf_seq(buttons, sample_freq, symbol_dur_seconds, mag):
    result = np.array([])
    for button in buttons:
        result = np.append(result, gen_dtmf(button, sample_freq, symbol_dur_seconds, mag))
        # Silence
        result = np.append(result, gen_silence(sample_freq, symbol_dur_seconds))
    return result

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
        if tokens[0] == "$WARMINIT":
            warm_state = True
        elif tokens[0] == "$ENDWARMINIT":
            warm_state = False
        elif tokens[0] == "$SKIP":
            skip_state = True
        elif tokens[0] == "$ENDSKIP":
            skip_state = False
        elif tokens[0] == "$PLAY":
            pass
        # Look for assignments
        elif tokens[1] == "=" and len(tokens) >= 3:
            # Here we pull off the first two tokens
            local_constants[tokens[0]] = tokens[2:]
        # Everything else is a normal command line
        else:
            if skip_state:
                continue
            print("----")
            print(tokens)
            # Resolve all named constants
            expanded_tokens = parse.expand_tokens(local_constants, tokens)
            # Convert to DTMF
            l = []
            for token in expanded_tokens:
                for s in parse.translate_token_to_dtmf_symbols(token):
                    dtmf_symbols = dtmf_symbols + s
    
    return dtmf_symbols

out_fn = "d:/demo.wav"
#samplerate = 44100
sample_rate = 8000
mag = 32767.0 / 2.0
#data = gen_dtmf_seq("139*", sample_rate, 0.1, mag / 2)
#data = np.append(data, data)
#data = np.append(data, gen_audio_seq("34"))
#wavfile.write(out_fn, sample_rate, data.astype(np.int16))

script = []

# Add special constants
constants = dict()

constants["MPW"] = [ "99" ]
constants["CPW"] = [ "98" ]
constants["APW"] = [ "98" ]
constants["RBPW"] = [ "98" ]

# Read a SCOM Programmer file
with open('tests/scom-demo-1.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        tokens = parse.tokenize_line(line.strip())
        if len(tokens) > 0:
            script.append(tokens)

dtmf_symbols = convert_script_to_dtmf_symbols(constants, script, True, False)

print("Result")
print(dtmf_symbols)

# Convert symbols to tones
wav_data = gen_dtmf_seq(dtmf_symbols, sample_rate, 0.075, mag / 2)
wavfile.write(out_fn, sample_rate, wav_data.astype(np.int16))


