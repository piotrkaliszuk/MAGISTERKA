import numpy as np
srodowisko_wiersze = 6
srodowisko_kolumny = 6
wartosciQ = np.zeros((srodowisko_wiersze, srodowisko_kolumny, 4))
#print(wartosciQ)
kierunki = ['up', 'right', 'down', 'left']

nagrody = np.full((srodowisko_wiersze, srodowisko_kolumny), -100)
nagrody[0, 3] = 100
przejścia = {}
przejścia[1] = [1, 2, 3]
przejścia[2] = [0, 1, 2]
przejścia[3] = [2, 3]
przejścia[4] = [1, 2, 3, 4]

for wiersz in range(1, 5):
    for kolumna in przejścia[wiersz]:
        nagrody[wiersz, kolumna] = -1
print(nagrody)
def czy_przeszkoda(curr_wiersz, curr_kolumna):
  if nagrody[curr_wiersz, curr_kolumna] == -1:
    return False
  else:
    return True

def losowy_start():
  wiersz = np.random.randint(srodowisko_wiersze)
  kolumna = np.random.randint(srodowisko_kolumny)
  while czy_przeszkoda(wiersz, kolumna):
    wiersz = np.random.randint(srodowisko_wiersze)
    kolumna = np.random.randint(srodowisko_kolumny)
  return wiersz, kolumna

def akcja(wiersz, kolumna, eps):
  if np.random.random() < eps:
    return np.argmax(wartosciQ[wiersz, kolumna])
  else:
    return np.random.randint(4)

def zmiana_pozycji(wiersz, kolumna, akcja):
  nowy_wiersz = wiersz
  nowa_kolumna = kolumna
  if kierunki[akcja] == 'up' and wiersz > 0:
    nowy_wiersz -= 1
  elif kierunki[akcja] == 'right' and kolumna < srodowisko_kolumny - 1:
    nowa_kolumna += 1
  elif kierunki[akcja] == 'down' and wiersz < srodowisko_wiersze - 1:
    nowy_wiersz += 1
  elif kierunki[akcja] == 'left' and kolumna > 0:
    nowa_kolumna -= 1
  return nowy_wiersz, nowa_kolumna

def droga(wiersz, kolumna):
    curr_wiersz, curr_kolumna = wiersz, kolumna
    najkrótsza_droga = []
    najkrótsza_droga.append([curr_wiersz, curr_kolumna])
    while not czy_przeszkoda(curr_wiersz, curr_kolumna):
        kierunek = akcja(curr_wiersz, curr_kolumna, 1.)
        curr_wiersz, curr_kolumna = zmiana_pozycji(curr_wiersz, curr_kolumna, kierunek)
        najkrótsza_droga.append([curr_wiersz, curr_kolumna])
    return najkrótsza_droga

eps = 0.8
gamma = 0.8
alfa = 0.8
for x in range(100):
    wiersz, kolumna = losowy_start()
    while not czy_przeszkoda(wiersz, kolumna):
        kierunek = akcja(wiersz, kolumna, eps) #kierunek wykonania akcji
        #print(kierunek)
        stary_wiersz, stara_kolumna = wiersz, kolumna #zapis wartości
        wiersz, kolumna = zmiana_pozycji(wiersz, kolumna, kierunek) #wykonanie akcji
        nagroda = nagrody[wiersz, kolumna] #pobranie nagrody z tablicy
        stareQ = wartosciQ[stary_wiersz, stara_kolumna, kierunek] #zapis starej wartosci Q, do wzoru
        noweQ = stareQ + (alfa * (nagroda + (gamma * np.max(wartosciQ[wiersz, kolumna])) - stareQ)) #wyliczenie wzóru
        wartosciQ[stary_wiersz, stara_kolumna, kierunek] = noweQ #podpisanie nowej wartości do tablicy
print(wartosciQ)

print(droga(4,3))