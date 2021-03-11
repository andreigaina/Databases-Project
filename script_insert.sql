
--INSERT INTO ADMINISTRATORI
INSERT INTO administratori VALUES(NULL,'Adriana Popa', 'adrianap@tuiasi.ro','0753246723');
INSERT INTO administratori VALUES(NULL,'Maricel Enache', 'maricel.ene@yahoo.com','0764389789');
INSERT INTO administratori VALUES(NULL,'Costel Lupascu', 'costell07@gamil.com','0755246723');
INSERT INTO administratori VALUES(NULL,'Denis Budeanu', 'denis.bud@yahoo.com','0764335789');
INSERT INTO administratori VALUES(NULL,'Monica Popa', 'monicapop@yahoo.com','0743246723');
INSERT INTO administratori VALUES(NULL,'Bogdan Pop', 'popbogdan@gmail.com','0724389789');
INSERT INTO administratori VALUES(NULL,'Andrei Loghin', 'loghinand@gamil.com','0745226723');
INSERT INTO administratori VALUES(NULL,'Alexandru Melinte', 'alex.mel@student.tuiasi.com','0744385789');
INSERT INTO administratori VALUES(NULL,'Denisa Maria', 'denisa100@yahoo.ro','0753436723');
INSERT INTO administratori VALUES(NULL,'Andrei Dima', 'dimaand@gmail.com','0764383289');
INSERT INTO administratori VALUES(NULL,'Bogdan Budeanu', 'bogdbud@ac.tuiasi.com','0734246723');
INSERT INTO administratori VALUES(NULL,'Radu Budeanu', 'radu.budeanu@yahoo.com','0764332989');
INSERT INTO administratori VALUES(NULL,'Yasmina Rachieriu', 'yasminaaa@yahoo.com','0777246723');
INSERT INTO administratori VALUES(NULL,'Adelina Cotiuga', 'aditacot@gmail.com','0748389789');
INSERT INTO administratori VALUES(NULL,'Iolanda Petras', 'iolipet@cuza.com','0720226723');
INSERT INTO administratori VALUES(NULL,'Iulica Izmana', 'iulicaizm@student.cuza.com','0759385789');
INSERT INTO administratori VALUES(NULL,'Ilie Cotiuga', 'cotiuga.ilie@student.ro','0736246723');
INSERT INTO administratori VALUES(NULL,'Manuel Cojocaru', 'manuelcoj@yahoo.com','0748589789');
INSERT INTO administratori VALUES(NULL,'Cosmin Cojocaru', 'cosmincojo@student.ac.tuiasi.com','0746246723');
INSERT INTO administratori VALUES(NULL,'Gabriel Vrabie', 'vrabioara.gabi@yahoo.com','0735335789');
  

--INSEST INTO FACULTATI
                                                
INSERT INTO facultati(cod_facultate,denumire,adresa) VALUES('IEEA','Facultatea de Inginerie Electrica, Energetica si Informatica',
        'Bulevardul Profesor Dr. doc. Dimitrie Mageron 21-23, Iasi 700050');
INSERT INTO facultati(cod_facultate,denumire,adresa) VALUES('AC','Facultatea de Automatica si Calculatoare',
        'Bulevardul Profesor Dr. doc. Dimitrie Mageron 27, Iasi 700050');
INSERT INTO facultati(cod_facultate,denumire,adresa) VALUES('ETTI','Facultatea de Electronica,Telecomunicatii si Tehnologii Informatiei',
        'Bulevardul Carol I nr. 11A, Iasi 700506');
INSERT INTO facultati(cod_facultate,denumire,adresa) VALUES('ARH','Facultatea de ARHITECTURA "G.M. Cantacuzino"',
        'Bulevardul Profesor Dimitrie Mangeron nr 3, Iasi 700050');
INSERT INTO facultati(cod_facultate,denumire,adresa) VALUES('MEC','Facultatea de Mecanica',
        'Bulevardul Profesor Dimitrie Mangeron 61-63, Iasi 700050'); 
INSERT INTO facultati(cod_facultate,denumire,adresa) VALUES('CMMI','Facultatea de Constructii Masini si Management Industrial',
        'Bulevardul Profesor Dimitrie Mangeron 59A, Iasi 700050'); 
