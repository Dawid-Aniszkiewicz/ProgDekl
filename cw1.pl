%Program cw1
/*
lubi(X,Y).
sport(X).
jarosz(X).
czyta(X).
niepali(X).
*/
jarosz(ola).
jarosz(ewa).
jarosz(jan).
jarosz(pawel).

niepali(ola).
niepali(ewa).
niepali(jan).

czyta(ola).
czyta(iza).
czyta(piotr).

sport(ola).
sport(jan).
sport(piotr).
sport(pawel).

lubi(ola,X):-jarosz(X),sport(X).
lubi(ewa,X):-niepali(X),jarosz(X).
lubi(iza,X):-czyta(X).
lubi(iza,X):-niepali(X),sport(X).
lubi(janek,X):-sport(X).
lubi(piotr,X):-jarosz(X),sport(X).
lubi(piotr,X):-czyta(X).
lubi(pawel,X):-jarosz(X),sport(X),czyta(X).
