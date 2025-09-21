from pyswip import Prolog
from collections import namedtuple

# Change this number to one to stop printing all results
DEBUG = 1

Syllable = namedtuple('Syllable', ['initial', 'vowel', 'final'])

# List of valid Korean initial consonants
#initials = ['g', 'd', 'b', 'r', 'n', 'm', 's', 'j', 'ch', 'k', 't', 'p', 'h', 'kk', 'tt', 'pp', 'ss', 'jj']
#vowels = ['a', 'ya', 'eo', 'yeo', 'o', 'yo', 'u', 'yu', 'eu', 'i', 'ae', 'yae', 'e', 'ye', 'oe', 'wi', 'ui', 'wa', 'wo', 'wae', 'we']
#finals = ['k', 't', 'p', 'l', 'n', 'm', 's', 'j', 'ch', 'k', 't', 'p', 'h', 'kk', 'tt', 'pp', 'ss', 'jj']

initials = {
    'g': 0,
    'kk': 1,
    'n': 2,
    'd': 3,
    'tt': 4,
    'dd': 4,
    'r': 5,
    'l': 5,
    'm': 6,
    'b': 7,
    'pp': 8,
    'bb': 8,
    's': 9,
    'ss': 10,
    'ng': 11,
    'w': 11, # w represents nothing, usually
    'j': 12,
    'jj': 13,
    'ch': 14,
    'k': 15,
    't': 16,
    'p': 17,
    'f': 17, # /f/ doesn't exist in korean but if something is romanized with f, it almost always becomes p
    'h': 18
}

vowels = {
    'a': 0,
    'ae': 1,
    'ya': 2,
    'yae': 3,
    'eo': 4,
    'e': 5,
    'yeo': 6,
    'ye': 7,
    'o': 8,
    'wa': 9,
    'wae': 10,
    'wi': 11,
    'oi': 11,
    'yo': 12,
    'u': 13,
    'oo': 13, # same as u
    'weo': 14,
    'wo': 14,
    'we': 15,
    'wi': 16,
    'yu': 17,
    'yoo': 17,
    'eu': 18,
    'ee': 19,
    'ui': 19,
    'i': 20
}

finals = {
    '': 0,
    'g': 1,
    'k': 1,
    'kk': 2,
    'ks': 3,
    'n': 4,
    'nj': 5,
    'nh': 6,
    'd': 7,
    'r': 8,
    'l': 8,
    'rk': 9,
    'rm': 10,
    'rb': 11,
    'rs': 12,
    'rt': 13,
    'rp': 14,
    'rh': 15,
    'm': 16,
    'b': 17,
    'bs': 18,
    's': 19,
    'ss': 20,
    'ng': 21,
    'j': 22,
    'ch': 23,
    't': 25,
    'p': 26,
    'h': 27
}

def tokenize(input_str: str) -> list[list[str]]:
    prolog = Prolog()

    prolog.consult("tokenizer.pl")

    tokenizations = []

    if DEBUG:
        print("---------------- Possible Tokenizations: ")

    for result in prolog.query(f"tokenize({input_str}, X)"):
        if DEBUG:
            print(result['X'])
        tokenizations.append(result['X'])

    return tokenizations

def syllabify(tokenizations: list[list[str]]) -> list[list[str]]:
    prolog = Prolog()

    prolog.consult("syllabifier.pl")

    syllabifications = []

    if DEBUG:
        print("---------------- Possible Syllabifications: ")

    for tokenization in tokenizations:
        for result in prolog.query(f"syllabify({tokenization}, X)"):
            if DEBUG:
                print(result['X'])
            syllabifications.append(result['X'])

    words = []

    for syllabification in syllabifications:
        current_word = [] 

        for syllable in syllabification:
            if len(syllable) == 3: # If there are three tokens in the syllable, then it has to be of the form IVF
                current_word.append(Syllable(syllable[0], syllable[1], syllable[2]))
            elif len(syllable) == 2:
                if syllable[0] in vowels: # Check if the first token is a vowel, i.e. of the form VF
                    current_word.append(Syllable('ng', syllable[0], syllable[1])) # add 'ng' in the beginning for Hangeul
                elif syllable[1] in vowels:
                    current_word.append(Syllable(syllable[0], syllable[1], None))
                else: 
                    raise ValueError(f"Invalid syllable formed!  Syllable: {syllable}")
            elif len(syllable) == 1: 
                current_word.append(Syllable('ng', syllable[0], None)) 

        words.append(current_word)

    return words

def convert(syllabifications: list[list[str]]) -> list[str]:
    if DEBUG:
        print("---------------- Possible Conversions: ")
    
    hangeul = {}

    for word in syllabifications:
        kor_str = ""
        syllabified_str = ""

        for syllable in word: 
            kor_num = 0xAC00 # This is the Unicode base

            if syllable.initial is not None: 
                kor_num += initials[syllable.initial] * 21 * 28
                if syllable.initial != 'ng': 
                    syllabified_str += syllable.initial

            kor_num += vowels[syllable.vowel] * 28
            syllabified_str += syllable.vowel

            if syllable.final is not None: 
                kor_num += finals[syllable.final]

                syllabified_str += syllable.final

            kor_str += chr(kor_num)
            syllabified_str += '.'
        
        # Korean = Syllable string
        # Example: 안녕하세요 = an.nyeong.ha.se.yo
        hangeul[kor_str] = syllabified_str[:-1]
    if DEBUG: 
        print(hangeul)
    return hangeul

if __name__ == '__main__':
    while True: 
        input_str = input("Please enter a romanization: ")

        tokenizations = tokenize(input_str)
        syllabifications = syllabify(tokenizations)
        conversions = convert(syllabifications)

        idx = 1

        if DEBUG:
            print("------------------------------------------------------------")

        for hangeul, syllable_str in conversions.items():

            print(f"({idx}) {hangeul} ({syllable_str})")
            idx += 1