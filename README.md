# Blackjack

Questo è un semplice gioco di Blackjack implementato in Python usando Tkinter per l'interfaccia grafica.

## Regole del gioco

1. **Obiettivo**: Ottenere un punteggio più alto del banco senza superare 21 punti.

2. **Valore delle carte**:
   - Le carte numeriche (2-9) valgono il loro valore nominale
   - Le figure (J, Q, K) valgono 10 punti
   - L'Asso può valere 1 o 11 punti (il programma sceglie automaticamente il valore migliore)

3. **Svolgimento del gioco**:
   - Il giocatore e il banco ricevono due carte ciascuno
   - Una carta del banco rimane coperta
   - Il giocatore può:
     - Chiedere una carta ("Carta")
     - Fermarsi ("Stai")
   - Se il giocatore supera 21 punti, perde immediatamente
   - Quando il giocatore si ferma, il banco scopre la sua carta e deve pescare finché non raggiunge almeno 17 punti
   - Se il banco ha 16 punti esatti è costretto a pescare

4. **Condizioni di vittoria**:
   - Se il giocatore supera 21 punti, vince il banco
   - Se il banco supera 21 punti, vince il giocatore
   - Altrimenti, vince chi ha il punteggio più alto
   - In caso di parità, è un pareggio

## Come giocare
1. Premi "Carta" per richiedere un'altra carta
2. Premi "Stai" quando sei soddisfatto delle tue carte
3. Premi "Nuova Partita" per iniziare una nuova mano