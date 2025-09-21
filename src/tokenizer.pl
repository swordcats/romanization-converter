letter(kk, c). 
letter(dd, c).
letter(tt, c).
letter(pp, c).
letter(bb, c).
letter(ss, c).
letter(jj, c).
letter(ch, c).
letter(ng, c).
letter(g, c).
letter(k, c).
letter(n, c).
letter(d, c).
letter(t, c).
letter(r, c).
letter(l, c).
letter(m, c).
letter(b, c).
letter(p, c).
letter(s, c).
letter(j, c).
letter(t, c).
letter(p, c).
letter(f, c).
letter(h, c).
letter(w, c).

letter(bs, c).
letter(rh, c).
letter(ks, c).
letter(nj, c).
letter(nh, c).
letter(rk, c).
letter(rm, c).
letter(rb, c).
letter(rp, c).

letter(yeo, v).
letter(yae, v).
letter(ye, v).
letter(oe, v).
letter(wi, v).
letter(oi, v).
letter(ee, v).
letter(ui, v).
letter(wa, v).
letter(ya, v).
letter(ae, v).
letter(wo, v).
letter(yu, v).
letter(yoo, v).
letter(eu, v).
letter(eo, v).
letter(yo, v).
letter(oo, v). % THIS IS NOT OFFICIAL, however it is common + unambiguous when it appears so i included it
letter(a, v).
letter(o, v).
letter(u, v).
letter(i, v).
letter(e, v).

consonant(L) :- letter(L, c).
vowel(L) :- letter(L, v).

% Prolog backtracking will check all of these rules and try to find a match. 
tokenize('', []). % This rule says that an empty string is a valid token.  It is a base case for recursion.

tokenize(Str, [H|NewT]) :-
    atom_chars(Str, [H|T]), % split a string into atoms: "bangtan" would become [b, a, n, g, t, a, n].  [H|T] means H = Head (b), T = Tail ([a, n, g, t, a, n])
    letter(H, _CV), % check if the Head is a valid letter
    atomic_list_concat(T, TAtom), % turn the tail from [a, n, g, t, a, n] into angtan
    tokenize(TAtom, NewT). % call tokenize again but this time with the tail (angtan) as an input

% This does the same as the other tokenize rule, except it checks the first two characters
tokenize(Str, [H|NewT]) :-
    atom_chars(Str, [H1, H2|T]), % "chekeu" becomes [c, h, e, k, e, u] H1 = c, H2 = h, T = [e, k, e, u]
    atom_concat(H1, H2, H), % concatenate the first two letters into one atom. c + h = ch
    letter(H, _CV),
    atomic_list_concat(T, TAtom),
    tokenize(TAtom, NewT).

% Does the same thing but with three characters
tokenize(Str, [H|NewT]) :-
    atom_chars(Str, [H1, H2, H3|T]),
    atom_concat(H1, H2, X),
    atom_concat(X, H3, H),
    letter(H, _CV),
    atomic_list_concat(T, TAtom),
    tokenize(TAtom, NewT).