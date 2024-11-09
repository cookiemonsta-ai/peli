import random
import json

pelaajat = [{"nimi":"pelaaja1", "nappulat":[0,0,0,0]},{"nimi":"pelaaja2","nappulat":[0,0,0,0]}]
vuoro=0
maaliinpaasy=20
maalialue=4

def heita_noppaa():
    return random.randint(1,6)

def siirra_nappulaa(pelaaja, nappula_indeksi, askelia):
    sijainti=pelaaja["nappulat"][nappula_indeksi]
    if sijainti==0 and askelia==6:
        pelaaja["nappulat"][nappula_indeksi]=1
    elif sijainti>0:
        uusi_sijainti=sijainti+askelia
        if uusi_sijainti<=maaliinpaasy:
            pelaaja["nappulat"][nappula_indeksi]=uusi_sijainti
            maalialueen_alku=maaliinpaasy-maalialue

            if uusi_sijainti>maaliinpaasy:
                ylimeneva=uusi_sijainti-maaliinpaasy
                uusi_sijainti=maaliinpaasy-ylimeneva
                print(f'{pelaaja["nimi"]} kimpoaa takaisin maalialueen päädystä!')

            if uusi_sijainti>=maalialueen_alku:
                print(f'{pelaaja["nimi"]} on maalialueella!')
                pelaaja["nappulat"][nappula_indeksi]=uusi_sijainti
                if uusi_sijainti==maaliinpaasy:
                    print(f'{pelaaja["nimi"]} sai nappulan maalialueelle!')
                    pelaaja["nappulat"][nappula_indeksi]="maalissa"

                else:
                    pelaaja["nappulat"][nappula_indeksi]=uusi_sijainti

                for vastustaja in pelaajat:
                    if vastustaja!=pelaaja:
                        for i in range(len(vastustaja["nappulat"])):
                            if vastustaja["nappulat"][i]==uusi_sijainti:
                                print(f'{vastustaja["nimi"]} syö {pelaaja["nimi"]}n nappulan!')
                                vastustaja["nappulat"][i]=0
                                
def pelaa_vuoro():
    global vuoro
    pelaaja=pelaajat[vuoro]
    print(f'{pelaaja["nimi"]}n vuoro!')
    nopan_tulos=heita_noppaa()
    print(f'Noppa heitti tuloksen {nopan_tulos}')
    for i in range(len(pelaaja["nappulat"])):
        if pelaaja["nappulat"][i]!="maalissa":
            siirra_nappulaa(pelaaja, i, nopan_tulos)
            break
    vuoro=(vuoro+1)%len(pelaajat)

def peli_paattyi():
    for pelaaja in pelaajat:
        if all([nappula=="maalissa" for nappula in pelaaja["nappulat"]]):
            print(f'{pelaaja["nimi"]} voitti pelin!')
            return True
    return False

def tallennus():
    pelitila={"pelaajat":pelaajat, "vuoro":vuoro}
    with open("peli.json", "w") as tiedosto:
        json.dump(pelitila, tiedosto)
    print("Peli tallennettu!")

def lataus():
    global pelaajat,vuoro
    try:
        with open("peli.json", "r") as tiedosto:
            pelitila=json.load(tiedosto)
            pelaajat=pelitila["pelaajat"]
            vuoro=pelitila["vuoro"]
        print("Peli ladattu!")
    except FileNotFoundError:
        print("Peliä ei ole tallennettu!")

while not peli_paattyi():
    pelaa_vuoro()
    tallenna=input("Haluatko tallentaa pelin? (k/e)")
    if tallenna=="k":
        tallennus()
        print("Peli tallennettu!")
