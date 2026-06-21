import random
import tkinter as tk

from tkinter import messagebox

class Sudoku:
    """Klasa odpowiedzialna za logikę gry Sudoku."""

    def __init__(self, liczba_pustych_pol=40):
        """Tworzy obiekt gry Sudoku i generuje nową planszę"""
        self.liczba_pustych_pol = liczba_pustych_pol
        self.rozwiazanie = self.stworz_pusta_plansze()
        self.plansza_startowa = None
        self.generuj_nowa_plansze()

    def stworz_pusta_plansze(self):
        """Tworzy pustą planszę sudoku 9x9 wypełnioną zerami"""
        return [[0 for _ in range(9)] for _ in range(9)]

    def kopiuj_plansze(self, plansza):
        """Tworzy kopię podanej planszy sudoku"""
        return [wiersz[:] for wiersz in plansza]

    def znajdz_puste_pole(self, plansza):
        """Znajduje pierwsze puste pole na planszy, czyli pole z wartością 0"""
        for i in range(9):
            for j in range(9):
                if plansza[i][j] == 0:
                    return i, j
        return None

    def czy_mozna_wstawic(self, plansza, wiersz, kolumna, liczba):
        """Sprawdza, czy daną liczbę można wstawić w podane miejsce planszy."""
        for i in range(9):
            if plansza[wiersz][i] == liczba:
                return False

        for i in range(9):
            if plansza[i][kolumna] == liczba:
                return False

        start_wiersz = (wiersz // 3) * 3
        start_kolumna = (kolumna // 3) * 3

        for i in range(start_wiersz, start_wiersz + 3):
            for j in range(start_kolumna, start_kolumna + 3):
                if plansza[i][j] == liczba:
                    return False

        return True

    def rozwiaz_sudoku(self, plansza):
        """Rozwiązuje sudoku metodą backtrackingu"""
        puste_pole = self.znajdz_puste_pole(plansza)

        if puste_pole is None:
            return True

        wiersz, kolumna = puste_pole

        for liczba in range(1, 10):
            if self.czy_mozna_wstawic(plansza, wiersz, kolumna, liczba):
                plansza[wiersz][kolumna] = liczba

                if self.rozwiaz_sudoku(plansza):
                    return True

                plansza[wiersz][kolumna] = 0

        return False

    def wypelnij_losowo(self, plansza):
        """Losowo wypełnia pustą planszę poprawnym rozwiązaniem Sudoku"""
        puste_pole = self.znajdz_puste_pole(plansza)

        if puste_pole is None:
            return True

        wiersz, kolumna = puste_pole

        liczby = list(range(1, 10))
        random.shuffle(liczby)

        for liczba in liczby:
            if self.czy_mozna_wstawic(plansza, wiersz, kolumna, liczba):
                plansza[wiersz][kolumna] = liczba

                if self.wypelnij_losowo(plansza):
                    return True

                plansza[wiersz][kolumna] = 0

        return False

    def usun_liczby(self, plansza):
        """Usuwa z planszy określoną liczbę pól, tworząc zadanie dla gracza"""
        usuniete = 0

        while usuniete < self.liczba_pustych_pol:
            wiersz = random.randint(0, 8)
            kolumna = random.randint(0, 8)

            if plansza[wiersz][kolumna] != 0:
                plansza[wiersz][kolumna] = 0
                usuniete += 1

    def generuj_nowa_plansze(self):
        """Generuje nowe sudoku"""
        self.rozwiazanie = self.stworz_pusta_plansze()
        self.wypelnij_losowo(self.rozwiazanie)

        self.plansza_startowa = self.kopiuj_plansze(self.rozwiazanie)
        self.usun_liczby(self.plansza_startowa)

    def rozwiaz(self, plansza):
        """Zwraca rozwiązanie podanej planszy albo None, jeśli nie da się jej rozwiązać"""
        kopia = self.kopiuj_plansze(plansza)

        if self.rozwiaz_sudoku(kopia):
            return kopia

        return None

    def podpowiedz(self, plansza):
        """Zwraca losową podpowiedź"""
        rozwiazana = self.rozwiaz(plansza)

        if rozwiazana is None:
            return None

        puste_pola = []

        for i in range(9):
            for j in range(9):
                if plansza[i][j] == 0:
                    puste_pola.append((i, j))

        if len(puste_pola) == 0:
            return None

        wiersz, kolumna = random.choice(puste_pola)
        liczba = rozwiazana[wiersz][kolumna]

        return wiersz, kolumna, liczba


class SudokuGUI:
    """Klasa odpowiedzialna za wygląd gry i obsługę okna Tkinter"""

    def __init__(self, root):
        """Tworzy okno gry oraz ekran startowy"""
        self.root = root
        self.root.title("Sudoku")
        self.root.geometry("630x780")  # Lekko powiększone okno na liczniki cyfr

        self.gra = None
        self.pola = []
        self.etykiety_licznikowe_cyfr = {}  # Słownik przechowujący labele z licznikami cyfr

        self.liczba_bledow = 0
        self.liczba_podpowiedzi = 0
        self.limit_podpowiedzi = 3
        self.napis_licznikow = None

        self.czas = 0
        self.napis_czasu = None
        self.gra_aktywna = False
        self.aktywne_pole = None

        self.tryb_notatek = False
        self.przycisk_notatek = None

        self.poziom_trudnosci = tk.StringVar(value="średni")

        self.poziomy = {
            "łatwy": 30,
            "średni": 40,
            "trudny": 50
        }

        self.ekran_startowy()

    def wyczysc_okno(self):
        """Usuwa wszystkie elementy znajdujące się aktualnie w oknie"""
        for element in self.root.winfo_children():
            element.destroy()

    def ekran_startowy(self):
        """Tworzy ekran startowy"""
        self.gra_aktywna = False
        self.wyczysc_okno()

        napis = tk.Label(
            self.root,
            text="SUDOKU",
            font=("Arial", 48, "bold")
        )
        napis.pack(pady=120)

        napis_poziom = tk.Label(
            self.root,
            text="Wybierz poziom trudności:",
            font=("Arial", 18)
        )
        napis_poziom.pack(pady=10)

        ramka_poziomow = tk.Frame(self.root)
        ramka_poziomow.pack(pady=10)

        tk.Radiobutton(
            ramka_poziomow,
            text="Łatwy",
            variable=self.poziom_trudnosci,
            value="łatwy",
            font=("Arial", 16)
        ).pack(anchor="w")

        tk.Radiobutton(
            ramka_poziomow,
            text="Średni",
            variable=self.poziom_trudnosci,
            value="średni",
            font=("Arial", 16)
        ).pack(anchor="w")

        tk.Radiobutton(
            ramka_poziomow,
            text="Trudny",
            variable=self.poziom_trudnosci,
            value="trudny",
            font=("Arial", 16)
        ).pack(anchor="w")

        przycisk_start = tk.Button(
            self.root,
            text="START",
            font=("Arial", 24, "bold"),
            width=10,
            command=self.start_gry
        )
        przycisk_start.pack(pady=30)

    def start_gry(self):
        """Uruchamia właściwą grę"""
        wybrany_poziom = self.poziom_trudnosci.get()
        liczba_pustych_pol = self.poziomy[wybrany_poziom]

        self.gra = Sudoku(liczba_pustych_pol=liczba_pustych_pol)

        self.liczba_bledow = 0
        self.liczba_podpowiedzi = 0
        self.czas = 0
        self.gra_aktywna = True
        self.aktywne_pole = None
        self.etykiety_licznikowe_cyfr = {}

        self.tryb_notatek = False
        self.przycisk_notatek = None

        self.wyczysc_okno()
        self.pola = []

        self.utworz_licznik_czasu()
        self.utworz_plansze()
        self.utworz_przyciski()
        self.utworz_cyfry()
        self.wpisz_plansze_do_gui(self.gra.plansza_startowa)
        self.aktualizuj_liczniki_cyfr()
        self.licz_czas()

    def utworz_licznik_czasu(self):
        """Tworzy etykietę wyświetlającą czas gry"""
        self.napis_czasu = tk.Label(
            self.root,
            text="Czas: 00:00",
            font=("Arial", 18, "bold")
        )
        self.napis_czasu.pack(pady=10)

    def licz_czas(self):
        """Aktualizuje licznik czasu co sekundę, dopóki gra jest aktywna"""
        if self.gra_aktywna:
            minuty = self.czas // 60
            sekundy = self.czas % 60

            self.napis_czasu.config(
                text=f"Czas: {minuty:02d}:{sekundy:02d}"
            )

            self.czas += 1
            self.root.after(1000, self.licz_czas)

    def utworz_plansze(self):
        """Tworzy graficzną planszę 9x9 z podziałem na kwadraty 3x3"""
        ramka_glowna = tk.Frame(self.root)
        ramka_glowna.pack(pady=20)

        for kwadrat_wiersz in range(3):
            for kwadrat_kolumna in range(3):

                ramka_kwadratu = tk.Frame(
                    ramka_glowna,
                    borderwidth=2,
                    relief="solid"
                )

                ramka_kwadratu.grid(
                    row=kwadrat_wiersz,
                    column=kwadrat_kolumna
                )

                for maly_wiersz in range(3):
                    for mala_kolumna in range(3):

                        i = kwadrat_wiersz * 3 + maly_wiersz
                        j = kwadrat_kolumna * 3 + mala_kolumna

                        pole = tk.Entry(
                            ramka_kwadratu,
                            width=3,
                            font=("Arial", 20),
                            justify="center"
                        )

                        pole.grid(
                            row=maly_wiersz,
                            column=mala_kolumna,
                            padx=1,
                            pady=1
                        )

                        pole.bind(
                            "<KeyRelease>",
                            lambda event, r=i, c=j: self.sprawdz_wpis(event, r, c)
                        )

                        pole.bind(
                            "<FocusIn>",
                            lambda event, r=i, c=j: self.ustaw_aktywne_pole(r, c)
                        )

                        pole.bind(
                            "<FocusOut>",
                            lambda event: self.wyczysc_podswietlenie()
                        )

                        if len(self.pola) <= i:
                            self.pola.append([])

                        self.pola[i].append(pole)

    def ustaw_aktywne_pole(self, wiersz, kolumna):
        """Zapamiętuje aktywne pole i podświetla wiersz, kolumnę oraz kwadrat 3x3"""
        self.aktywne_pole = (wiersz, kolumna)
        self.podswietl_obszar(wiersz, kolumna)

    def podswietl_obszar(self, wiersz, kolumna):
        """Zmienia kolor tła dla powiązanych pól na planszy"""
        # Najpierw resetujemy kolory tła wszystkich pól do białego
        self.wyczysc_podswietlenie()

        start_wiersz = (wiersz // 3) * 3
        start_kolumna = (kolumna // 3) * 3

        for i in range(9):
            for j in range(9):
                # Sprawdzamy czy pole należy do tego samego wiersza, kolumny lub kwadratu 3x3
                w_tym_samym_wierszu = (i == wiersz)
                w_tej_samej_kolumnie = (j == kolumna)
                w_tym_samym_kwadracie = (
                            start_wiersz <= i < start_wiersz + 3 and start_kolumna <= j < start_kolumna + 3)

                if w_tym_samym_wierszu or w_tej_samej_kolumnie or w_tym_samym_kwadracie:
                    if i == wiersz and j == kolumna:
                        self.pola[i][j].config(bg="#bbdefb")  # Ciemniejszy błękit dla dokładnie klikniętego pola
                    else:
                        self.pola[i][j].config(bg="#e3f2fd")  # Jasny błękit dla linii i kwadratu

    def wyczysc_podswietlenie(self):
        """Przywraca domyślne białe tło dla wszystkich pól"""
        for i in range(9):
            for j in range(9):
                self.pola[i][j].config(bg="white")

    def utworz_przyciski(self):
        """Tworzy przyciski: podpowiedź, rozwiąż, nowa gra"""
        ramka = tk.Frame(self.root)
        ramka.pack(pady=10)

        tk.Button(
            ramka,
            text="Podpowiedź",
            command=self.przycisk_podpowiedz
        ).grid(row=0, column=0, padx=10)

        self.napis_licznikow = tk.Label(
            self.root,
            text="Błędy: 0/3   Podpowiedzi: 0/3",
            font=("Arial", 14)
        )
        self.napis_licznikow.pack(pady=5)

        tk.Button(
            ramka,
            text="Rozwiąż",
            command=self.przycisk_rozwiaz
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            ramka,
            text="Nowa gra",
            command=self.nowa_gra
        ).grid(row=0, column=2, padx=10)

        self.przycisk_notatek = tk.Button(
            ramka,
            text="Tryb notatek: WYŁĄCZONY",
            command=self.przelacz_tryb_notatek
        )
        self.przycisk_notatek.grid(row=0, column=3, padx=10)

    def przelacz_tryb_notatek(self):
        """Włącza lub wyłącza tryb wpisywania notatek"""
        self.tryb_notatek = not self.tryb_notatek

        if self.tryb_notatek:
            self.przycisk_notatek.config(text="Tryb notatek: WŁĄCZONY")
        else:
            self.przycisk_notatek.config(text="Tryb notatek: WYŁĄCZONY")

    def utworz_cyfry(self):
        """Tworzy sekcję wyboru cyfr wraz z licznikami sztuk pozostałych do wpisania"""
        napis = tk.Label(
            self.root,
            text="Wybierz cyfrę:",
            font=("Arial", 14)
        )
        napis.pack(pady=5)

        ramka_cyfr = tk.Frame(self.root)
        ramka_cyfr.pack(pady=5)

        for liczba in range(1, 10):
            # Kontener na przycisk i jego licznik pod spodem
            kontener = tk.Frame(ramka_cyfr)
            kontener.grid(row=0, column=liczba - 1, padx=4)

            tk.Button(
                kontener,
                text=str(liczba),
                font=("Arial", 16, "bold"),
                width=3,
                command=lambda l=liczba: self.wpisz_cyfre(l)
            ).pack()

            # Etykieta licznika pod przyciskiem
            etykieta_licznik = tk.Label(
                kontener,
                text="9",
                font=("Arial", 10, "italic"),
                fg="gray"
            )
            etykieta_licznik.pack()

            # Zapisujemy referencję do etykiety, aby móc ją aktualizować w locie
            self.etykiety_licznikowe_cyfr[liczba] = etykieta_licznik

    def wpisz_cyfre(self, liczba):
        """
        Wpisuje cyfrę do aktywnego pola albo dodaje ją jako notatkę

        Jeżeli tryb notatek jest wyłączony, cyfra jest traktowana jako odpowiedź gracza i
        od razu sprawdzana.
        Jeśli tryb notatek jest włączony, cyfra zostaje dodana lub usunięta z listy notatek w
        danym polu
        """
        if self.aktywne_pole is None:
            messagebox.showinfo(
                "Informacja",
                "Najpierw kliknij puste pole na playszy"
            )
            return

        wiersz, kolumna = self.aktywne_pole
        pole = self.pola[wiersz][kolumna]

        if pole["state"] == "disabled":
            return

        if self.tryb_notatek:
            aktualny_tekst = pole.get()

            # Zmiana: Jeśli w polu jest czarna (ostateczna) odpowiedź, nie nadpisujemy jej notatkami
            if aktualny_tekst.isdigit() and len(aktualny_tekst) == 1 and pole.cget("fg") == "black":
                return

            notatki = aktualny_tekst.split()

            if str(liczba) in notatki:
                notatki.remove(str(liczba))
            else:
                notatki.append(str(liczba))

            notatki.sort()

            pole.delete(0, tk.END)
            pole.insert(0, " ".join(notatki))
            pole.config(font=("Arial", 9), fg="gray")

            return

        pole.config(font=("Arial", 20), fg="black")
        pole.delete(0, tk.END)
        pole.insert(0, str(liczba))

        self.sprawdz_wpis(None, wiersz, kolumna)

    def aktualizuj_liczniki(self):
        """Aktualizuje napis pokazujący liczbę błędów i wykorzystanych podpowiedzi"""
        self.napis_licznikow.config(
            text=f"Błędy: {self.liczba_bledow}/3     Podpowiedzi: {self.liczba_podpowiedzi}/3")

    def aktualizuj_liczniki_cyfr(self):
        """Zlicza ile cyfr znajduje się na planszy i odświeża etykiety informacyjne"""
        # Słownik zliczający wystąpienia każdej cyfry
        wystapienia = {i: 0 for i in range(1, 10)}

        for i in range(9):
            for j in range(9):
                # Zmiana: Liczymy tylko ostateczne cyfry (czarne), ignorujemy szare notatki
                if self.pola[i][j].cget("fg") == "black":
                    wartosc = self.pola[i][j].get()
                    if wartosc.isdigit() and len(wartosc) == 1:
                        cyfra = int(wartosc)
                        if 1 <= cyfra <= 9:
                            wystapienia[cyfra] += 1

        # Aktualizacja widoku w GUI
        for cyfra, etykieta in self.etykiety_licznikowe_cyfr.items():
            pozostalo = 9 - wystapienia[cyfra]
            if pozostalo <= 0:
                etykieta.config(text="✔", fg="green", font=("Arial", 10, "bold"))
            else:
                etykieta.config(text=str(pozostalo), fg="gray", font=("Arial", 10, "italic"))

    def ekran_przegranej(self):
        """Pokazuje ekran przegranej po popełnieniu trzech błędów"""
        self.wyczysc_okno()

        napis = tk.Label(
            self.root,
            text="PRZEGRAŁEŚ",
            font=("Arial", 50, "bold")
        )
        napis.pack(pady=150)

        przycisk = tk.Button(
            self.root,
            text="Wróć do ekranu startowego",
            font=("Arial", 18),
            command=self.ekran_startowy
        )
        przycisk.pack(pady=20)

    def ekran_wygranej(self):
        """Pokazuje ekran wygranej po poprawnym ukończeniu sudoku"""
        self.gra_aktywna = False
        self.wyczysc_okno()

        napis = tk.Label(
            self.root,
            text="GRATULACJE!",
            font=("Arial", 50, "bold"),
        )
        napis.pack(pady=150)

        przycisk = tk.Button(
            self.root,
            text="Wróć do ekranu startowego",
            font=("Arial", 18),
            command=self.ekran_startowy
        )
        przycisk.pack(pady=20)

    def czy_gracz_wygral(self):
        """Sprawdza, czy cała plansza została poprawnie uzupełniona"""
        for i in range(9):
            for j in range(9):
                wartosc = self.pola[i][j].get()

                # Zmiana: Jeśli pole jest puste lub jest szarą notatką, gracz jeszcze nie wygrał
                if wartosc == "" or self.pola[i][j].cget("fg") == "gray":
                    return False

                if not wartosc.isdigit():
                    return False

                if int(wartosc) != self.gra.rozwiazanie[i][j]:
                    return False

        return True

    def pobierz_plansze_z_gui(self):
        """Odczytuje liczby wpisane przez gracza i zamienia je na planszę"""
        plansza = []

        for i in range(9):
            wiersz = []

            for j in range(9):
                wartosc = self.pola[i][j].get()

                # Zmiana: Jeśli pole jest szare (notatka), traktujemy je jako puste (0) przy rozwiązywaniu
                if wartosc == "" or self.pola[i][j].cget("fg") == "gray":
                    wiersz.append(0)
                elif " " in wartosc:
                    #notatki traktujemy jako puste pola
                    wiersz.append(0)
                elif wartosc.isdigit() and len(wartosc) == 1 and 1 <= int(wartosc) <= 9:
                    wiersz.append(int(wartosc))
                else:
                    messagebox.showerror(
                        "Błąd",
                        "Można wpisywać tylko liczby od 1 do 9."
                    )
                    return None

            plansza.append(wiersz)

        return plansza

    def wpisz_plansze_do_gui(self, plansza):
        """Wpisuje podaną planszę do pól widocznych w oknie gry"""
        for i in range(9):
            for j in range(9):
                self.pola[i][j].config(state="normal")
                self.pola[i][j].delete(0, tk.END)
                self.pola[i][j].config(font=("Arial", 20), fg="black")

                if plansza[i][j] != 0:
                    self.pola[i][j].insert(0, str(plansza[i][j]))

                if self.gra.plansza_startowa[i][j] != 0:
                    self.pola[i][j].config(
                        state="disabled",
                        disabledforeground="black"
                    )
        self.aktualizuj_liczniki_cyfr()

    def sprawdz_wpis(self, event, wiersz, kolumna):
        """Sprawdza czy gracz podał poprawną cyfrę"""
        # Zmiana: Jeśli jesteśmy w trybie notatek, stylizujemy tekst z klawiatury na notatkę i pomijamy walidację błędów
        if self.tryb_notatek:
            self.pola[wiersz][kolumna].config(font=("Arial", 9), fg="gray")
            self.aktualizuj_liczniki_cyfr()
            return

        # Zmiana: Jeśli tryb notatek jest wyłączony, ale gracz nacisnął nową cyfrę na klawiaturze, przywracamy normalny styl
        if event is not None and event.char.isdigit():
            self.pola[wiersz][kolumna].config(font=("Arial", 20), fg="black")

        # Zmiana: Jeśli pole wciąż ma status notatki (jest szare), ignorujemy je (np. przy usuwaniu backspacem)
        if self.pola[wiersz][kolumna].cget("fg") == "gray":
            self.aktualizuj_liczniki_cyfr()
            return

        wartosc = self.pola[wiersz][kolumna].get()

        if wartosc == "":
            self.aktualizuj_liczniki_cyfr()
            return

        if " " in wartosc:
            self.aktualizuj_liczniki_cyfr()
            return

        if not wartosc.isdigit() or not (1 <= int(wartosc) <= 9):
            messagebox.showerror(
                "Błąd",
                "Można wpisywać tylko liczby od 1 do 9."
            )
            self.pola[wiersz][kolumna].delete(0, tk.END)
            self.aktualizuj_liczniki_cyfr()
            return

        liczba = int(wartosc)

        if liczba != self.gra.rozwiazanie[wiersz][kolumna]:
            self.liczba_bledow += 1
            self.aktualizuj_liczniki()

            messagebox.showerror(
                "Błąd",
                "Ta liczba jest niepoprawna!"
            )
            self.pola[wiersz][kolumna].delete(0, tk.END)

            if self.liczba_bledow >= 3:
                self.ekran_przegranej()
        else:
            # Ponieważ pole zostało poprawnie wypełnione, odświeżamy też podświetlenie dla nowego stanu
            self.podswietl_obszar(wiersz, kolumna)

        self.aktualizuj_liczniki_cyfr()

        if self.czy_gracz_wygral():
            self.ekran_wygranej()

    def przycisk_rozwiaz(self):
        """Obsługuje przycisk "ROZWIĄŻ" i wpisuje pełne rozwiązanie"""
        plansza = self.pobierz_plansze_z_gui()

        if plansza is None:
            return

        rozwiazana = self.gra.rozwiaz(plansza)

        if rozwiazana is None:
            messagebox.showinfo("Informacja", "Nie da się rozwiązać tej planszy.")
        else:
            self.wpisz_plansze_do_gui(rozwiazana)

            self.gra_aktywna = False

            przycisk_powrotu = tk.Button(
                self.root,
                text="Wróć do ekranu startowego",
                font=("Arial", 14),
                command=self.ekran_startowy
            )
            przycisk_powrotu.pack(pady=10, before=self.napis_licznikow)

    def przycisk_podpowiedz(self):
        """Obsługuje przycisk podpowiedzi i pilnuje limitu"""
        if self.liczba_podpowiedzi >= self.limit_podpowiedzi:
            messagebox.showinfo(
                "Informacja",
                "wykorzystano wszystkie podpowiedzi"
            )
            return
        """Obsługuje przycisk "PODPOWIEDŹ" i wpisuje jedną poprawną liczbę"""
        plansza = self.pobierz_plansze_z_gui()

        if plansza is None:
            return

        wynik = self.gra.podpowiedz(plansza)

        if wynik is None:
            messagebox.showinfo("Informacja", "Brak podpowiedzi.")
            return

        wiersz, kolumna, liczba = wynik

        self.pola[wiersz][kolumna].config(font=("Arial", 20), fg="black")
        self.pola[wiersz][kolumna].delete(0, tk.END)
        self.pola[wiersz][kolumna].insert(0, str(liczba))

        self.liczba_podpowiedzi += 1
        self.aktualizuj_liczniki()
        self.aktualizuj_liczniki_cyfr()

        if self.czy_gracz_wygral():
            self.ekran_wygranej()

    def nowa_gra(self):
        """Generuje nową planszę i odświeża widok gry"""
        wybrany_poziom = self.poziom_trudnosci.get()
        liczba_pustych_pol = self.poziomy[wybrany_poziom]

        self.gra = Sudoku(liczba_pustych_pol=liczba_pustych_pol)

        self.liczba_bledow = 0
        self.liczba_podpowiedzi = 0
        self.czas = 0
        self.gra_aktywna = True
        self.aktywne_pole = None
        self.etykiety_licznikowe_cyfr = {}

        self.tryb_notatek = False
        self.przycisk_notatek = None

        self.wyczysc_okno()
        self.pola = []

        self.utworz_licznik_czasu()
        self.utworz_plansze()
        self.utworz_przyciski()
        self.utworz_cyfry()
        self.wpisz_plansze_do_gui(self.gra.plansza_startowa)
        self.aktualizuj_liczniki_cyfr()
        self.licz_czas()


root = tk.Tk()
aplikacja = SudokuGUI(root)
root.mainloop()