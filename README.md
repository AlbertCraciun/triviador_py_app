# triviador_py_app

## Requirements
python 3.11.0 +
pip 21.2.4 +
pyqt5 5.15.4 +
```pip install pyqt5```

### draft of flow:

1. Ecranul 1 - ecranul de start:
- se adaugă echipele, introducând numele acestora în niște câmpuri și apăsând plus pentru a apărea noi câmpuri. Se pot introduce maxim 15 echipe
- se seteaza timpul de timer sau opțiunile de timer (timer on/off pentru selecția de categorii și număruld e secunde pentru selecția de răspuns la întrebări - minim 10s, maxim 60secunde)
- se selecteaza nuamrul de runde clasice, numarul de runde duel si nuamarul de runde campion (Classic Rounds, Duel Rounds, Champion Rounds)
- se apasă pe butonul de start

2. Ecranul 2 - ecranul cu selecția de categorii
- incepe timer-ul
- apar categoriile de intrebari si o varianta cu intrebare aleatorie
- la apasare apare ecranul 3

3. Ecranul 3 - intrebarea
- incepe timerul cu secundele selectate
- apare intrebarea aleatoare sau din categoria aleasa cu variantele de raspuns
- dupa ce timpul expira 
- apar casute in care se introduce litera aleasa de fiecare echipa si apoi se apasa submit answer

4. Ecranul 4 - validare raspunsuri si punctaje
- daca echipa a selectat intrebare aleatorie primeste punctaj dublu (40p)
- daca echipa a selectat intrebare dintr-o anume categorie primeste punctaj standard (20p)
- daca a raspuns gresit nu primeste puncte;
- celelalte echipe sunt punctate astfel: 0p pentru raspuns gresit, pe jumatatea punctajului standard (10p) pentru raspuns corect daca si echipa de rand a raspuns corect, 75% din punctajul standard daca echipa de rand a gresit, dar echipele au raspuns corect (15p)
- se afiseaza atat punctajul pe runda curenta, cat si punctajul total acumulat

5. de aici se repeta ecranele 2-3-4 pana se termina numarul de runde clasice

6. Incep rundele de duel, runde in care se poate fura punctajul. E un ecran de tranzitie pe care se da start runde duel

7. Ecran duel:
- echipa de rand alege echipa pe care o ataca si categoria de intrebare apoi (daca vrea)

8. Ecran intrebare duel:
- incepe timerul
- apare intrebare cu variante de raspuns
- la final de timer dispar raspunsurile si apar casutele pentru completarea literelor de catre echipe

9. Ecran optional: daca echipele care se dueleaza au acelasi raspuns corect la intrebarea cu variante atunci primesc o intrebare de departajare care are un raspuns numeric. Apar doar doua casute care pot fi completate de catre cele 2 echipe la expirarea timpului.

10. se dau intrebari pana una raspunde mai aproape de raspunsul corect decat cealalta echipa

11. Ecranul de rezultat:
- daca echipa care ataca a raspuns corect la intrebarea cu varianta si echipa care este atacata nu, atunci cea care a atacat primeste 20p, iar cea care a fost atacata pierde 20p
- restul echipelor primesc cate 5p daca au raspuns corect la intrebarea cu variante (indiferent de răspunsul echipelor de la duel)
- daca echipa care e atacata a raspuns corect la intrebarea cu variante si echipa care ataca a gresit, atunci se termina runda de duel, echipa care a raspuns corect (cea atacata, primind 10p)
- daca s-a ajuns la intrebari de departajare se aplica regulile de mai sus: celelalte echipe care nu fac parte din duel primesc puncte daor in functie de intrebarea cu variante, daca castiga duelul echipa care are a atacat primeste 20p, daca castiga duelul cea care s-a aparut atunci primeste 10p.

12. se repeta rundele de duel dupa numarul de runde selectat la inceput

13. Se afiseaza punctajul final si se trece la rundele de campioni (unde cele mai bune 2 echipe se lupta)
- echipa care a fost pe locul I, incepe cu 50p in plus.
- aceste runde nu au posibilitatea de alegere a categoriei
- dureaza cat a fost stabilit la inceput, dar cu -5secunde la timer
- punctajul de la aceste runde se calculeaza separat, incepand de la 0 (celalalt punctaj se salveaza)
- exista intrebari de departajare daca ambele echipe raspund corect la variante
- pentru echipa care castiga runda se dau 50p de punct
- daca numarul de runde de campionu s-a incheiat si intre punctajele celor doua echipe nu exista diferenta de 100 de puncte minim sau egal, atunci jocul se continua doar cu intrebari de departajare punctate cu 25p pana cand se ajunge la o diferenta de mai mare sau egala cu 100p pentru o echipa