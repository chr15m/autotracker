#!/usr/bin/env python

import os
import sys
import random

from strategies import Strategy_Main
from generators import Generator_Breaks, Generator_Bass, Generator_AmbientMelody
from keys import Key_Minor, Key_Major
from it.sample import Sample_KS, Sample_Kicker, Sample_NoiseHit, Sample_File, Sample_FileSlice

from autotracker import main, MIDDLE_C

def breaks_and_chips(itf):
    pace = random.random()
    # set the tempo
    itf.tempo = int(pace * 65 + 120)

    # path to this script's home
    home = os.path.dirname(__file__)
    samples = os.path.join(home, "samples")

    print "Generating samples"
    MIDDLE_C = 220.0 * (2.0 ** (3.0 / 12.0))

    def brk():
        return samples + "/" + random.choice(["amen.wav", "think.wav"])

    def bleep(t):
        return samples + "/" + random.choice([f for f in os.listdir(samples) if f.startswith("c64") and "-" + t + ".wav" in f])

    which_break = brk()
    SMP_BREAK = [itf.smp_add(s) for s in [Sample_FileSlice(filename=which_break, which=x) for x in xrange(8)]]

    SMP_HI = itf.smp_add(Sample_File(name = "bleep", filename=bleep("hi")))

    if random.randint(0, 1):
        SMP_BASS = itf.smp_add(Sample_KS(name = "KS Bass", freq = MIDDLE_C/4, decay = 0.005, nfrqmul = 0.5, filt0 = 0.2, filtn = 0.2, filtf = 0.005, length_sec = 0.7))
    else:
        SMP_BASS = itf.smp_add(Sample_File(name = "bleep-bass", filename=bleep("lo")))

    print "Generating patterns"
    strat = Strategy_Main(random.randint(50,50+12-1)+12, Key_Minor if random.random() < 0.6 else Key_Major, 128, 32)
    strat.gen_add(Generator_Breaks(s_chunks=SMP_BREAK, pitch=int(pace * 12 + 54)))
    strat.gen_add(Generator_AmbientMelody(smp = SMP_HI))
    strat.gen_add(Generator_Bass(smp = SMP_BASS))

    for i in xrange(6):
        itf.ord_add(itf.pat_add(strat.get_pattern()))

    return itf

main(sys.argv, breaks_and_chips)