INSERT INTO facultati(cod_facultate,denumire,adresa) VALUES('DIMA','Facultatea de Design Industrial si Managementul Afacerilor',
        'Bulevardul Profesor Dimitrie Mangeron 59B, Iasi 700050'); 
INSERT INTO facultati(cod_facultate,denumire,adresa) VALUES('SIM','Facultatea de Stiinta si Ingineria Materialelor',
        'Bulevardul Profesor Dimitrie Mangeron 30, Iasi 700050');     
INSERT INTO facultati(cod_facultate,denumire,adresa) VALUES('ICPM','Facultatea de Inginerie Chimica si Protectia Mediului',
        'Bulevardul Profesor Dimitrie Mangeron 70, Iasi 700050'); 
INSERT INTO facultati(cod_facultate,denumire,adresa) VALUES('HIDR','Facultatea de Hidrotehnica',
        'Bulevardul Profesor Dimitrie Mangeron 65, Iasi 700050');         
        
--INSERT INTO CAMINE       

INSERT INTO camine VALUES('T1','Campus Tudor Vladimirescu, 109-111, Iasi 700560',197,
    (SELECT id_administrator FROM administratori where telefon_administrator='0764389789'));
INSERT INTO camine VALUES('T2','Campus Tudor Vladimirescu, 109-111, Iasi 700560',197,
    (SELECT id_administrator FROM administratori where telefon_administrator='0744385789'));
INSERT INTO camine VALUES('T3','Campus Tudor Vladimirescu, 109-111, Iasi 700560',197,
    (SELECT id_administrator FROM administratori where telefon_administrator='0755246723'));
INSERT INTO camine VALUES('T4','Campus Tudor Vladimirescu, 109-111, Iasi 700560',197,
    (SELECT id_administrator FROM administratori where telefon_administrator='0764335789'));
INSERT INTO camine VALUES('T5','Campus Tudor Vladimirescu, 109-111, Iasi 700560',197,
    (SELECT id_administrator FROM administratori where telefon_administrator='0743246723'));
INSERT INTO camine VALUES('T7','Campus Tudor Vladimirescu, 109-111, Iasi 700560',148,
    (SELECT id_administrator FROM administratori where telefon_administrator='0724389789'));
INSERT INTO camine VALUES('T8','Campus Tudor Vladimirescu, 109-111, Iasi 700560',143,
    (SELECT id_administrator FROM administratori where telefon_administrator='0745226723'));
INSERT INTO camine VALUES('T9','Campus Tudor Vladimirescu, 109-111, Iasi 700560',110,
    (SELECT id_administrator FROM administratori where telefon_administrator='0753436723'));
INSERT INTO camine VALUES('T10','Campus Tudor Vladimirescu, 109-111, Iasi 700560',110,
    (SELECT id_administrator FROM administratori where telefon_administrator='0764383289'));
INSERT INTO camine VALUES('T11','Campus Tudor Vladimirescu, 109-111, Iasi 700560',100,
    (SELECT id_administrator FROM administratori where telefon_administrator='0734246723'));
INSERT INTO camine VALUES('T12','Campus Tudor Vladimirescu, 109-111, Iasi 700560',78,
    (SELECT id_administrator FROM administratori where telefon_administrator='0753246723'));
INSERT INTO camine VALUES('T13','Campus Tudor Vladimirescu, 109-111, Iasi 700560',76,
    (SELECT id_administrator FROM administratori where telefon_administrator='0735335789'));
INSERT INTO camine VALUES('T14','Campus Tudor Vladimirescu, 109-111, Iasi 700560',77,
    (SELECT id_administrator FROM administratori where telefon_administrator='0746246723'));
INSERT INTO camine VALUES('T15','Campus Tudor Vladimirescu, 109-111, Iasi 700560',78,
    (SELECT id_administrator FROM administratori where telefon_administrator='0748589789'));
INSERT INTO camine VALUES('T16','Campus Tudor Vladimirescu, 109-111, Iasi 700560',132,
    (SELECT id_administrator FROM administratori where telefon_administrator='0748589789'));
