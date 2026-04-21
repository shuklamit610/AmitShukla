% Parent relationships
parent(john, mary).
parent(john, mike).
parent(susan, mary).
parent(susan, mike).

parent(mary, lisa).
parent(mary, tom).

parent(mike, anna).
parent(mike, joe).

% Gender
male(john).
male(mike).
male(tom).
male(joe).

female(susan).
female(mary).
female(lisa).
female(anna).

child(X, Y) :- parent(Y, X).

grandparent(X, Y) :-
    parent(X, Z),
    parent(Z, Y).

sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.

cousin(X, Y) :-
    parent(P1, X),
    parent(P2, Y),
    sibling(P1, P2).

descendant(X, Y) :-
    parent(Y, X).

descendant(X, Y) :-
    parent(Z, X),
    descendant(Z, Y).

