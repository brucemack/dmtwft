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

dtmf_pairs = dict()

# The official DTMF frequency pairs
dtmf_pairs["1"] = ( 697, 1209 )
dtmf_pairs["2"] = ( 697, 1336 )
dtmf_pairs["3"] = ( 697, 1477 )
dtmf_pairs["A"] = ( 697, 1633 )

dtmf_pairs["4"] = ( 770, 1209 )
dtmf_pairs["5"] = ( 770, 1336 )
dtmf_pairs["6"] = ( 770, 1477 )
dtmf_pairs["B"] = ( 770, 1633 )

dtmf_pairs["7"] = ( 852, 1209 )
dtmf_pairs["8"] = ( 852, 1336 )
dtmf_pairs["9"] = ( 852, 1477 )
dtmf_pairs["C"] = ( 852, 1633 )

dtmf_pairs["*"] = ( 941, 1209 )
dtmf_pairs["0"] = ( 941, 1336 )
dtmf_pairs["#"] = ( 941, 1477 )
dtmf_pairs["D"] = ( 941, 1633 )

def gen_two_tones(freq_0, freq_1, sample_freq, dur_seconds, mag):
    samples = int(sample_freq * dur_seconds)
    omega_0 = 2.0 * 3.1415926 * (freq_0 / sample_freq)    
    omega_1 = 2.0 * 3.1415926 * (freq_1 / sample_freq)    
    return [ int(mag * math.cos(x * omega_0)) + int(mag * math.cos(x * omega_1)) for x in range(0, samples)]

def gen_silence(sample_freq, dur_seconds):
    samples = int(sample_freq * dur_seconds)
    return [0 for _ in range(0, samples)]
            
def gen_dtmf(button, sample_freq, dur_seconds, mag):
    return gen_two_tones(dtmf_pairs[button][0], dtmf_pairs[button][1], sample_freq, dur_seconds, mag)

def gen_dtmf_seq(buttons, sample_freq, tone_dur_seconds, gap_dur_seconds, mag):
    result = []
    # Add a leading silence 
    result = result + gen_silence(sample_freq, 2)
    # Add each DTMF button 
    for button in buttons:
        # Tone 
        result.extend(gen_dtmf(button, sample_freq, tone_dur_seconds, mag))
        # Silence
        result.extend(gen_silence(sample_freq, gap_dur_seconds))
    return result