INSERT INTO camine VALUES('T17','Campus Tudor Vladimirescu, 109-111, Iasi 700560',274,
    (SELECT id_administrator FROM administratori where telefon_administrator='0736246723'));
INSERT INTO camine VALUES('T18','Campus Tudor Vladimirescu, 109-111, Iasi 700560',113,
    (SELECT id_administrator FROM administratori where telefon_administrator='0759385789'));
INSERT INTO camine VALUES('T19','Campus Tudor Vladimirescu, 109-111, Iasi 700560',110,
    (SELECT id_administrator FROM administratori where telefon_administrator='0753246723'));
INSERT INTO camine VALUES('T20','Campus Tudor Vladimirescu, 109-111, Iasi 700560',57,
    (SELECT id_administrator FROM administratori where telefon_administrator='0753246723'));
INSERT INTO camine VALUES('T21','Campus Tudor Vladimirescu, 109-111, Iasi 700560',61,
    (SELECT id_administrator FROM administratori where telefon_administrator='0753246723'));


--INSERT INTO CAMERE 

INSERT INTO camere VALUES(NULL,1,1,270.00,'C2P',(SELECT cod_camin FROM camine WHERE cod_camin='T1'));
INSERT INTO camere VALUES(NULL,30,2,135.00,'C2P',(SELECT cod_camin FROM camine WHERE cod_camin='T2'));
INSERT INTO camere VALUES(NULL,13,2,140.00,'C2P',(SELECT cod_camin FROM camine WHERE cod_camin='T3'));
INSERT INTO camere VALUES(NULL,40,2,140.00,'C2P',(SELECT cod_camin FROM camine WHERE cod_camin='T5'));
INSERT INTO camere VALUES(NULL,22,2,170.00,'I',(SELECT cod_camin FROM camine WHERE cod_camin='T7'));
INSERT INTO camere VALUES(NULL,112,2,175.00,'I',(SELECT cod_camin FROM camine WHERE cod_camin='T8'));
INSERT INTO camere VALUES(NULL,14,4,150.00,'C2P',(SELECT cod_camin FROM camine WHERE cod_camin='T9'));
INSERT INTO camere VALUES(NULL,24,4,165.00,'C2P',(SELECT cod_camin FROM camine WHERE cod_camin='T10'));
INSERT INTO camere VALUES(NULL,118,3,180.00,'C2P',(SELECT cod_camin FROM camine WHERE cod_camin='T11'));
INSERT INTO camere VALUES(NULL,29,3,185.00,'C2P',(SELECT cod_camin FROM camine WHERE cod_camin='T12'));
INSERT INTO camere VALUES(NULL,52,3,170.00,'C2P',(SELECT cod_camin FROM camine WHERE cod_camin='T13'));
INSERT INTO camere VALUES(NULL,43,3,175.00,'C2P',(SELECT cod_camin FROM camine WHERE cod_camin='T14'));
INSERT INTO camere VALUES(NULL,11,3,140.00,'C2P',(SELECT cod_camin FROM camine WHERE cod_camin='T15'));
INSERT INTO camere VALUES(NULL,31,2,200.00,'I',(SELECT cod_camin FROM camine WHERE cod_camin='T16'));
INSERT INTO camere VALUES(NULL,11,4,120.00,'C2C',(SELECT cod_camin FROM camine WHERE cod_camin='T17'));
INSERT INTO camere VALUES(NULL,21,4,110.00,'C2C',(SELECT cod_camin FROM camine WHERE cod_camin='T18'));
INSERT INTO camere VALUES(NULL,104,4,155.00,'C2C',(SELECT cod_camin FROM camine WHERE cod_camin='T19'));
INSERT INTO camere VALUES(NULL,2,2,300.00,'I',(SELECT cod_camin FROM camine WHERE cod_camin='T20'));
INSERT INTO camere VALUES(NULL,7,2,300.00,'I',(SELECT cod_camin FROM camine WHERE cod_camin='T21'));


--INSERT INTO TIPURI_ACTE

