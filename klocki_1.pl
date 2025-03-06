%Program:klocki_1
%baza danych o ukladzie klocków
%Definiowane predykaty:
%na/2
%===========
%na(X,Y)
%opis:spelniony, gdy klocek X lezy
%bezposrednio na klocku Y
%-----------
na(c,a).
na(c,b).
na(d,c).
%-----------
/*
Informacje o budowie programu:
Program sklada sie z 3 klauzul.
Program zawiera 1 definicje relacji.
Jest to relacja na/2.
Definicja relacji na/2 sklada sie z 
3 klauzul, ktore sa faktami.
*/
%Pod(X,Y) - klocek X lezy pod klockiem Y
pod(X,Y):-na(Y,X).
miedzy(X,Y,Z):-na(Z,X),na(X,Y).
miedzy(X,Y,Z):-na(Y,X),na(X,Z).
/*
Informacje o budowie programu:
Program składa się z 6 klauzul.
Program zawiera 3 definicje relacji.
Są to relacje na/2, pod/2 i między/3.
Definicja relacji na/2 składa się z 
3 klauzul,które są faktami.
Definicja relacji pod/2 składa się z 1 
klauzuli, która jest regułą.
Definicja relacji między/3 składa się
z 2 klauzul, które są regułami.
*/
