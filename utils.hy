(import os)
(import math)
(import random)
(import pprint)
(import [sys [stderr]])
(import [hashlib [sha256]])
(import [functools [partial]])

(import [it.itfile [ITFile]])
(import [it.sample [Sample_File Sample_FileSlice Sample_Raw]])
(import [it.pattern [Pattern]])

(def here (os.path.dirname __file__))

(defn fx-code [c] (- (ord (.lower c)) 96))

(defn get-wrapped [array index]
  (get array (% (int index) (len array))))

(defn null-pattern-fn [&rest args])

(defn value-or-callable [v &rest args] (if (callable v) (apply v args) v))

; taken from pure-data
(defn mtof [m]
  (cond
    [(<= m -1500) 0]
    [(> m 1499) (mtof 1499)]
    [true (* (math.exp (* m .0577622650)) 8.17579891564)]))

; taken from pure-data
(defn ftom [f]
  (if (> f 0)
    (* (math.log (* f .12231220585)) 17.3123405046)
    -1500))

(defn dir-to-samples [d itf] (list-comp
                               (itf.smp_add (Sample_File :name (os.path.basename f) :filename (os.path.join d f)))
                               [f (os.listdir d)]
                               (f.endswith ".wav")))

(defn dir-sample-list [dir starts-with]
  (list-comp (os.path.join dir f) [f (os.listdir dir)] (and (f.startswith starts-with) (f.endswith ".wav"))))

(defn print-through [message p] (print message p) p)

(defn prerr [&rest parts] (stderr.write (+ (.join " " (list-comp (str x) [x parts])) "\n")))

(defn generator-wrapper [generator-fn]
  (fn [channel-number pattern strategy rhythm beat-begin beats-length key-root key-chord]
    (let [[block (list (range beat-begin (+ beat-begin beats-length)))]
          [result (generator-fn
                   strategy.pat_idx
                   channel-number
                   block)]]
      ; apply the results to the pattern object
      (for [row (range (len result))]
        (set-pattern-value! pattern channel-number (+ row beat-begin) (get result row))))))

(defn set-pattern-value! [pattern channel-number row value]
  (setv (get (get pattern.data row) channel-number) value))

(defn add-pattern [i length pattern-number channel-number pattern-data]
  (let [[existing-pattern (> (len i.patlist) pattern-number)]
        [p (if existing-pattern (get i.patlist pattern-number) (Pattern length))]]
    (list-comp (set-pattern-value! p channel-number r (get pattern-data r)) [r (range length)])
    (if (not existing-pattern)
      (i.ord_add (i.pat_add p)))))

(defn add-sample [i name sample &rest args &kwargs kwargs]
  (cond
    [(= (type sample) unicode) (if (in "slices" kwargs)
                                 (list-comp (i.smp_add (Sample_FileSlice name
                                                                         :filename sample
                                                                         :slices (get kwargs "slices")
                                                                         :which s
                                                                         :loop (.get kwargs "loop" nil)))
                                   [s (range (get kwargs "slices"))])
                                 (i.smp_add (Sample_File name :filename sample)))]
    [(= (type sample) list) (i.smp_add (Sample_Raw name
                                                   :samples sample
                                                   :flags (.get kwargs "flags" 0)
                                                   :loop (.get kwargs "loop" {})))]))

(defn sample-length [i sample]
  (len (getattr (get i.smplist (- sample 1)) "data")))

(defn track-builder [track-name bpm pattern-length]
  (let [[i (ITFile track-name)]
        [s (partial add-sample i)]
        [p (partial add-pattern i pattern-length)]]
    (setv i.name track-name)
    (setv i.tempo bpm)
    [i s p]))

(defn weighted-choice [r vals]
  (r.choice (sum (list-comp (* [c] (get vals c)) [c vals]) [])))

(defn flip-pattern-data [pattern]
  (list-comp (list r) [r (apply zip pattern)]))

(defn post-process [pattern-list processing-fn]
  (list-comp (list-comp (processing-fn row pattern-data.rows) [row pattern-data.data]) [pattern-data pattern-list]))

(defn add-message [itf message]
  (setv itf.message (+ itf.message message "\n")))

(defn random-hash [r]
  (.hexdigest (sha256 (str (r.random)))))

(defn initial-hash [existing]
  (try
    (do (int existing 16) existing)
    (except [e Exception]
      (random-hash random))))

(defn extract-hash [argv &optional [which 0]]
  (let [[valid-hashes (list (filter (fn [arg] (try
                                                (if (and (> (len arg) 8) (int arg 16)) arg)
                                                (except [e Exception]))) argv))]]
    (if (> (len valid-hashes) which) (get valid-hashes which))))

(defn make-rng [&rest material]
  (random.Random (str material)))

