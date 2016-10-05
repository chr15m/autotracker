(defn random-rhythm-loop [rnd loop-length]
  (let [[freq (rnd.choice [1 1 2 2 2 3 3 4 4 4 5 6 6 7 8 8 8])]
        [phase (rnd.randint 0 (- loop-length 1))]]
    (list-comp (int (not (% (+ r phase) freq))) [r (range loop-length)])))

(defn genetic-rhythm-loop [rnd loop-length]
  (let [[num-variants (rnd.randint 1 5)]
        [variants (list-comp (random-rhythm-loop rnd loop-length) [v (range num-variants)])]]
    (list-comp (get (rnd.choice variants) l) [l (range loop-length)])))

