
--Calculam punctajele studentilor
UPDATE punctaje 
    SET punctaj_total = CASE 
                            WHEN an_studiu=1 THEN (medie_student * 10)
                            ELSE
                                (medie_student * (numar_credite*10/(60.0*(an_studiu-1)))+  (bonus))
                        END

--Afisare nume camin cu administratorul corespunzator si numarul de telefon al acestuia
SELECT cod_camin, nume_administrator, telefon_administrator FROM camine c, administratori a
	WHERE c.id_administrator = a.id_administrator;

--Afisare camine si informatii despre conditii si pret
SELECT camine.cod_camin,nr_camera, nr_locuri, baie, pret_cazare FROM camine, camere 
    WHERE camine.cod_camin = camere.cod_camin;

--Afisare studenti cu informatii despre facultatea la care sunt si puntajele obtinute
SELECT nume_student, denumire, punctaj_total FROM facultati f,studenti s, punctaje p
    WHERE s.cod_facultate = f.cod_facultate AND s.nr_matricol =  p.nr_matricol;

--Afisare studenti cu optiunile lor
SELECT nume_student, o.cod_camin,nr_camera,(SELECT nume_student FROM studenti m where m.nr_matricol=o.coleg1) "Nume optiune coleg 1",
    (SELECT nume_student FROM studenti m where m.nr_matricol=o.coleg2) "Nume optiune coleg 2",
    (SELECT nume_student FROM studenti m where m.nr_matricol=o.coleg3) "Nume optiune coleg 3" FROM studenti s, optiuni o,camere c 
    WHERE s.nr_matricol = o.nr_matricol AND c.id_camera = o.id_camera;

--Afisare studenti cu  actele pe care le-au depus
SELECT nume_student, denumire_tip_act  "Denumire act",nr_act,data_act 
    FROM studenti s, acte,tipuri_acte tip WHERE s.nr_matricol=acte.nr_matricol AND tip.cod_tip_act=acte.cod_tip_act ORDER BY nume_student;

--Afisam tipul actelor si cati studenti au adus acel act si le ordonam dupa nume
SELECT denumire_tip_act "Denumire act",count(acte.cod_tip_act) "Numar exemplare"
    FROM  acte LEFT JOIN tipuri_acte tip ON acte.cod_tip_act=tip.cod_tip_act GROUP BY denumire_tip_act ORDER BY denumire_tip_act;
    
--Adaugam un bonus de Black Friday la studentii care au punctajul mai mic de 50
UPDATE punctaje  SET punctaj_total=punctaj_total+(50-punctaj_total) WHERE punctaj_total<50;

--Afisam numarul de camere total din campus
SELECT SUM(nr_camere) "Nr. total camere in campus" FROM camine; 

--Nr de camine in administrarea fiecarui admin
SELECT nume_administrator,count(c.id_administrator) "NR. CAMINE"
    FROM camine c LEFT JOIN administratori a ON c.id_administrator=a.id_administrator GROUP BY nume_administrator;

--Topul preferintelor caminelor
SELECT cod_camin,count(nr_locuri) "Nr camere" FROM camere
    GROUP BY cod_camin ORDER BY "Nr camere" DESC;

--Punctaj minim
SELECT nume_student,punctaj_total FROM  studenti s,punctaje p WHERE
     s.nr_matricol=p.nr_matricol AND punctaj_total=(SELECT min(punctaj_total) FROM punctaje);
	 
--Punctaj maxim     
SELECT nume_student,punctaj_total FROM  studenti s,punctaje p WHERE
     s.nr_matricol=p.nr_matricol AND punctaj_total=(SELECT max(punctaj_total) FROM punctaje);
	 
--Punctaj mediu
SELECT avg(punctaj_total) "Punctaj mediu"  FROM  studenti s left JOIN punctaje p ON
     s.nr_matricol=p.nr_matricol; 
	 
--Punctaje mai mari decat punctajul mediu
SELECT nume_student, punctaj_total FROM studenti s, punctaje p WHERE
       punctaj_total>(SELECT avg(punctaj_total) "Punctaj mediu"  FROM  studenti s left JOIN punctaje p ON
       s.nr_matricol=p.nr_matricol) AND s.nr_matricol=p.nr_matricol;
	   
--Afisare camine care au pretul mai mic de 150 si camine care  au pretul mai mare de 200
SELECT cod_camin, pret_cazare FROM camere cam WHERE cam.pret_cazare<150 UNION  SELECT cod_camin, pret_cazare FROM camere cam WHERE cam.pret_cazare>200;
 
 
 
 
 
 
 --INSERT-URI CU ERORI PENTRU A TESTA CONSTRANGERILE
