import math
import numpy as np

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

def gen_dtmf_seq(buttons, sample_freq, tone_dur_seconds, gap_dur_seconds, mag):
    result = np.array([])
    for button in buttons:
        # Tone
        result = np.append(result, gen_dtmf(button, sample_freq, tone_dur_seconds, mag))
        # Silence
        result = np.append(result, gen_silence(sample_freq, gap_dur_seconds))
    return result
