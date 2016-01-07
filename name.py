import random

# pick a random name
RN_NOUNS = [
    ("cat","cats"),("kitten","kittens"),
    ("dog","dogs"),("puppy","puppies"),
    ("elf","elves"),("knight","knights"),
    ("wizard","wizards"),("witch","witches"),("leprechaun","leprechauns"),
    ("dwarf","dwarves"),("golem","golems"),("troll","trolls"),
    ("city","cities"),("castle","castles"),("town","towns"),("village","villages"),
    ("journey","journeys"),("flight","flights"),("place","places"),
    ("bird","birds"),
    ("ocean","oceans"),("sea","seas"),
    ("boat","boats"),("ship","ships"),
    ("whale","whales"),
    ("brother","brothers"),("sister","sisters"),
    ("viking","vikings"),("ghost","ghosts"),
    ("garden","gardens"),("park","parks"),
    ("forest","forests"),("ogre","ogres"),
    ("sweet","sweets"),("candy","candies"),
    ("hand","hands"),("foot","feet"),("arm","arms"),("leg","legs"),
    ("body","bodies"),("head","heads"),("wing","wings"),
    ("gorilla","gorillas"),("ninja","ninjas"),("bear","bears"),
    ("vertex","vertices"),("matrix","matrices"),("simplex","simplices"),
    ("shape","shapes"),
    ("apple","apples"),("pear","pears"),("banana","bananas"),
    ("orange","oranges"),
    ("demoscene","demoscenes"),
    ("sword","swords"),("shield","shields"),("gun","guns"),("cannon","cannons"),
    ("report","reports"),("sign","signs"),("year","years"),("age","ages"),
    ("blood","bloods"),("breed","breeds"),("monument","monuments"),
    ("cheese","cheeses"),("horse","horses"),("sheep","sheep"),("fish","fish"),
    ("dock","docks"),("tube","tubes"),("road","roads"),("path","paths"),
    ("tunnel","tunnels"),("retort","retorts"),
    ("toaster","toasters"),("goat","goats"),
    ("tofu","tofus"),("vine","vines"),("branch","branches"),

]

RN_ADJECTIVES = [
    "tense","grand","pleasing","absurd","offensive","crazed",
    "magic","lovely","tired","lively","tasty","jealous",
    "red","orange","yellow","green","blue","purple","pink","brown",
    "white","black","cheap","blazed","biased","sweet",
    "invisible","hidden","secret","long","short","tall","broken",
    "random","fighting","hunting","eating","drinking","drunk",
    "weary","walking","running","flying","strong","weak",
    "woeful","tearful","rich","poor","awoken","sacred",
]

RN_VERBS = [
    # TODO
]

RN_PATTERNS = [
    "the (n[0])'s (n[0,1])",
    "(N[0])'s (n[0,1])",
    "(n[0,1]) of (N[0,1])",
    "on the (n[0])'s (n[0,1])",
    "(n[0,1]) of the (n[0,1])",
    "the (a) (n[0,1])",
    "(A) (n[0])",
    "(a) (n[1])",
    "(a) and (a)",
    "(N[0,1]) and (N[0,1])",
]

def randoname():
    pat = random.choice(RN_PATTERNS)
    while "(" in pat:
        ps, po, pp = pat.partition("(")
        p, pc, pn = pp.partition(")")

        assert pc == ")", "expected ')' in name pattern"

        p = random.choice(p.split("|"))
        if p.startswith("n") or p.startswith("N"):
            idx = random.choice(eval(p[1:]))
            w = random.choice(RN_NOUNS)[idx]
            if idx in [0] and p.startswith("N"):
                if w[0] in "aeiouAEIOU":
                    p = "an " + w
                else:
                    p = "a " + w
            else:
                p = w
        elif p.startswith("a") or p.startswith("A"):
            w = random.choice(RN_ADJECTIVES)
            if p.startswith("A"):
                if w[0] in "aeiouAEIOU":
                    p = "an " + w
                else:
                    p = "a " + w
            else:
                p = w
        else:
            raise Exception("invalid name pattern type")

        pat = ps + p + pn

    return pat

