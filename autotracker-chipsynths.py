#!/usr/bin/env python
# Original by Ben "GreaseMonkey" Russell, 2011. Public domain.

import os
import sys
import random

from strategies import Strategy_Main
from generators import Generator_Drums, Generator_Bass, Generator_AmbientMelody
from keys import Key_Minor, Key_Major
from it.sample import Sample_KS, Sample_Kicker, Sample_NoiseHit, Sample_File
from it.itfile import ITFile
from name import randoname

#################
#               #
#   BOOTSTRAP   #
#               #
#################

if len(sys.argv) > 1:
    print "Seeding with ", sys.argv[1]
    random.seed(sys.argv[1])

print "Creating module"
itf = ITFile()

# path to this script's home
home = os.path.dirname(__file__)
samples = os.path.join(home, "samples")

print "Generating samples"
# these could do with some work, they're a bit crap ATM --GM
# note: commented a couple out as they use a fair whack of space and are unused.
MIDDLE_C = 220.0 * (2.0 ** (3.0 / 12.0))
#SMP_PIANO = itf.smp_add(Sample_KS(name = "KS Piano", freq = MIDDLE_C, decay = 0.07, nfrqmul = 0.02, filtdc = 0.1, filt0 = 0.09, filtn = 0.6, filtf = 0.4, length_sec = 1.0))
#SMP_HOOVER = itf.smp_add(Sample_Hoover(name = "Hoover", freq = MIDDLE_C))

def bleep(t):
    return samples + "/" + random.choice([f for f in os.listdir(samples) if f.startswith("c64") and "-" + t + ".wav" in f])

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

print "Saving"
if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    name = randoname()
itf.name = name
fname = "bu-%s.it" % name.replace(" ","-").replace("'","")
itf.save(fname)

print "Done"
print "Saved as \"%s\"" % fname
