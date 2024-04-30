# Sisukas

Opintojen etenemistä havainnollistava sovellus, jonka avulla opiskelijat voivat pitää kirjaa meneillään olevista kursseistaan, sekä nähdä katsauksen jo suoritetuista kursseistaan.

[Viikko 5: Release](https://github.com/tihvis/ot-harjoitustyo/releases/tag/viikko5)

## Dokumentaatio

- [Vaatimusmäärittely](/study-app/dokumentaatio/vaatimusmaarittely.md)
- [Arkkitehtuurikuvaus](/study-app/dokumentaatio/arkkitehtuuri.md)
- [Käyttöohje](/study-app/dokumentaatio/kayttoohje.md)
- [Työaikakirjanpito](/study-app/dokumentaatio/tuntikirjanpito.md)
- [Changelog](/study-app/dokumentaatio/changelog.md)

## Asennus

1. Asenna riippuvuudet komennolla:
```
poetry install
```

2. Suorita projektin alustustoimenpiteet:
```
poetry run invoke build
```

3. Käynnistä sovellus:
```
poetry run invoke start
```

## Komentorivitoiminnot

Testien suorittaminen:
```
poetry run invoke test
```

Testikattavuusraportin generoiminen htmlcov-hakemistoon:

```
poetry run invoke coverage-report
```

Tiedoston [.pylintrc](https://github.com/tihvis/ot-harjoitustyo/blob/master/study-app/.pylintrc) määrittelemät tarkistukset:

```
poetry run invoke lint
```