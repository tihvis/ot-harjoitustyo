# Arkkitehtuurikuvaus

Ohjelman rakenne noudattaa kolmitasoista kerrosarkkitehtuuria allaolevan kuvan mukaisesti.

![Luokkakaavio](./kuvat/luokkakaavio.png)

Luokat [UserService](https://github.com/tihvis/ot-harjoitustyo/blob/master/study-app/src/services/user_service.py) ja [CourseService](https://github.com/tihvis/ot-harjoitustyo/blob/master/study-app/src/services/course_service.py) vastaavat sovelluksen sovelluslogiikasta, ja tarjoavat toiminnallisuudet kokonaisuudet kaikille käyttöliittymän (UI) toiminnoille. 

UserService ja CourseService pääsevät käsiksi käyttäjiin ja kurssitietojen tallentamiseen kutsumalla luokkia [UserRepository](https://github.com/tihvis/ot-harjoitustyo/blob/master/study-app/src/repositories/user_repository.py) ja [CourseRepository](https://github.com/tihvis/ot-harjoitustyo/blob/master/study-app/src/repositories/course_repository.py), jotka vastaavat tiedon pysyväistallennuksesta SQLite-tietokantaan.

Sovelluksen loogisen tietomallin muodostaa käyttäjiä ja heidän kursseja kuvaavat luokat [User](https://github.com/tihvis/ot-harjoitustyo/blob/master/study-app/src/entities/user.py) ja [Course](https://github.com/tihvis/ot-harjoitustyo/blob/master/study-app/src/entities/course.py).



