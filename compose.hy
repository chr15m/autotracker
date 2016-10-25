(require hy.contrib.loop)

; ***** Rhythm loops ***** ;

; returns [1 0 0 1 ... 0]
(defn random-rhythm-loop [rnd loop-length]
  (let [[freq (rnd.choice [0 0 1 1 2 2 2 3 3 4 4 4 5 6 6 7 8 8 8])]
        [phase (rnd.randint 0 (- loop-length 1))]]
    (list-comp
      (int (and
             freq
             (not (% (+ r phase) freq))))
      [r (range loop-length)])))

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
  (loop [[notes [(rnd.randint 0 12)]]]
    (if (< (len notes) n)
      (recur
        (list (set (+ notes [(% (+ (get notes -1) (rnd.choice note-jump-probabilities)) 12)]))))
      (sorted notes))))

; uses one to three of the 'transform-' functions on existing notes set
(defn mutate-notes [rnd original-notes]
  (let [[mutation-count (rnd.randint 1 3)]]
    (loop [[x 0] [notes original-notes]]
      (if (< x mutation-count)
        (recur
          (inc x)
          ((rnd.choice [transform-notes-flip
                        transform-notes-multiply-prime])
                       rnd
                       notes)))
      notes)))

(defn transform-notes-flip [rnd notes]
  (let [[pivot (rnd.randint 1 12)]]
    (list-comp (% (+ (* (- n pivot) -1) pivot) 12) [n notes])))

(defn transform-notes-multiply-prime [rnd notes]
  (let [[multiplier (rnd.choice [2 3 5 7])]]
    (list-comp (% (* multiplier n) 12) [n notes])))

; composing sets of note patterns
(defn make-notes-progression [rnd]
  (let [[sections (rnd.choice [1 2 3])]]
    {:note-sets (make-notes-set rnd sections)
     :rootnote (rnd.randint 48 72)
     :pattern (sum (list-comp (* [p] (rnd.choice [2 4 8])) [p (range sections)]) [])}))

(defn make-notes-set [rnd sections]
  (let [[notes-count (rnd.choice [3 4 5])]]
    (loop [[notes-sets [(get-good-notes rnd notes-count)]]]
      (if (< (len notes-sets) sections)
        (recur
          (+ notes-sets
            [(mutate-notes rnd (get notes-sets -1))]))
        notes-sets))))

