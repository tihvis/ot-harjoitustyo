# Vaatimusmäärittely

## Sovelluksen kuvaus

Sovelluksen avulla käyttäjä voi seurata ja pitää kirjaa omien opintojensa etenemisestä. Sovelluksella voi olla useita käyttäjiä, joilla jokaisella on omat yksilölliset tiedot opintojensa etenemisestä. Kaikki toiminnallisuudet ovat siis käyttäjäkohtaisia, eli jokainen käyttäjä voi nähdä, lisätä ja muokata vain omia kurssejaan. Sovelluksella on vain yhdenlaisia käyttäjiä, eli opiskelijoita. 

## Käyttöliittymäluonnos

Sovellus koostuu kuudesta eri näkymästä.

![](./kuvat/kayttoliittyma-hahmotelma.png)

Sovellus aukeaa kirjautumisnäkymään.

**Kirjautuminen**:
* käyttäjä voi siirtyä onnistuneen kirjautumisen jälkeen etusivulle.
* käyttäjä voi siirtyä uuden käyttäjätunnuksen luomiseen.

**Uusi käyttäjä**:
* käyttäjä voi luoda uuden käyttäjätunnuksen ja siihen liitetyn salasanan.

**Etusivu**:
* listaus käyttäjän käynnissä olevista kursseista, ja mahdollisuus avata jokaisesta tarkempi kurssinäkymä.
* painike uuden kurssin lisäämistä varten.
* painike, josta pääsee suoritettujen kurssien näkymään.
* uloskirjautumispainike, joka kirjaa käyttäjän ulos ja ohjaa takaisin kirjautumissivulle.

**Uusi kurssi**:
* käyttäjä voi tallentaa uuden kurssin sovellukseen täyttämällä sen nimen, opintopisteet ja mahdolliset tehtäväkohtaiset maksimipisteet.

**Kurssinäkymä**:
* käyttäjä voi nähdä montako pistettä jokaisesta kurssin osa-alueesta on suoritettu tähän asti, ja muokata suoritettujen pisteiden määrää.
* käyttäjä voi merkitä kurssin suoritetuksi.
* käyttäjä voi poistaa kurssin.

**Suoritetut**:
* hyväksytysti suoritettujen opintopisteiden määrä ja keskiarvo.
* listaus suoritetuista kursseista.
* mahdollisuus siirtyä muokkaamaan/tarkastelemaan suoritetun kurssin sisältöä.
* painike etusivulle.

## Perusversion tarjoama toiminnallisuus

:sunglasses: = koko toiminnallisuus valmis ja testattu

### Ennen kirjautumista

- :sunglasses: Käyttäjä voi luoda järjestelmään käyttäjätunnuksen.
  - Käyttäjätunnuksen täytyy olla uniikki ja pituudeltaan vähintään 4 merkkiä.
  - Salasanan tulee olla vähintään 8 merkkiä pitkä, sisältäen vähintään yhden ison kirjaimen ja yhden numeron.
  - Mikäli käyttäjätunnus tai salasana eivät täytä vaadittuja kriteereitä, käyttäjälle tulee tästä ilmoitus.
- :sunglasses: Käyttäjä voi kirjautua järjestelmään.
  - Kirjautuminen onnistuu olemassaolevalla käyttäjätunnuksella ja salasanalla.
  - Käyttäjälle tulee virheilmoitus, mikäli käyttäjätunnusta ei olemassa, tai syötetty salasana on väärin.

### Kirjautumisen jälkeen

- :sunglasses: Käyttäjä näkee etusivulla listattuna hänen tällä hetkellä käynnissä olevat kurssit.
  - Jokaisen kurssin kohdalla on "Näytä/muokkaa"-painike, jota painamalla avautuu kyseisen kurssin oma kurssisivu.

- :sunglasses: Käyttäjä voi lisätä uuden oman suoritetun/käynnissä olevan kurssin järjestelmään.
  - Kurssin tietoihin saa tallennettua kurssin nimen, opintopistemäärän, sekä tiedot siitä, mistä eri osa-alueista (esim. tehtävät/harjoitustyö/koe/vertaisarviot, yms) kurssin suoritus koostuu.
  - Käyttäjä saa lisättyä jokaisen osa-alueen kohdalle niiden tuomat maksimipisteet.

- :sunglasses: Käyttäjä voi päivittää omien käynnissä olevien kurssien etenemistä.
  - Käyttäjä voi merkitä reaaliaikaisesti kurssin pistekertymän etenemistä, ja nähdä montako pistettä hän on kustakin osa-alueesta siihen asti suorittanut maksimiin verrattuna.
  - Käyttäjä voi merkitä kurssin suoritetuksi, jolloin lisäksi ilmoitetaan suorituspäivä, sekä saatu arvosana.
  - Käyttäjä voi poistaa kyseisen kurssin suorituksen.

- :sunglasses: Käyttäjä voi nähdä listan omista suoritetuista kursseistaan.
  - Näkymässä näkyy montako opintopistettä käyttäjä on suorittanut hyväksytysti, ja mikä hyväksytysti suoritettujen kurssien keskiarvo on.
  - Listauksessa näkyy lisäksi suoritettujen kurssien nimet, suorituspäivät, opintopisteet ja arvosana.
  - Listalla olevien suoritettujen kurssien tietoja pääsee muokkaamaan. Käyttäjä voi muokata kertyneitä pisteitä, muuttaa kurssin statuksen takaisin käynnissä olevaksi tai muokata kurssin arvosanaa tai suorituspäivämäärää. Tämä on hyödyllistä, jos käyttäjä haluaa myöhemmin uusia joitain kurssin osia, tai vaikkapa koko kurssin. 

- :sunglasses: Käyttäjä voi kirjautua ulos.
  - Uloskirjautumisen jälkeen käyttäjä ohjataan sisäänkirjautumissivulle.

## Jatkokehitysideoita

- Suoritettujen kurssien listausta voi järjestää suorituspäivämäärän, arvosanan tai kurssin nimen perusteella.
- Käyttäjä voi lisätä kurssitietoihin kommentteja.
- Kurssin tietoihin voi syöttää eri arvosanoihin vaaditut pisterajat.
- Käyttäjä voi poistaa käyttäjätunnuksensa ja sen myötä kaikki tallentamansa tiedot.
- Käyttäjä voi lisätä tarkempia tietoja kurssien osa-alueista, kuten deadlineja, missattuja pisteitä, yms.
- Käyttäjärooleihin lisätään opettaja, joka pystyy näkemään rajattuja tietoja opiskelijoiden opintojen etenemisestä. Tähän vaaditaan myös opiskelijan suostumus.
