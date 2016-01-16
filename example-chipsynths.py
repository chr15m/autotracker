#!/usr/bin/env python
# Original by Ben "GreaseMonkey" Russell, 2011. Public domain.

import os
import sys
import random

from strategies import Strategy_Main
from generators import Generator_Drums, Generator_Bass, Generator_AmbientMelody
from keys import Key_Minor, Key_Major
from it.sample import Sample_KS, Sample_Kicker, Sample_NoiseHit, Sample_File

from autotracker import main, MIDDLE_C, samples

def bleep(t):
    return samples + "/" + random.choice([f for f in os.listdir(samples) if f.startswith("c64") and "-" + t + ".wav" in f])

def chipsynths(itf):
    # set the tempo
    itf.tempo = random.randint(90,160)
    
    SMP_KICK = itf.smp_add(Sample_Kicker(name = "Kick"))
    SMP_HHC = itf.smp_add(Sample_NoiseHit(name = "NH Hihat Closed", gvol = 32, decay = 0.03, filtl = 0.99, filth = 0.20))
    SMP_HHO = itf.smp_add(Sample_NoiseHit(name = "NH Hihat Open", gvol = 32, decay = 0.5, filtl = 0.99, filth = 0.20))
    SMP_SNARE = itf.smp_add(Sample_NoiseHit(name = "NH Snare", decay = 0.12, filtl = 0.15, filth = 0.149))

    SMP_HI = itf.smp_add(Sample_File(name = "bleep", filename=bleep("hi")))

    if random.randint(0, 1):
        SMP_BASS = itf.smp_add(Sample_KS(name = "KS Bass", freq = MIDDLE_C/4, decay = 0.005, nfrqmul = 0.5, filt0 = 0.2, filtn = 0.2, filtf = 0.005, length_sec = 0.7))
    else:
        SMP_BASS = itf.smp_add(Sample_File(name = "bleep-bass", filename=bleep("lo")))

    print "Generating patterns"
    strat = Strategy_Main(random.randint(50,50+12-1)+12, Key_Minor if random.random() < 0.6 else Key_Major, 128, 32)
    strat.gen_add(Generator_Drums(s_kick = SMP_KICK, s_snare = SMP_SNARE, s_hhc = SMP_HHC, s_hho = SMP_HHO))
    strat.gen_add(Generator_AmbientMelody(smp = SMP_HI))
    strat.gen_add(Generator_Bass(smp = SMP_BASS))

    for i in xrange(6):
        itf.ord_add(itf.pat_add(strat.get_pattern()))
    
    return itf

main(sys.argv, chipsynths)
