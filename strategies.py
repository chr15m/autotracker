##########################
#                        #
#   RANDOCHORD FACTORY   #
#                        #
##########################

import random
from keys import Key_GenericOctave, Key_Minor, Key_Major
from it.pattern import Pattern

class Strategy:
    def __init__(self, *args, **kwargs):
        self.setup(*args,**kwargs)
        self.gens = []
        self.chused = 0

    def setup(self, *args, **kwargs):
        self.key = Key_GenericOctave(60)

    def gen_add(self, gen):
        self.gens.append((self.chused,gen))
        self.chused += gen.size()

    def get_key(self):
        return self.key

class Strategy_Main(Strategy):
    def setup(self, basenote, keytype, patsize, blocksize, *args, **kwargs):
        self.basenote = basenote
        self.keytype = keytype
        self.patsize = patsize
        self.blocksize = blocksize
        self.key = keytype(basenote)
        self.pats = []
        self.rspeed = 2**random.randint(2,3)

        self.rhythm = [3]+[0]*(self.rspeed-1)+[1]+[0]*(self.rspeed-1)
        self.rhythm *= (self.patsize//len(self.rhythm))

        self.pat_idx = 0

        self.newkseq()

    def newkseq(self):
        self.kseq = random.choice({
            Key_Minor: [
                [(0,Key_Minor),(-4,Key_Major),(5,Key_Major),(-2,Key_Major)],
                [(0,Key_Minor),(-2,Key_Major),(-4,Key_Major),(-5,Key_Minor)],
            ],
            Key_Major: [
                [(0,Key_Major),(-5,Key_Major),(-3,Key_Minor),(5,Key_Major)],
                [(0,Key_Major),(0,Key_Major),(-7,Key_Minor),(-5,Key_Major)],
            ],
        }[self.keytype])

        self.kseq2 = random.choice({
            Key_Minor: [
                [(3,Key_Major),(0,Key_Minor),(-4,Key_Major),(-2,Key_Major)],
                [(-4,Key_Major),(-2,Key_Major),(0,Key_Minor),(-2,Key_Major)],
            ],
            Key_Major: [
                [(2,Key_Minor),(0,Key_Major),(-3,Key_Minor),(0,Key_Major)],
                [(-3,Key_Minor),(-5,Key_Major),(-7,Key_Major),(-5,Key_Major)],
            ],
        }[self.keytype])

    def get_pattern(self):
        pat = Pattern(self.patsize)

        kseq = self.kseq2[:] if self.pat_idx % 8 >= 4 else self.kseq[:]

        for i in xrange(0,self.patsize,self.blocksize):
            k,kt = kseq.pop(0)
            kchord = kt(self.basenote+k)
            for chn,gen in self.gens:
                gen.apply_notes(chn, pat, self, self.rhythm, i, self.blocksize, self.key, kchord)

            kseq.append(k)

        self.pats.append(pat)

        self.pat_idx += 1

        return pat

    def get_key(self):
        return self.key

