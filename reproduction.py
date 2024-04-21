from parsing import *

#page5455 stuff
pages5455=reconstructor.reconstruct(list(list(parsed.find_data("segment"))[15].find_data("clause"))[-2])\
+ reconstructor.reconstruct(list(list(parsed.find_data("segment"))[15].find_data("clause"))[-1])
pages5455_indexes=list(map(lambda x: runeToIndex(x),filter(lambda x: x in alphabet, pages5455)))

def count_duplicates(numbers):
    count = 0
    for i in range(len(numbers) - 1):
        if numbers[i] == numbers[i + 1]:
            count += 1
    return count

def subtract_kth_previous_mod_29(numbers,k,skips={}):
    result = [*numbers[0:k]]  # Initialize the result list with the first k numbers
    skip=0
    for i in range(k, len(numbers)):
            if numbers[i] in skips:
                #do not modify this number
                result.append(numbers[i])
                #we should skip it when modifying other numbers
                skip += 1
            else:
                # Subtract the previous number mod 29 and append to the result list
                # except if we skipped, use the last unused number that isn't skipped 
                result.append((numbers[i] - numbers[i - k - skip]) % 29)
                skip = max(0,skip-1)
    return result

def freq_list(indexes):
    freqs = [0 for a in gematria_primus]
    for a in indexes:
        freqs[a] += 1
    return freqs

def indexOfCoincidence(indexes):
    return (1.0/(len(indexes)* (len(indexes)-1))) * sum([(a * (a-1)) for a in freq_list(indexes)])

#TODO: this is busted
def indexOfCoincidenceWithPeriodK(indexes,k,skips={}):
    ioc=0
    for i in range(0,k):
        ioc+=indexOfCoincidence(list(filter(lambda a: a not in skips, indexes[i::k])))
    return ioc/k

from collections import defaultdict
def fold_dicts(dicts):
    folded_dict = defaultdict(int)
    for d in dicts:
        for key, value in d.items():
            folded_dict[key] += value
    return dict(folded_dict)

def subtract_keystream_mod_29(numbers,keystream):
    result = []  # Initialize the result list with the first k numbers
    for i in range(0, len(numbers)):
        # Subtract the keystream mod 29 and append to the result list
        result.append((numbers[i] - keystream[i%len(keystream)]) % 29)
    return result

def index_all(a,l):
    return [i for i, x in enumerate(l) if x == a]

for i in range(1,14):
    print("0,%d:" % i)
    print(indexOfCoincidenceWithPeriodK(pages5455_indexes,i)*29)
        
for j in range(1,14):
    for i in range(1,14):
        print("%d,%d:" % (j, i))
        print(indexOfCoincidenceWithPeriodK(subtract_kth_previous_mod_29(pages5455_indexes,j),i)*29)


