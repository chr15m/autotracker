OGGS=$(wildcard samples/*.ogg) $(wildcard samples/**/*.ogg)
WAVS := $(OGGS:.ogg=.wav)

all: $(WAVS)

%.wav: %.ogg
	oggdec "$<"

