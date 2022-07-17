"""
This class implements a deck functionality.
It creates a deck and shuffles it with a 
separate functions.
"""
import random


class Deck:
    def __init__(self):
        self.deck = Deck.make_deck()

    @staticmethod
    def make_deck():
        card_values = ['2', '3', '4', '5', '6',
                       '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        card_suits = ["\u2666", "\u2665", "\u2663", "\u2660"]
        deck_list = []

        # Make a deck.
        for suit in card_suits:
            for value in card_values:
                deck_list.append(value + suit)

        return deck_list

    @staticmethod
    def shuffle(deck):
        random.shuffle(deck)
