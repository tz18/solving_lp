from parsing import *

#########information########
#information type 0 (i)   : pt[i] = ct[i]
#information type 1 (i,s,j) : key[j] = s - pt[i]
#information type 2 (i,s,j) : key[j] != ct[i] - s
##
##def gather_one_datum(ct, i, key_period, j, skip):
##    if ct[i] == skip:
##        return  [
##                #ct[i] is a true skip
##                #we learn about the pt
##                #pt[i] == ct[i]
##                #next j is j
##                ((0, i), j),
##                #ct[i] is a false skip
##                #we learn a little about the key but not much
##                #key[j] == skip - pt[i]
##                #next j is (j+1) % key_period
##                ((1, (i,skip,j)), (j + 1) % key_period)
##                ]
##    else:
##        #we rule out one letter for this position in the key
##        #next j is (j+1) % key_period
##        #key[j] != ct[i] - skip
##        return [((2, (i,skip,j)), (j + 1) % key_period)]
        
akoan2=reconstructor.reconstruct(list(parsed.find_data("segment"))[5])
akoan2_indexes=list(map(lambda x: runeToIndex(x),filter(lambda x: x in alphabet, akoan2)))

import numpy as np

#here skip_indexes is a list of indexes in the ordinals array that contain a true skip
def rule_out_key_letters_from_skips(ordinals, period, skip, skip_indexes):
    result = [set() for i in range(0,period)]
    k = 0;
    for i, a in enumerate(ordinals):
        if i not in skip_indexes:
            result[k].add(a-skip)
            k = (k + 1)%period
    return result

#49,58 the actual skip indexes in koan2
#subtract the alphabet from the ruled out indexes to get what's left
not_ruled_out=[set(i for i in range(0,len(gematria_primus))) - a for a in rule_out_key_letters_from_skips(akoan2_indexes,13,0,[49,58])]
print(not_ruled_out)

#the true key was still a possibility
for i,a in enumerate(list(map(letterToIndex, "FIRFUMFERENFE"))):
    print(a in not_ruled_out[i])

#we didn't narrow it down by much
print([len(set(i for i in range(0,len(gematria_primus))) - a) for a in rule_out_key_letters_from_skips(akoan2_indexes,13,0,[49,58])])
