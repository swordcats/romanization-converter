% Initials
initial(g).
initial(d).
initial(b).
initial(r).
initial(l).
initial(n).
initial(m).
initial(s).
initial(j).
initial(ch).
initial(k).
initial(t).
initial(p).
initial(f).
initial(h).
initial(w).
initial(kk).
initial(tt).
initial(dd).
initial(pp).
initial(bb).
initial(ss).
initial(jj).

% Finals
final(k).
final(g).
final(t).
final(d).
final(r).
final(p).
final(l).
final(n).
final(m).
final(j).
final(s).
final(ch).
final(h).
final(ng).
final(kk).
final(ss).
final(bs).
final(rh).
final(ks).
final(nj).
final(nh).
final(rk).
final(rm).
final(rb).
final(rp).

% Vowels carry over from tokenizer.pl

% Syllable rules
syllable([]). % An empty syllable is a valid syllable
syllable([I, V, F]) :- initial(I), vowel(V), final(F).
syllable([I, V]) :- initial(I), vowel(V).
syllable([V, F]) :- vowel(V), final(F).
syllable([V]) :- vowel(V).

% An empty list is a valid syllabification.  This is the base case for the recursion
syllabify([], []).

% Check if the first element of the list forms a syllable
syllabify([H|T], [[H]|NewT]) :-
    syllable([H]),
    syllabify(T, NewT).
    
% Check if the first two elements of the list form a syllable
syllabify([H1, H2|T], [[H1, H2]|NewT]) :-
    syllable([H1, H2]),
    syllabify(T, NewT).

% Check if the first three elements of the list form a syllable
syllabify([H1, H2, H3|T], [[H1, H2, H3]|NewT]) :-
    syllable([H1, H2, H3]),
    syllabify(T, NewT).