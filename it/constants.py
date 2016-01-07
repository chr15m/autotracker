# tunables.
SMP_FREQ = 44100
SMP_16BIT = True

# IT format constants. leave these alone.
IT_FLAG_STEREO = 0x01
IT_FLAG_VOL0MIX = 0x02 # absolutely useless since 1.04.
IT_FLAG_INSTR = 0x04
IT_FLAG_LINEAR = 0x08
IT_FLAG_OLDEFF = 0x10 # don't enable this, it's not well documented.
IT_FLAG_COMPATGXX = 0x20 # don't enable this, it's not well documented.
IT_FLAG_PWHEEL = 0x40 # MIDI-related, don't use
IT_FLAG_USEMIDI = 0x80 # undocumented MIDI crap, don't use
IT_SPECIAL_MESSAGE = 0x01 # MIDI-related, don't use
IT_SPECIAL_UNK1 = 0x02 # undocumented MIDI crap, don't use
IT_SPECIAL_UNK2 = 0x04 # undocumented MIDI crap, don't use
IT_SPECIAL_HASMIDI = 0x08 # undocumented MIDI crap, don't use
IT_SAMPLE_EXISTS = 0x01
IT_SAMPLE_16BIT = 0x02
IT_SAMPLE_STEREO = 0x04 # don't use, it's a modplugism.
IT_SAMPLE_IT214 = 0x08 # not supported yet - don't use.
IT_SAMPLE_LOOP = 0x10
IT_SAMPLE_SUS = 0x20 # mikmod doesn't like this, so be wary.
IT_SAMPLE_LOOPBIDI = 0x40
IT_SAMPLE_SUSBIDI = 0x80
# IT_CONVERT_* refers to the sample conversion flags.
# this is a VERY internal feature and not widely implemented.
# please ensure you ONLY use IT_CONVERT_SIGNED for normal samples.
# EXCEPTION: IT_CONVERT_DELTA + IT_SAMPLE_IT214 = IT215 compression.
IT_CONVERT_SIGNED = 0x01
IT_CONVERT_BIGEND = 0x02
IT_CONVERT_DELTA = 0x04
IT_CONVERT_BYTEDELT = 0x08
IT_CONVERT_TXWAVE = 0x10
IT_CONVERT_STEREO = 0x20

# anyhow, here's some code. enjoy.
IT_BASEFLG_SAMPLE = (
       IT_SAMPLE_EXISTS
    | (IT_SAMPLE_16BIT if SMP_16BIT else 0)
)
