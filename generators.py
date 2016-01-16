import random

class Generator:
    def __init__(self, *args, **kwargs):
        pass

    def size(self):
        return 1

    def apply_notes(self, chn, pat, strat, rhythm, bbeg, blen, kroot, kchord):
        pass

class Generator_Bass(Generator):
    def __init__(self, smp, *args, **kwargs):
        self.smp = smp

    def size(self):
        return 1

    def apply_notes(self, chn, pat, strat, rhythm, bbeg, blen, kroot, kchord):
        base = kchord.get_base_note()

        leadin = 0

        for row in xrange(bbeg, bbeg+blen, 1):
            if rhythm[row]&1:
                n = base-12 if random.random() < 0.5 else base
                pat.data[row][chn] = [n, self.smp, 255, 0, 0]

                if leadin != 0 and random.random() < 0.4:
                    gran = 2
                    count = 1

                    #if random.random() < 0.2:
                    #   gran = 1

                    if leadin > gran*2 and random.random() < 0.4:
                        count += 1
                        if leadin > gran*3 and random.random() < 0.4:
                            count += 1

                    for j in xrange(count):
                        pat.data[row-(j+1)*gran][chn] = [
                             base+12 if random.random() < 0.5 else base
                            ,self.smp
                            ,0xFF
                            ,ord('S')-ord('A')+1
                            ,0xC0 + random.randint(1,2)
                        ]

                if random.random() < 0.2:
                    pat.data[row][chn][0] += 12
                    if random.random() < 0.4:
                        pat.data[row][chn][3] = ord('S')-ord('A')+1
                        pat.data[row][chn][4] = 0xC0 + random.randint(1,2)
                    else:
                        pat.data[row+2][chn] = [254, self.smp, 255, 0, 0]

                leadin = 0
            else:
                leadin += 1

class Generator_AmbientMelody(Generator):
    MOTIF_PROSPECTS = [
        # 1-steps
        [1],
        [2],
        [3],

        # 2-steps
        [1,3],
        [2,3],
        [2,4],

        # niceties
        [5,7],
        [5,12],
        [7,12],
        [7],
        [5],
        [12],

        # 3-chords
        [3,7],
        [4,7],

        # 4-chords
        [3,7,10],
        [3,7,11],
        [4,7,10],
        [4,7,11],

        # turns and stuff
        [1,0],
        [2,0],
        [1,-1,0],
        [1,-2,0],
        [2,-1,0],
        [2,-2,0],
    ]

    def __init__(self, smp, *args, **kwargs):
        self.smp = smp
        self.beatrow = 2**random.randint(2,3)
        self.lq = 60
        self.ln = -1
        self.mq = []
        self.nq = []

    def size(self):
        return 1

    def apply_notes(self, chn, pat, strat, rhythm, bbeg, blen, kroot, kchord):
        base = kchord.get_base_note()
        if bbeg == 0:
            self.lq = base
            self.ln = -1
            self.mq = []
            self.nq = []

        pat.data[bbeg][chn] = [self.lq, self.smp, 255, 0, 0]
        self.nq.append(bbeg)
        #self.ln = self.lq

        stabbing = False

        row = bbeg
        while row < bbeg+blen:
            if pat.data[row][chn][0] != 253:
                self.nq.append(row)

                row += self.beatrow
                continue

            q = 60

            if self.mq:
                if stabbing or random.random() < 0.9:
                    n = self.mq.pop(0)
                    self.ln = n
                    pat.data[row][chn] = [n, self.smp, 255, 0, 0]
                    self.nq.append(row)

                    if not self.mq:
                        self.lq = n

                    if random.random() < 0.2 or stabbing:
                        row += self.beatrow // 2
                        stabbing = not stabbing
                    else:
                        row += self.beatrow
                else:
                    row += self.beatrow
            elif row-bbeg >= 2*self.beatrow and random.random() < 0.3:
                backstep = random.randint(3,min(10,row//(self.beatrow//2)))*(self.beatrow//2)
                print "back", row, backstep

                for i in xrange(backstep):
                    if row-bbeg >= blen:
                        break
                    pat.data[row][chn] = pat.data[row-backstep][chn][:]
                    n = pat.data[row][chn][0]
                    if n != 253:
                        self.ln = self.lq = n
                    row += 1
            else:
                if len(self.nq) > 5:
                    self.nq = self.nq[-5:]

                while True:
                    kk = False
                    while True:
                        rbi = random.choice(self.nq)
                        rbn = pat.data[rbi][chn][0]

                        if self.ln != -1 and abs(rbn-self.ln) > 12:
                            continue

                        break

                    m = None
                    print rbn
                    for j in xrange(20):
                        m = random.choice(self.MOTIF_PROSPECTS)

                        down = random.random() < (8.0+(self.ln-base))/8.0 if self.ln != -1 else 0.5

                        print m,rbn,down,base
                        if down:
                            m = [rbn-v for v in m]
                        else:
                            m = [rbn+v for v in m]


                        if self.ln == m[0]:
                            continue

                        k = True
                        for v in m:
                            if not (kchord.has_note(v) and kroot.has_note(v)):
                                k = False
                                break

                        if k:
                            kk = True
                            break

                    if kk:
                        break


                if rbn != self.ln:
                    m = [rbn] + m

                print m
                self.mq += m

                # repeat at same row

class Generator_Drums(Generator):
    def __init__(self, s_kick, s_hhc, s_hho, s_snare, *args, **kwargs):
        self.s_kick = s_kick
        self.s_hhc = s_hhc
        self.s_hho = s_hho
        self.s_snare = s_snare
        self.beatrow = 2**random.randint(1,2)

    def size(self):
        return 3

    def apply_notes(self, chn, pat, strat, rhythm, bbeg, blen, kroot, kchord):
        for row in xrange(bbeg,bbeg+blen,self.beatrow):
            vol = 255
            smp = self.s_hhc
            if not (rhythm[row]&2):
                if (row&8):
                    vol = 48
                if (row&4):
                    vol = 32
                if (row&2):
                    vol = 16
                if (row&1):
                    vol = 8

                if random.random() < 0.2:
                    smp = self.s_hho

            pat.data[row][chn] = [60, smp, vol, 0, 0]

        for row in xrange(bbeg,bbeg+blen,2):
            if random.random() < 0.1 and not rhythm[row]&1:
                pat.data[row][chn+1] = [60,self.s_kick,255,0,0]

        did_kick = False
        for row in xrange(bbeg,bbeg+blen,1):
            if rhythm[row]&1:
                if did_kick:
                    pat.data[row][chn+2] = [60,self.s_snare,255,0,0]
                else:
                    if random.random() < 0.1:
                        pat.data[row+2][chn+1] = [60,self.s_kick,255,0,0]
                    else:
                        pat.data[row][chn+1] = [60,self.s_kick,255,0,0]

                did_kick = not did_kick

class Generator_Breaks(Generator):
    def __init__(self, s_chunks, pitch=60, *args, **kwargs):
        self.s_chunks = s_chunks
        self.pitch = pitch
        self.beatrow = 4
    
    def size(self):
        return 1
    
    def apply_notes(self, chn, pat, strat, rhythm, bbeg, blen, kroot, kchord):
        for row in xrange(bbeg,bbeg+blen,self.beatrow):
            pat.data[row][chn] = [self.pitch, self.s_chunks[(row / self.beatrow) % len(self.s_chunks)], 255, 0, 0]


