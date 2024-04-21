from lptext import text
from lark import Lark
rune_parser = Lark(r"""
RUNE: "ᚠ"|"ᚢ"|"ᚦ"|"ᚩ"|"ᚱ"|"ᚳ"|"ᚷ"|"ᚹ"|"ᚻ"|"ᚾ"|"ᛁ"|"ᛄ"|"ᛇ"|"ᛈ"|"ᛉ"|"ᛋ"|"ᛏ"|"ᛒ"|"ᛖ"|"ᛗ"|"ᛚ"|"ᛝ"|"ᛟ"|"ᛞ"|"ᚪ"|"ᚫ"|"ᚣ"|"ᛡ"|"ᛠ"

runeword: RUNE ( RUNE )*

nonruneword: (DIGIT | LETTER)*

word: runeword | nonruneword

clause: ( word "-" )* word "."

paragraph: clause* "&"

segment: paragraph* "$"

chapter: segment* "§"

%ignore " "
%ignore "/"
%ignore "§"
%ignore "%"
%ignore "\n"
%import common.INT
%import common.WORD
%import common.DIGIT
%import common.LETTER
""", start='chapter', maybe_placeholders=False)

from lark.visitors import Visitor_Recursive
class Count(Visitor_Recursive):
    def __init__(self):
        self.count={"chapters":0,
           "segments":0,
           "paragraphs":0,
           "clauses":0,
           "words":0,
           "runewords":0,
           "nonrunewords":0,
           "runes":0}
    def chapter(self,tree):
        self.count["chapters"]+=1
    def segment(self,tree):
        self.count["segments"]+=1
    def paragraph(self,tree):
        self.count["paragraphs"]+=1
    def clause(self,tree):
        self.count["clauses"]+=1
    def runeword(self,tree):
        self.count["runewords"]+=1
        self.count["runes"]+=len(tree.children)
    def nonruneword(self,tree):
        self.count["nonrunewords"]+=1
    def word(self,tree):
        self.count["words"]+=1
    def getCount(self,tree):
        self.visit_topdown(tree)
        return self.count
        

from lark.reconstruct import Reconstructor
reconstructor=Reconstructor(rune_parser)
parsed=rune_parser.parse(text)

c=Count()
c.visit_topdown(parsed)
print(c.count)

unsolved_segments=list(parsed.find_data("segment"))[7:]

punctuation = set("$%-\n/.&§")
alphabet = set(text) - set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") - punctuation
gematria_primus=[('ᚠ', 'F', 2), ('ᚢ', 'U', 3), ('ᚦ', 'TH', 5), ('ᚩ', 'O', 7),
 ('ᚱ', 'R', 11), ('ᚳ', 'C', 13), ('ᚷ', 'G', 17), ('ᚹ', 'W', 19),
 ('ᚻ', 'H', 23), ('ᚾ', 'N', 29), ('ᛁ', 'I', 31), ('ᛄ', 'J', 37),
 ('ᛇ', 'EO', 41), ('ᛈ', 'P', 43), ('ᛉ', 'X', 47), ('ᛋ', 'S', 53),
 ('ᛏ', 'T', 59), ('ᛒ', 'B', 61), ('ᛖ', 'E', 67), ('ᛗ', 'M', 71),
 ('ᛚ', 'L', 73), ('ᛝ', 'NG', 79), ('ᛟ', 'OE', 83), ('ᛞ', 'D', 89),
 ('ᚪ', 'A', 97), ('ᚫ', 'AE', 101), ('ᚣ', 'Y', 103), ('ᛡ', 'IA', 107),
 ('ᛠ', 'EA', 109)]

def getIndexOfTuple(l, index, value):
    for pos,t in enumerate(l):
        if t[index] == value:
            return pos
    raise ValueError("list.index(x): x not in list")

def runeToIndex(rune):
    return getIndexOfTuple(gematria_primus, 0, rune)

def letterToIndex(letter):
    return getIndexOfTuple(gematria_primus,1,letter)

def gematriaToIndex(gematria):
    return getIndexOfTuple(gematria_primus,2,gematria)

def indexToRune(index):
    return gematria_primus[index][0]

def indexToLetter(index):
    return gematria_primus[index][1]
    
def indexToGematria(index):
    return gematria_primus[index][2]
