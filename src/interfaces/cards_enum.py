CARDS = {
    "Rabbit": [(-1, -1), (1, 1), (2, 0)],
    "Cobra": [(-1, 0), (1, 1), (1, -1)],
    "Rooster": [(-1, 0), (-1, -1), (1, 1), (1, 0)],
    "Tiger": [(0, 2), (0, -1)],
    "Monkey": [(-1, -1), (-1, 1), (1, -1), (1, 1)]
}

CARDS_ID = {card: i for i, card in enumerate(CARDS, 0)}

print(CARDS_ID)