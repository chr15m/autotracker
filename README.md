Procedurally generate Impulse Tracker tunes using [Hy](http://hylang.org/) (Lisp).

	#!/usr/bin/env hy
	
	(import [autotracker.utils [track-builder]])
	(import [random [Random]])
	(import [math [sin]])
	
	(let [[rnd (Random)]
	      ; get impulse tracker file, sample loader, pattern creator
	      ; here our track is called "From Scratch" at 180 BPM with default pattern length of 128
	      [[it sample pattern] (track-builder "From Scratch" 180 128 "This is my message")]
	      ; create three samples
	      ; one loading from file
	      [s1 (sample "evolved" "samples/bassdrum-0-008307e09a04df9da674a0077f123c5960280db9-evolved.wav")]
	      ; one from an array of floats (sine wave)
	      [s2 (sample "sine" (list-comp (sin (* (/ s 4410) 440)) (s (range 4410))))]
	      ; then an array of samples by slicing up a wav into 8 chunks
	      [s3 (sample "amen" "autotracker/samples/amen.wav" :slices 8)]
	      [rows (xrange 128)]]
	  ; now we create patterns with the "pattern" function
	  ; each row/col trigger entry is an array like:
	  ; [midi-note sample volume fx-type fx-param]
	  ; e.g. in pattern 0, channel 0 - lists of row/col note triggers
	  (pattern 0 0 (list-comp [(rnd.randint 0 128) s1 255 0 0] [p rows]))
	  (pattern 1 1 (list-comp [(rnd.randint 0 128) s1 255 0 0] [p rows]))
	  (pattern 1 2 (list-comp [(rnd.randint 0 128) s2 255 0 0] [p rows]))
	  (pattern 2 0 (list-comp [60 (rnd.choice s3) 255 0 0] [p rows]))
	  ; write the impulse tracker file out to disk
	  (it.save "from-scratch.it"))

Based on autotracker.py by Ben Russell.

### Original license ###

> autotracker-bottomup - the quite a few times more ultimate audio experience
> by Ben "GreaseMonkey" Russell, 2011. Public domain.