--Unele constrangeri se vor repeta si de aceea vor aparea ca si exemplu o singura data
-- FORMAT MAIL GRESIT   
INSERT INTO studenti VALUES(NULL, 'Vlad Cristea', 'Strada Hotilor, NR. 103, 707458','Sibiu','SB','a@b.c','0732905427',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='AC'));

-- FORMAT TELEFON GRESIT
INSERT INTO studenti VALUES(NULL, 'Vlad Cristea', 'Strada Hotilor, NR. 103, 707458','Sibiu','SB','a@yahoo.com','7732905427',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='AC'));

--FORMAT JUDET GRESIT
--Judetul va fi un acronim valid din Romania
INSERT INTO studenti VALUES(NULL, 'Vlad Cristea', 'Strada Hotilor, NR. 103, 707458','Sibiu','sB','a@yahoo.com','0732905427',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='AC'));
    
--FORMAT NR_MATRICOL GRESIT
--Numarul matricol incepe cu cifra 4 si este format din 4 cifre
INSERT INTO studenti VALUES(3000, 'Vlad Cristea', 'Strada Hotilor, NR. 103, 707458','Sibiu','SB','a@yahoo.com','0732905427',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='AC'));

--FORMAT LOCALITATE GRESIT
--Localitatea nu va contine caractere speciale cu exceptia cratimei
INSERT INTO studenti VALUES(NULL, 'Vlad Cristea', 'Strada Hotilor, NR. 103, 707458','Sibiu.','SB','a@yahoo.com','0732905427',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='AC'));

--FORMAT DOMICILIU GRESIT
--Domiciliul nu va contine caractere speciale cu exceptia cratimei si a punctului
INSERT INTO studenti VALUES(NULL, 'Vlad Cristea', 'Strada=Hotilor, NR. 103!, 707458','Sibiu','SB','a@yahoo.com','0732905427',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='AC'));
	
--FORMAT CAMIN GRESIT
--Caminele incep cu litera T si contin maxim 2 cifre
INSERT INTO camine VALUES('A1','Campus Tudor Vladimirescu, 109-111, Iasi 700560',197,
    (SELECT id_administrator FROM administratori where telefon_administrator='0764389789'));
    
--FORMAT CAMIN GRESIT                                 
INSERT INTO facultati(cod_facultate,denumire,adresa) VALUES('aAAA','Facultatea de Inginerie Electrica, Energetica si Informatica',
        'Bulevardul Profesor Dr. doc. Dimitrie Mageron 21-23, Iasi 700050');

--FORMAT BAIE GRESIT   
--Tipul baii poate lua valorile C2P,C2C si I
INSERT INTO camere VALUES(NULL,2,2,270.00,'NOT',(SELECT cod_camin FROM camine WHERE cod_camin='T1')); 

--NOT unique key(nr_camera, cod_camin)
INSERT INTO camere VALUES(NULL,1,1,270.00,'C2P',(SELECT cod_camin FROM camine WHERE cod_camin='T1')); 

--NUMAR PERSOANE IN CAMERA DEPASIT  
--Numarul persoanelor in camera este cuprins intre 1 si 4 
INSERT INTO camere VALUES(NULL,2,5,270.00,'NOT',(SELECT cod_camin FROM camine WHERE cod_camin='T1')); 

--DATA DEPUNERE ACTE DEPASITA
--Data depunerii actelor nu se incadreaza in intervalul impus
INSERT INTO acte VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0769328459'),
    (SELECT cod_tip_act FROM tipuri_acte WHERE denumire_tip_act='Adeverinta situatie financiara'),
    TO_DATE('2019-09-22', ' YYYY-MM-DD'),'8BJ34453');
	
--DATA DEPUNERE ACTE INVALIDA
--Data este una din viitor
INSERT INTO acte VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0769328459'),
    (SELECT cod_tip_act FROM tipuri_acte WHERE denumire_tip_act='Adeverinta situatie financiara'),
    TO_DATE('2022-09-22', ' YYYY-MM-DD'),'8BJ34453');
	
--NR ACT INVALID
--NR_ACT trebuie sa contina doar cifre si litere
INSERT INTO acte VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0769328459'),
    (SELECT cod_tip_act FROM tipuri_acte WHERE denumire_tip_act='Adeverinta situatie financiara'),
    TO_DATE('2022-09-22', ' YYYY-MM-DD'),'8BJ3=453');