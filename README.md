# μ-scale: uporabniška mikrostoritev

Ta repozitorij vsebuje izvorno kodo mikrostoritve za registracijo in prijavo uporabnikov, ki je del projekta μ-scale (microscale)
(glavni repozitorij je na voljo [tukaj](https://github.com/RSO-2024-Mikrovrtickarja/micro-scale)).

## 1. Arhitektura in CI/CD
Mikrostoritev je razvita z uporabo ogrodja [FastAPI](https://fastapi.tiangolo.com/) v [Pythonu](https://www.python.org/) 3.12+,
pri čemer za upravljanje odvisnosti in virtualnega Python okolja projekt uporablja orodje [Poetry](https://python-poetry.org/).

Mikrostoritev ob zagonu na vratih `8002` izpostavi:
- REST API, ki overjenemu uporabniku omogoča dostop do funkcionalnosti registracije in prijave.
- OpenAPI dokumentacijo, ki je na voljo na poti `/docs` (surova OpenAPI dokumentacija je na voljo na `/openapi.json`).

Ob spremembah na glavni veji (`main`) se v tem GitHub repozitoriju proži CI/CD cevovod, 
ki aplikacijo zapakira v vsebnik Docker in naloži na vsebniški register na oblaku Azure, 
kjer je projekt nameščen. Za več podrobnosti o namestitvi glej glavni repozitorij [tukaj](https://github.com/RSO-2024-Mikrovrtickarja/micro-scale).


## 2. Lokalno nameščanje
Za lokalno nameščanje, razvijanje in testiranje je potrebno namestiti sledeča orodja (navodila so prilagojena razvijanju na operacijskem sistemu Windows):
- [Python](https://www.python.org/) 3.12 ali več,
- [Poetry](https://python-poetry.org/) 1.8 ali več,
- [PostgreSQL](https://www.postgresql.org/) 16 ali več,
- [PowerShell 7](https://github.com/PowerShell/PowerShell).

Po namestitvi zgornjih orodij se je treba prepričati, da so orodja za ukazno vrstico od baze PostgreSQL
vnešeni v pot ("PATH"), saj bomo morali do njih dostopati v naslednjem koraku. Sedaj poženemo skripto
`./scripts/init-database.ps1`, ki bo inicializirala podatkovno bazo, do katere bo naša lokalna instanca
te mikrostoritve dostopala. Vnesti bomo morali administratorsko uporabniško ime in geslo, ki si ga moramo zapomniti.

Ko je inicializacija baze končana, skopirajmo `.env.TEMPLATE` v `.env` in izpolnimo manjkajoče ali spremenimo napačne
nastavitve, kot sta naslov in poverilnice za dostop do baze ter nastavitve, ki se tičejo žetonov JWT.

Sedaj izvedemo sledeče ukaze:
```bash
$ poetry install --no-root
$ poetry run python main.py
```

S tem bomo zagnali našo mikrostoritev, ki bo poskrbela, da so nastavitve veljavne,
morebiti ustvarila manjkajoče tabele v bazi in nato izpostavila strežnik HTTP na vratih `8002`.

Do dokumentacije naše REST mikrostoritve lahko sedaj dostopamo na naslovu `http://127.0.0.1:8002/docs`.


> Za podrobnejše korake, kar se tiče namestitve v Kubernetes okolje, 
> glej glavni repozitorij [tukaj](https://github.com/RSO-2024-Mikrovrtickarja/micro-scale).   


### 2.1 Konfiguracija
Ta mikrostoritev se konfigurira preko okoljskih spremenljivk, opisanih spodaj:
```bash
# Naslov (IP ali domena), kjer se nahaja baza PostgreSQL. 
DATABASE_HOSTNAME=localhost
# Številka vrat, na katerih posluša baza PostgreSQL.
DATABASE_PORT=5433
# Uporabniško ime, s katerim se bo mikrostoritev overila bazi.
DATABASE_USERNAME=postgres
# Geslo, s katerim se bo mikrostoritev overila bazi.
DATABASE_PASSWORD=postgres
# Ime baze, kjer naj se hranijo podatki. Baza mora že obstajati.
DATABASE_NAME=microscale_storage

# Skrivni ključ, ki se uporablja za podpisovanje JWT žetonov.
JWT_SECRET_KEY=supersecretkey
# Algoritem, ki naj se uporabi pri JWT žetonih.
JWT_ALGORITHM=HS256
# Trajanje veljavnosti JWT žetona za dostop, v minutah.
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
```
