lubi(marcin,gitara).
lubi(magda,ksiazki).
lubi(piotr,gitara).
lubi(ola,sport).
lubi(ania,Y):-lubi(magda,Y).
hobby(X,Y):-lubi(X,Z),lubi(Y,Z).
