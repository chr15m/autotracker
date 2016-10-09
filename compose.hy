(require hy.contrib.loop)

; ***** Rhythm loops ***** ;

; returns [1 0 0 1 ... 0]
(defn random-rhythm-loop [rnd loop-length]
  (let [[freq (rnd.choice [1 1 2 2 2 3 3 4 4 4 5 6 6 7 8 8 8])]
        [phase (rnd.randint 0 (- loop-length 1))]]
    (list-comp (int (not (% (+ r phase) freq))) [r (range loop-length)])))

; returns [1 0 0 1 ... 0]
(defn genetic-rhythm-loop [rnd loop-length]
  (let [[num-variants (rnd.randint 1 5)]
        [variants (list-comp (random-rhythm-loop rnd loop-length) [v (range num-variants)])]]
    (list-comp (get (rnd.choice variants) l) [l (range loop-length)])))

; ***** Notes and melodies ***** ;

; eyeballed
(def note-jump-probabilities [5 5 5 5 5 7 7 7 3 3 3 6 6 2 2 4 4 1])

; returns a set of notes like [3 4 7 9]
(defn get-good-notes [rnd n]
  ; (random.sample (range 0 12) (+ (max sequence) 1))
  (loop [[c (dec n)] [notes [(rnd.randint 0 12)]]]
    (if (> c 0)
      (recur
        (dec c)
        (+ notes [(% (+ (get notes -1) (rnd.choice note-jump-probabilities)) 12)]))
      (sorted notes))))

