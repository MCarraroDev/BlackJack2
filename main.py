import os
import random
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

# Costanti del gioco
VALORI_CARTE = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "t": 10,
    "j": 10,
    "q": 10,
    "k": 10,
    "a": 11,
}

RANGHI = ["2", "3", "4", "5", "6", "7", "8", "9", "t", "j", "q", "k", "a"]
SEMI = [
    "C",
    "D",
    "H",
    "S",
]  # Clubs (Fiori), Diamonds (Quadri), Hearts (Cuori), Spades (Picche)

# Creiamo la finestra principale
finestra = tk.Tk()
finestra.title("Blackjack")
finestra.geometry("1280x720")
finestra.configure(bg="#2C3E50")

# Dizionario per memorizzare le immagini
carte_images = {}
carta_retro = None

# Dimensioni desiderate per le carte
CARD_WIDTH = 100
CARD_HEIGHT = 145

# Carica il retro della carta
retro = Image.open(os.path.join("assets", "carte", "cardBack.png"))
retro = retro.resize((CARD_WIDTH, CARD_HEIGHT), Image.Resampling.LANCZOS)
carta_retro = ImageTk.PhotoImage(retro)

# Carica tutte le carte
for rango in RANGHI:
    for seme in SEMI:
        nome_file = f"{rango}{seme}.png"
        percorso = os.path.join("assets", "carte", nome_file)
        if os.path.exists(percorso):
            img = Image.open(percorso)
            img = img.resize((CARD_WIDTH, CARD_HEIGHT), Image.Resampling.LANCZOS)
            carte_images[f"{rango}{seme}"] = ImageTk.PhotoImage(img)

# Variabili globali per il gioco
mazzo = []
mano_giocatore = []
mano_banco = []

# Creiamo le etichette e i frame per le carte
label_banco = tk.Label(
    finestra, text="Banco", font=("Arial", 16), bg="#2C3E50", fg="white"
)
label_banco.pack(pady=5)

# Etichetta per il punteggio del banco
label_punteggio_banco = tk.Label(
    finestra, text="Punteggio banco: 0", font=("Arial", 12), bg="#2C3E50", fg="white"
)
label_punteggio_banco.pack(pady=2)

frame_banco = tk.Frame(finestra, bg="#2C3E50")
frame_banco.pack(pady=10)

label_giocatore = tk.Label(
    finestra, text="Le tue carte", font=("Arial", 16), bg="#2C3E50", fg="white"
)
label_giocatore.pack(pady=5)

# Etichetta per il punteggio del giocatore
label_punteggio_giocatore = tk.Label(
    finestra, text="Il tuo punteggio: 0", font=("Arial", 12), bg="#2C3E50", fg="white"
)
label_punteggio_giocatore.pack(pady=2)

frame_giocatore = tk.Frame(finestra, bg="#2C3E50")
frame_giocatore.pack(pady=10)


def calcola_punteggio(mano, mostra_tutto=True):
    """Calcola il punteggio di una mano di carte"""
    punteggio = 0
    assi = 0

    # Prima contiamo le carte non asso
    for i, carta in enumerate(mano):
        # Se è la seconda carta del banco e non dobbiamo mostrarla, la saltiamo
        if not mostra_tutto and i > 0:
            continue

        if carta[0] == "A":
            assi += 1
        else:
            punteggio += VALORI_CARTE[carta[0]]

    # Poi aggiungiamo gli assi
    for _ in range(assi):
        if punteggio + 11 <= 21:  # Se possiamo usare 11 senza sballare
            punteggio += 11
        else:  # Altrimenti usiamo 1
            punteggio += 1

    return punteggio


def aggiorna_punteggi():
    """Aggiorna i punteggi mostrati"""
    # Aggiorna punteggio giocatore
    punteggio_giocatore = calcola_punteggio(mano_giocatore)
    label_punteggio_giocatore.config(text=f"Il tuo punteggio: {punteggio_giocatore}")

    # Aggiorna punteggio banco (mostra solo la prima carta)
    punteggio_banco = calcola_punteggio(mano_banco, mostra_tutto=False)
    label_punteggio_banco.config(text=f"Punteggio banco visibile: {punteggio_banco}")