INSERT INTO tipuri_acte VALUES(NULL,'Contract de inchiriere');
INSERT INTO tipuri_acte VALUES(NULL,'Adeverinta membru asociatie');
INSERT INTO tipuri_acte VALUES(NULL,'Adeverinta orfan');
INSERT INTO tipuri_acte VALUES(NULL,'Adeverinta olimpic');
INSERT INTO tipuri_acte VALUES(NULL,'Adeverinta situatie financiara');
INSERT INTO tipuri_acte VALUES(NULL,'Adeverinta parinti in invatamant');
INSERT INTO tipuri_acte VALUES(NULL,'Copie buletin');
INSERT INTO tipuri_acte VALUES(NULL,'Cerere viza flotant');


--INSERT INTO STUDENTI

INSERT INTO studenti VALUES(NULL, 'Andrei Dima', 'Sat Parcovaci, NR. 103, 707168','Harlau','IS','andrei.dima@yahoo.com','0745238542',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='AC'));
INSERT INTO studenti VALUES(NULL, 'Bogdan Gogu', 'Sat Maxut, NR. 301, 705101','Deleni','IS','gogubogdan05@gmail.com','0769328459',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='ETTI'));
INSERT INTO studenti VALUES(NULL, 'Alexandru Soflete', 'Sat Agigea, Nr. 203, 707343','Agigea','CT','','0745289832',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='AC'));
INSERT INTO studenti VALUES(NULL, 'Bitoleanu Alexandru', 'Strada Omului, Bl.203, Et. 10, Ap. 50','Bucuresti','B','bitbitalex@gmail.com','0768437743',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='HIDR'));
INSERT INTO studenti VALUES(NULL, 'Aciu Lia Elena', 'Strada Motru, Bl. 25, Sc. A, Et. 5, Ap. 23','Buzau','BZ','liaelena@corporatie.com','0722394389',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='MEC'));
INSERT INTO studenti VALUES(NULL, 'Badea Nicolae', 'Strada Avram Iancu, Bl. 1, Sc. B, Et. 7, Ap. 11','Bacau','BC','badnicolae@yahoo.com','0756738262',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='IEEA'));
INSERT INTO studenti VALUES(NULL, 'Constantinescu Mircea', 'Sat Bichesti, Nr. 504 ','Focsani','VN','const.mircea@gmail.com','0776858732',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='ARH'));
INSERT INTO studenti VALUES(NULL, 'Darie Emanuel', 'Strada Crizantemelor, Bl. 13, Sc. C, Et. 1, Ap. 8','Roman','NT','manuel.darie@gmail.com','0747038273',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='CMMI'));
INSERT INTO studenti VALUES(NULL, 'Lascu Dan', 'Str. Frumoasa, Bl.20, Et. 3, Ap. 12 ','Ianca','BR','dan.lascu@yahoo.com','0743754787',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='DIMA'));
INSERT INTO studenti VALUES(NULL, 'Miclaus Simona', 'Oras Miclauseni, NR. 444, 705232','Miclauseni','IS','simonamic@gmail.com','0720943745',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='IEEA'));
INSERT INTO studenti VALUES(NULL, 'Nicoara Tania', 'Strada Turnurilor, Nr. 137A','Sighisoara','MS','tanianicoara.@yahoo.com','0743954895',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='ICPM'));
INSERT INTO studenti VALUES(NULL, 'Popa Valentin', 'Strada Aviatie, NR. 30','Iasi','IS','popavali@gmail.com','0774575033',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='SIM'));
INSERT INTO studenti VALUES(NULL, 'Rab Laura', 'Sat Badeni, NR. 199, 705656','Badeni','IS','rablaura@yahoo.com','0753090909',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='AC'));
INSERT INTO studenti VALUES(NULL, 'Sandu Florin', 'Stada Chiriilor, Bl. 37, Et. 10, Ap. 40','Cluj-Napoca','CJ','florins0304@gmail.com','0727284884',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='ETTI'));
INSERT INTO studenti VALUES(NULL, 'Stefanescu Florian', 'Strada Nucilor, Nr. 333, 706943','Albesti','VS',NULL,'0723458237',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='HIDR'));
INSERT INTO studenti VALUES(NULL, 'Voncila Ion', 'Strada Teilor, NR. 4, 703232','Voinesti','IS','ionvoncila@gmail.com','0734100760',
    (SELECT cod_facultate FROM facultati WHERE cod_facultate='ARH'));


