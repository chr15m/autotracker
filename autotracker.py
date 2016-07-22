#!/usr/bin/env python
# autotracker-bottomup - the quite a few times more ultimate audio experience
# by Ben "GreaseMonkey" Russell, 2011. Public domain.
#
#
#
# BUGS:
# - sometimes gets stuck in an infinite loop. attempted to alleviate it but it doesn't work.
# - i think it sometimes jumps further than an octave in some situations
# oh and:
# - has moments where it sounds bad. if you can fix this for good, let me know!

import os
import sys
import random
from hashlib import sha256

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

MIDDLE_C = 220.0 * (2.0 ** (3.0 / 12.0))

# path to this script's home
home = os.path.dirname(__file__)
samples = os.path.join(home, "samples")

def generate(argv, callback=None):
    if len(argv) > 1:
        name = argv[1]
    else:
        name = randoname()
    
    print "Seeding with '%s'" % name
    try:
        test_hash = int(name, 16)
    except:
        seed_hash = sha256(name).hexdigest()
    else:
        seed_hash = name
    random.seed(seed_hash)
    fname = "bu-%s.it" % name.replace(" ","-").replace("'","")
    
    print "Creating module"
    itf = ITFile(name, "seed-hash " + seed_hash + "\n")
    itf = callback(itf, name, fname, seed_hash)
    
    print "Saving"
    
    itf.name = name
    itf.save(fname)
    
    print "Done"
    print "Saved as \"%s\"" % fname

def default(itf):
    # set the tempo
    itf.tempo = random.randint(90,160)
    
    print "Generating samples"
    # these could do with some work, they're a bit crap ATM --GM
    # note: commented a couple out as they use a fair whack of space and are unused.
    SMP_GUITAR = itf.smp_add(Sample_KS(name = "KS Guitar", freq = MIDDLE_C/2, decay = 0.005, nfrqmul = 1.0, filt0 = 0.1, filtn = 0.6, filtf = 0.0004, length_sec = 1.0))
    SMP_BASS = itf.smp_add(Sample_KS(name = "KS Bass", freq = MIDDLE_C/4, decay = 0.005, nfrqmul = 0.5, filt0 = 0.2, filtn = 0.2, filtf = 0.005, length_sec = 0.7))
    #SMP_PIANO = itf.smp_add(Sample_KS(name = "KS Piano", freq = MIDDLE_C, decay = 0.07, nfrqmul = 0.02, filtdc = 0.1, filt0 = 0.09, filtn = 0.6, filtf = 0.4, length_sec = 1.0))
    #SMP_HOOVER = itf.smp_add(Sample_Hoover(name = "Hoover", freq = MIDDLE_C))
    
    SMP_KICK = itf.smp_add(Sample_Kicker(name = "Kick"))
    SMP_HHC = itf.smp_add(Sample_NoiseHit(name = "NH Hihat Closed", gvol = 32, decay = 0.03, filtl = 0.99, filth = 0.20))
    SMP_HHO = itf.smp_add(Sample_NoiseHit(name = "NH Hihat Open", gvol = 32, decay = 0.5, filtl = 0.99, filth = 0.20))
    SMP_SNARE = itf.smp_add(Sample_NoiseHit(name = "NH Snare", decay = 0.12, filtl = 0.15, filth = 0.149))
    
    print "Generating patterns"
    strat = Strategy_Main(random.randint(50,50+12-1)+12, Key_Minor if random.random() < 0.6 else Key_Major, 128, 32)
    strat.gen_add(Generator_Drums(s_kick = SMP_KICK, s_snare = SMP_SNARE, s_hhc = SMP_HHC, s_hho = SMP_HHO))
    strat.gen_add(Generator_AmbientMelody(smp = SMP_GUITAR))
    strat.gen_add(Generator_Bass(smp = SMP_BASS))
    
    for i in xrange(6):
        itf.ord_add(itf.pat_add(strat.get_pattern()))

    return itf

if __name__ == "__main__":
    generate(sys.argv, default)

