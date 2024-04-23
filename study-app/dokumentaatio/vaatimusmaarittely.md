# Vaatimusmäärittely

## Sovelluksen kuvaus

Sovelluksen avulla käyttäjä voi seurata ja pitää kirjaa omien opintojensa etenemisestä. Sovelluksella voi olla useita käyttäjiä, joilla jokaisella on omat yksilölliset tiedot opintojensa etenemisestä. Kaikki toiminnallisuudet ovat siis käyttäjäkohtaisia, eli jokainen käyttäjä voi nähdä, lisätä ja muokata vain omia kurssejaan. Sovelluksella on vain yhdenlaisia käyttäjiä, eli opiskelijoita. 

## Käyttöliittymäluonnos

Sovellus koostuu viidestä eri näkymästä.

![](./kuvat/kayttoliittyma-hahmotelma.png)

Sovellus aukeaa kirjautumisnäkymään.

**Kirjautuminen**:
* käyttäjä voi siirtyä onnistumisen kirjautumisen jälkeen etusivulle.
* käyttäjä voi siirtyä uuden käyttäjätunnuksen luomiseen.

**Uusi käyttäjä**:
* käyttäjä voi luoda uuden käyttäjätunnuksen ja siihen liitetyn salasanan.

**Etusivu**:
* listaus käyttäjän käynnissä olevista kursseista, ja mahdollisuus avata jokaisesta tarkempi kurssinäkymä.
* painike uuden kurssin lisäämistä varten.
* painike, josta pääsee suoritettujen kurssien näkymään.
* uloskirjautumispainike, joka ohjaa takaisin kirjautumissivulle.

**Kurssinäkymä**:
* käyttäjä voi nähdä montako pistettä jokaisesta kurssin osa-alueesta on suoritettu tähän asti, ja muokata suoritettujen pisteiden määrää.
* käyttäjä voi merkitä kurssin suoritetuksi.
* käyttäjä voi poistaa kurssin.

**Suoritetut**:
* suoritettujen kurssien ja opintopisteiden määrä ja keskiarvo.
* mahdollisuus siirtyä muokkaamaan/tarkastelemaan kurssin sisältöä.
* painike etusivulle.

## Perusversion tarjoama toiminnallisuus

:white_check_mark: = valmis
:hourglass_flowing_sand: = työn alla


### Ennen kirjautumista

- Käyttäjä voi luoda järjestelmään käyttäjätunnuksen. :white_check_mark:
  - :white_check_mark: Käyttäjätunnuksen täytyy olla uniikki ja pituudeltaan vähintään 4 merkkiä.
  - :white_check_mark: Salasanan tulee olla vähintään 8 merkkiä pitkä, sisältäen vähintään yhden ison kirjaimen ja yhden numeron.
  - :white_check_mark: Mikäli käyttäjätunnus tai salasana eivät täytä vaadittuja kriteereitä, käyttäjälle tulee tästä ilmoitus.
- Käyttäjä voi kirjautua järjestelmään. :white_check_mark:
  - :white_check_mark: Kirjautuminen onnistuu olemassaolevalla käyttäjätunnuksella ja salasanalla.
  - :white_check_mark: Käyttäjälle tulee virheilmoitus, mikäli käyttäjätunnusta ei olemassa, tai syötetty salasana on väärin.

### Kirjautumisen jälkeen

- Käyttäjä näkee etusivulla listattuna hänen tällä hetkellä käynnissä olevat kurssit. :white_check_mark:

- Käyttäjä voi lisätä uuden oman suoritetun/käynnissä olevan kurssin järjestelmään. :white_check_mark:
  - :white_check_mark: Kurssin tietoihin saa tallennettua kurssin nimen, opintopistemäärän, sekä tiedot siitä, mistä eri osa-alueista (esim. tehtävät/harjoitustyö/koe/vertaisarviot, yms) kurssin suoritus koostuu.
  - :white_check_mark: Käyttäjä saa lisättyä jokaisen osa-alueen kohdalle niiden tuomat maksimipisteet.

- Käyttäjä voi päivittää omien käynnissä olevien kurssien etenemistä.
  - :white_check_mark: Käyttäjä voi merkitä reaaliaikaisesti kurssin pistekertymän etenemistä, ja nähdä montako pistettä kustakin osa-alueesta on siihen asti kerätty maksimiin verrattuna.
  - :white_check_mark: Käyttäjä voi merkitä kurssin suoritetuksi, jolloin lisäksi ilmoitetaan suorituspäivä, sekä saatu arvosana.
  - :white_check_mark: Käyttäjä voi poistaa kyseisen kurssin suorituksen.

- Käyttäjä voi nähdä listan omista suoritetuista kursseistaan. :hourglass_flowing_sand:
  - Listauksessa näkyy montako kurssia ja opintopistettä tähän asti on suoritettu, ja mikä suoritettujen kurssien keskiarvo on.
  - Listauksessa näkyy lisäksi suoritettujen kurssien nimet, suorituspäivät, opintopisteet ja arvosana.
  - Listalla olevien suoritettujen kurssien tietoja pääsee muokkaamaan. Tämä on hyödyllistä, jos käyttäjä haluaa esimerkiksi myöhemmin uusia kurssin kokeen ja korottaa sen arvosanaa.

- Käyttäjä voi kirjautua ulos. :white_check_mark:

## Jatkokehitysideoita

- Suoritettujen kurssien listausta voi järjestää suorituspäivämäärän, arvosanan tai kurssin nimen perusteella.
- Käyttäjä voi lisätä kurssitietoihin kommentteja.
- Kurssin tietoihin voi syöttää eri arvosanoihin vaaditut pisterajat.
- Käyttäjä voi poistaa käyttäjätunnuksensa ja sen myötä kaikki tallentamansa tiedot.
- Käyttäjä voi lisätä tarkempia tietoja kurssien osa-alueista, kuten deadlineja, missattuja pisteitä, yms.
- Käyttäjärooleihin lisätään opettaja, joka pystyy näkemään rajattuja tietoja opiskelijoiden opintojen etenemisestä. Tähän vaaditaan myös opiskelijan suostumus.
