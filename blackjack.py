import random


class Game:
    pass


class Deck:
    def __init__(self):
        self.deck = Deck.make_deck()

    @staticmethod
    def make_deck():
        card_values = ['2', '3', '4', '5', '6',
                       '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        card_suits = ["\u2666", "\u2665", "\u2663", "\u2660"]
        deck_list = []

        # Make a deck of cards
        for suit in card_suits:
            for value in card_values:
                deck_list.append(value + suit)

        return deck_list

    def shuffle(self):
        random.shuffle(self.deck)


class Players:
    pass