--INSERT INTO PUNCTAJE
   
INSERT INTO punctaje VALUES ((SELECT  nr_matricol FROM studenti WHERE telefon_student='0745238542'),NULL,3.5,9.75,60,2);
INSERT INTO punctaje VALUES ((SELECT  nr_matricol FROM studenti WHERE telefon_student='0745289832'),NULL,10,10,60,2);
INSERT INTO punctaje VALUES ((SELECT  nr_matricol FROM studenti WHERE telefon_student='0769328459'),NULL,0,7.32,111,3);
INSERT INTO punctaje VALUES ((SELECT  nr_matricol FROM studenti WHERE telefon_student='0768437743'),NULL,1,8.69,180,4);
INSERT INTO punctaje VALUES ((SELECT  nr_matricol FROM studenti WHERE telefon_student='0722394389'),NULL,7.5,9.00,120,3);
INSERT INTO punctaje VALUES ((SELECT  nr_matricol FROM studenti WHERE telefon_student='0756738262'),NULL,1,9.5,60,2);
INSERT INTO punctaje VALUES ((SELECT  nr_matricol FROM studenti WHERE telefon_student='0776858732'),NULL,0,9.2,0,1);
INSERT INTO punctaje VALUES ((SELECT  nr_matricol FROM studenti WHERE telefon_student='0747038273'),NULL,0,7.8,0,1);
INSERT INTO punctaje VALUES ((SELECT  nr_matricol FROM studenti WHERE telefon_student='0743754787'),NULL,0,10,60,2);
INSERT INTO punctaje VALUES ((SELECT  nr_matricol FROM studenti WHERE telefon_student='0720943745'),NULL,10,4.2,50,3);
INSERT INTO punctaje VALUES ((SELECT  nr_matricol FROM studenti WHERE telefon_student='0743954895'),NULL,0,1,120,4);
INSERT INTO punctaje VALUES ((SELECT  nr_matricol FROM studenti WHERE telefon_student='0774575033'),NULL,5,8.69,175,4);
INSERT INTO punctaje VALUES ((SELECT  nr_matricol FROM studenti WHERE telefon_student='0753090909'),NULL,7.25,8,112,3);
INSERT INTO punctaje VALUES ((SELECT  nr_matricol FROM studenti WHERE telefon_student='0727284884'),NULL,0,10,0,1);
INSERT INTO punctaje VALUES ((SELECT  nr_matricol FROM studenti WHERE telefon_student='0723458237'),NULL,0,7.32,45,2);
INSERT INTO punctaje VALUES ((SELECT  nr_matricol FROM studenti WHERE telefon_student='0734100760'),NULL,0,8.69,180,4);

 --INSERT INTO OPTIUNI
 
INSERT INTO optiuni VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0745238542'),
    (SELECT cod_camin FROM camine where cod_camin='T2' ),(SELECT id_camera FROM camere  WHERE (cod_camin='T2' AND nr_camera=30)),
    (SELECT nr_matricol FROM studenti WHERE telefon_student='0769328459'),
    NULL,
    NULL);
INSERT INTO optiuni VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0769328459'),
    (SELECT cod_camin FROM camine where cod_camin='T2' ),(SELECT id_camera FROM camere  WHERE (cod_camin='T2' AND nr_camera=30)),
    (SELECT nr_matricol FROM studenti WHERE telefon_student='0745238542'),
    NULL,
    NULL);
INSERT INTO optiuni VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0745289832'),
    (SELECT cod_camin FROM camine where cod_camin='T7' ),(SELECT id_camera FROM camere  WHERE (cod_camin='T7' AND nr_camera=22)),
    NULL,
    NULL,
    NULL);
INSERT INTO optiuni VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0768437743'),
   (SELECT cod_camin FROM camine where cod_camin='T19' ),(SELECT id_camera FROM camere  WHERE (cod_camin='T19' AND nr_camera=104)),
   (SELECT nr_matricol FROM studenti WHERE telefon_student='0756738262'),
   (SELECT nr_matricol FROM studenti WHERE telefon_student='0776858732'),
   (SELECT nr_matricol FROM studenti WHERE telefon_student='0747038273'));
