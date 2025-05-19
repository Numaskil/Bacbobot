
"""
Bac Bo Analysis & Suggestion Bot
--------------------------------
Este script analisa a sequência de resultados do Bac Bo (Jogador, Banqueiro ou Empate)
e sugere a próxima aposta, combinando quatro estratégias:

1. Martingale (gestão de stake)
2. Anti‑padrão (inverter após 3 resultados iguais)
3. Repetição (seguir resultado anterior)
4. Empates raros (sugerir 'Empate' após X rodadas sem empate)

Observação: o script NÃO faz apostas automáticas. Ele apenas mostra a sugestão
e o valor de stake calculado. Você digita o resultado real para acompanhar.
"""

import json
import os
from collections import deque

# CONFIGURAÇÕES DO USUÁRIO
INITIAL_STAKE = 25           # valor inicial da aposta (R$)
PROFIT_TARGET = 100          # lucro desejado antes de parar (R$)
LOSS_LIMIT   = None          # sem limite de perda definido
TIE_THRESHOLD = 20           # quantas rodadas sem empate antes de sugerir 'Empate'

# ESTADO
history = deque(maxlen=100)   # últimos 100 resultados
bankroll = 0                  # lucro acumulado
current_stake = INITIAL_STAKE
last_bet_side = None
last_bet_result = None

print("Bac Bo Bot iniciado!")
print("Digite os resultados conforme aparecem (J = Jogador, B = Banqueiro, E = Empate)")
print("Para sair, digite 'sair'.\n")

def decide_next_bet():
    global history
    # Estratégia 1: Empate raro
    rounds_since_tie = next((i for i, r in enumerate(reversed(history), 1) if r == 'E'), None)
    if rounds_since_tie is None or rounds_since_tie > TIE_THRESHOLD:
        return 'E'
    # Estratégia 2: Anti‑padrão
    if len(history) >= 3 and len(set(list(history)[-3:])) == 1:
        last = history[-1]
        if last == 'J':
            return 'B'
        elif last == 'B':
            return 'J'
    # Estratégia 3: Repetição
    if history:
        return history[-1]
    # Sem histórico: escolhe Jogador por padrão
    return 'J'

def update_stake(win):
    global current_stake
    if win:
        current_stake = INITIAL_STAKE
    else:
        current_stake *= 2  # Martingale

while True:
    result = input("Resultado (J/B/E) >> ").strip().upper()
    if result in ['SAIR', 'S', 'QUIT', 'Q', 'EXIT']:
        print("Encerrando bot.")
        break
    if result not in ['J', 'B', 'E']:
        print("Entrada inválida. Use J, B ou E.")
        continue
    history.append(result)

    # Avalia aposta anterior
    if last_bet_side:
        win = (result == last_bet_side)
        update_stake(win)
        if win:
            bankroll += current_stake
            print(f"Você GANHOU a aposta anterior! Lucro atual: R${bankroll}")
        else:
            bankroll -= current_stake
            print(f"Você PERDEU a aposta anterior. Lucro atual: R${bankroll}")

    # Verifica limites
    if PROFIT_TARGET is not None and bankroll >= PROFIT_TARGET:
        print(f"Alvo de lucro atingido! +R${bankroll}. Pare o jogo.")
        break
    if LOSS_LIMIT is not None and bankroll <= -LOSS_LIMIT:
        print(f"Limite de perda atingido! -R${-bankroll}. Pare o jogo.")
        break

    # Decide próxima aposta
    next_bet = decide_next_bet()
    last_bet_side = next_bet
    print(f"\n>>> Sugestão de APOSTA: {next_bet} | Stake: R${current_stake}\n")