def aggiorna_carte():
    """Aggiorna la visualizzazione delle carte"""
    # Pulisce i frame
    for widget in frame_banco.winfo_children():
        widget.destroy()
    for widget in frame_giocatore.winfo_children():
        widget.destroy()

    # Mostra le carte del banco
    for i, carta in enumerate(mano_banco):
        if i == 1:  # Nascondi la seconda carta
            label = tk.Label(frame_banco, image=carta_retro, bg="#2C3E50")
        else:
            carta_img = carte_images[f"{carta[0].lower()}{carta[1]}"]
            label = tk.Label(frame_banco, image=carta_img, bg="#2C3E50")
        label.pack(side="left", padx=5)

    # Mostra le carte del giocatore
    for carta in mano_giocatore:
        carta_img = carte_images[f"{carta[0].lower()}{carta[1]}"]
        label = tk.Label(frame_giocatore, image=carta_img, bg="#2C3E50")
        label.pack(side="left", padx=5)

    # Aggiorna i punteggi
    aggiorna_punteggi()


def chiedi_carta():
    """Il giocatore chiede una carta"""
    mano_giocatore.append(mazzo.pop())
    aggiorna_carte()

    # Controlla se il giocatore ha sballato
    if calcola_punteggio(mano_giocatore) > 21:
        messagebox.showinfo("Game Over", "Hai sballato! Il banco vince!")
        btn_carta.config(state="disabled")
        btn_stai.config(state="disabled")


def stai():
    """Il giocatore sta e gioca il banco"""
    # Mostra tutte le carte del banco
    for widget in frame_banco.winfo_children():
        widget.destroy()
    for carta in mano_banco:
        carta_img = carte_images[f"{carta[0].lower()}{carta[1]}"]
        label = tk.Label(frame_banco, image=carta_img, bg="#2C3E50")
        label.pack(side="left", padx=5)

    # Il banco pesca carte finché non ha almeno 17
    while calcola_punteggio(mano_banco) < 17:
        mano_banco.append(mazzo.pop())
        for widget in frame_banco.winfo_children():
            widget.destroy()
        for carta in mano_banco:
            carta_img = carte_images[f"{carta[0].lower()}{carta[1]}"]
            label = tk.Label(frame_banco, image=carta_img, bg="#2C3E50")
            label.pack(side="left", padx=5)

    # Calcola i punteggi finali
    punteggio_giocatore = calcola_punteggio(mano_giocatore)
    punteggio_banco = calcola_punteggio(mano_banco)

    # Aggiorna il punteggio finale del banco
    label_punteggio_banco.config(text=f"Punteggio banco: {punteggio_banco}")

    messaggio = f"Utente: {punteggio_giocatore}\n"
    messaggio += f"Banco: {punteggio_banco}\n\n"

    if punteggio_banco > 21:
        messaggio += "Il banco ha sballato! Hai vinto!"
    elif punteggio_banco > punteggio_giocatore:
        messaggio += "Il banco vince!"
    elif punteggio_banco < punteggio_giocatore:
        messaggio += "Hai vinto!"
    else:
        messaggio += "Pareggio!"

    messagebox.showinfo("Risultato", messaggio)
    btn_carta.config(state="disabled")
    btn_stai.config(state="disabled")


def nuova_partita():
    """Inizia una nuova partita"""
    global mazzo, mano_giocatore, mano_banco

    # Crea e mischia il mazzo
    mazzo = [(rango, seme) for rango in RANGHI for seme in SEMI]
    random.shuffle(mazzo)

    # Distribuisce le carte iniziali
    mano_giocatore = [mazzo.pop(), mazzo.pop()]
    mano_banco = [mazzo.pop(), mazzo.pop()]

    # Aggiorna la visualizzazione
    aggiorna_carte()

    # Abilita i pulsanti
    btn_carta.config(state="normal")
    btn_stai.config(state="normal")


# Creiamo i pulsanti
frame_bottoni = tk.Frame(finestra, bg="#2C3E50")
frame_bottoni.pack(pady=20)

btn_carta = tk.Button(
    frame_bottoni,
    text="Carta",
    command=chiedi_carta,
    font=("Arial", 12),
    padx=20,
    pady=10,
)
btn_carta.pack(side="left", padx=5)

btn_stai = tk.Button(
    frame_bottoni, text="Stai", command=stai, font=("Arial", 12), padx=20, pady=10
)
btn_stai.pack(side="left", padx=5)

btn_nuova = tk.Button(
    frame_bottoni,
    text="Nuova Partita",
    command=nuova_partita,
    font=("Arial", 12),
    padx=20,
    pady=10,
)
btn_nuova.pack(side="left", padx=5)

# Inizia la prima partita
nuova_partita()

# Avvia il gioco
finestra.mainloop()