INSERT INTO optiuni VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0722394389'),
   (SELECT cod_camin FROM camine where cod_camin='T11' ),(SELECT id_camera FROM camere  WHERE (cod_camin='T11' AND nr_camera=118)),
   (SELECT nr_matricol FROM studenti WHERE telefon_student='0720943745'),
   (SELECT nr_matricol FROM studenti WHERE telefon_student='0743954895'),
    NULL);
INSERT INTO optiuni VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0743754787'),
    (SELECT cod_camin FROM camine where cod_camin='T1' ),(SELECT id_camera FROM camere  WHERE (cod_camin='T1' AND nr_camera=1)),
    NULL,
    NULL,
    NULL);
INSERT INTO optiuni VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0774575033'),
    (SELECT cod_camin FROM camine where cod_camin='T17' ),(SELECT id_camera FROM camere  WHERE (cod_camin='T17' AND nr_camera=11)),
   (SELECT nr_matricol FROM studenti WHERE telefon_student='0727284884'),
   (SELECT nr_matricol FROM studenti WHERE telefon_student='0723458237'),
   (SELECT nr_matricol FROM studenti WHERE telefon_student='0734100760'));
INSERT INTO optiuni VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0753090909'),
    (SELECT cod_camin FROM camine where cod_camin='T10' ),(SELECT id_camera FROM camere  WHERE (cod_camin='T10' AND nr_camera=24)),
    NULL,
    NULL,
    NULL);   

 --INSERT INTO ACTE

INSERT INTO acte VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0745238542'),
    (SELECT cod_tip_act FROM tipuri_acte WHERE denumire_tip_act='Contract de inchiriere'),
    TO_DATE('2020-09-14', ' YYYY-MM-DD'),'8BJ327a2');
INSERT INTO acte VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0745238542'),
    (SELECT cod_tip_act FROM tipuri_acte WHERE denumire_tip_act='Copie buletin'),
    TO_DATE('2020-09-15', ' YYYY-MM-DD'),'MZ783402');
INSERT INTO acte VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0745238542'),
    (SELECT cod_tip_act FROM tipuri_acte WHERE denumire_tip_act='Cerere viza flotant'),
    TO_DATE('2020-09-14', ' YYYY-MM-DD'),'FL029388');
INSERT INTO acte VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0745238542'),
    (SELECT cod_tip_act FROM tipuri_acte WHERE denumire_tip_act='Adeverinta orfan'),
    TO_DATE('2020-09-14', ' YYYY-MM-DD'),'ORF03894');
INSERT INTO acte VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0743754787'),
    (SELECT cod_tip_act FROM tipuri_acte WHERE denumire_tip_act='Contract de inchiriere'),
    TO_DATE('2020-09-15', ' YYYY-MM-DD'),'M8S325L2');
INSERT INTO acte VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0743754787'),
    (SELECT cod_tip_act FROM tipuri_acte WHERE denumire_tip_act='Copie buletin'),
    TO_DATE('2020-09-15', ' YYYY-MM-DD'),'KZ783912');
INSERT INTO acte VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0743754787'),
    (SELECT cod_tip_act FROM tipuri_acte WHERE denumire_tip_act='Adeverinta olimpic'),
    TO_DATE('2020-09-14', ' YYYY-MM-DD'),'OL785432');
INSERT INTO acte VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0722394389'),
    (SELECT cod_tip_act FROM tipuri_acte WHERE denumire_tip_act='Contract de inchiriere'),
    TO_DATE('2020-09-16', ' YYYY-MM-DD'),'93GSAD34');
INSERT INTO acte VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0722394389'),
    (SELECT cod_tip_act FROM tipuri_acte WHERE denumire_tip_act='Adeverinta membru asociatie'),
    TO_DATE('2020-09-16', ' YYYY-MM-DD'),'AS854923');
INSERT INTO acte VALUES((SELECT nr_matricol FROM studenti WHERE telefon_student='0722394389'),
    (SELECT cod_tip_act FROM tipuri_acte WHERE denumire_tip_act='Copie buletin'),
    TO_DATE('2020-09-16', ' YYYY-MM-DD'),'XZ234085');