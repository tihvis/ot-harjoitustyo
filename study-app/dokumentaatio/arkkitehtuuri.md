# Arkkitehtuurikuvaus

## Rakenne

Ohjelman rakenne noudattaa kolmitasoista kerrosarkkitehtuuria allaolevan kuvan mukaisesti.

![Luokkakaavio](./kuvat/luokkakaavio.png)

Luokat [UserService](https://github.com/tihvis/ot-harjoitustyo/blob/master/study-app/src/services/user_service.py) ja [CourseService](https://github.com/tihvis/ot-harjoitustyo/blob/master/study-app/src/services/course_service.py) vastaavat sovelluksen sovelluslogiikasta, ja tarjoavat toiminnalliset kokonaisuudet kaikille käyttöliittymän (UI) toiminnoille. 

UserService ja CourseService pääsevät käsiksi käyttäjiin ja kurssitietojen tallentamiseen kutsumalla luokkia [UserRepository](https://github.com/tihvis/ot-harjoitustyo/blob/master/study-app/src/repositories/user_repository.py) ja [CourseRepository](https://github.com/tihvis/ot-harjoitustyo/blob/master/study-app/src/repositories/course_repository.py), jotka vastaavat tiedon pysyväistallennuksesta SQLite-tietokantaan.

Sovelluksen loogisen tietomallin muodostaa käyttäjiä ja heidän kursseja kuvaavat luokat [User](https://github.com/tihvis/ot-harjoitustyo/blob/master/study-app/src/entities/user.py) ja [Course](https://github.com/tihvis/ot-harjoitustyo/blob/master/study-app/src/entities/course.py).

## Toimintalogiikka

Alla on kuvattu sovelluksen päätoiminnallisuuksien toimintalogiikkaa sekvenssikaavioina.

### Uuden käyttäjän luominen

Kun sovelluksen alkunäkymästä klikataan "Luo uusi käyttäjätunnus", käyttäjää pyydetään syöttämään käyttäjätunnus sekä salasana kahdesti. Jos syötetty käyttäjätunnus ei ole käytössä, ja syötetyt salasanat täsmäävät ja täyttävät annetut vaatimukset, etenee sovelluksen kontrolli seuraavasti:

```mermaid
 sequenceDiagram
    actor Käyttäjä
    participant UI
    participant UserService
    participant UserRepository
    participant Onni_Opiskelija

    Käyttäjä ->> UI: click "Rekisteröidy"
    UI ->> UserService: create_user("Onni_Opiskelija", "S4lasana", "S4lasana")
    UserService ->> UserRepository: find_by_username("Onni_Opiskelija")
    UserRepository -->> UserService: None
    UserService ->> Onni_Opiskelija: User("Onni_Opiskelija", "S4lasana")
    UserService ->> UserRepository: create(Onni_Opiskelija)
    UserRepository -->> UserService: user
    UserService -->> UI: user
    UI ->> UI: handle_show_main_view()
```

### Sisäänkirjautuminen

Kun sovelluksen kirjautumisnäkymässä syötetään olemassaoleva käyttäjätunnus ja siihen liittyvä oikea salasana, etenee sovelluksen kontrolli seuraavasti:

```mermaid
 sequenceDiagram
    actor Käyttäjä
    participant UI
    participant UserService
    participant UserRepository

    Käyttäjä ->> UI: click "Kirjaudu sisään"
    UI ->> UserService: login("Onni_Opiskelija", "S4lasana")
    UserService ->> UserRepository: find_by_username("Onni_Opiskelija")
    UserRepository -->> UserService: user
    UserService -->> UI: user
    UI ->> UI: handle_show_main_view()
```

### Uuden kurssin lisääminen

Kun sisäänkirjautunut käyttäjä klikkaa "Lisää uusi kurssi"-painiketta sovelluksen päänäkymästä, ja syöttää kurssin tiedot (nimi, opintopisteet, ja mahdolliset tehtävät ja niiden pistemäärät) etenee sovelluksen kontrolli seuraavasti:

```mermaid
 sequenceDiagram
    actor Käyttäjä
    participant UI
    participant CourseService
    participant CourseRepository
    participant course

    Käyttäjä ->> UI: click "Lisää uusi kurssi"
    UI ->> CourseService: create_course(1, "Ohjelmistotuotanto", 5, {1: 10, 5: 4})
    CourseService ->> course: Course(1, "Ohjelmistotuotanto", 5, {1: 10, 5: 4})
    CourseService ->> CourseRepository: create(course)
    CourseRepository -->> CourseService: course
    CourseService -->> UI: course
    UI ->> UI: handle_show_main_view()
```

### Meneillään olevan kurssin etenemisen päivittäminen

Kun sisäänkirjautunut käyttäjä on lisännyt uuden kurssin itselleen, hän pääsee päivittämään sen etenemistä klikkaamalla kyseisen kurssin kohdalla olevaa "Näytä/muokkaa" painiketta sovelluksen etusivulla. Kun käyttäjä on syöttänyt päivitetyt pistekertymät kurssin eri tehtäville, sovelluksen kontrolli etenee seuraavasti:

```mermaid
 sequenceDiagram
    actor Käyttäjä
    participant UI
    participant CourseService
    participant CourseRepository

    Käyttäjä ->> UI: click "Tallenna muutokset"
    UI ->> CourseService: update_course(course_id, {1: 5, 5: 2})
    CourseService ->> CourseRepository: update(course_id, {1: 5, 5: 2})
    UI ->> UI: handle_show_main_view()
```