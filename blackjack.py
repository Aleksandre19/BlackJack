import random


class BalckJack:
    def __init__(self, amount):
        self.amount = amount
        self.deck = Deck.make_deck()
        self.start()

    def start(self):
        while True:
            play_or_no = input(
                f"You are starting with ${self.amount}. Would you like to play a hand? ")

            if self.start_game_validation(play_or_no):
                Hand(self.deck, self.amount)
                break
            else:
                self.end()

    def start_game_validation(self, play_or_no):
        if play_or_no.lower() == "yes" or play_or_no.lower() == "no":
            if play_or_no.lower() == "yes":
                return True
            else:
                return False
        else:
            print("This is not right format. Write eather yes or no. Try again")

    def end(self):
        pass


class Hand:
    def __init__(self, deck, amount):
        self.deck = deck
        self.amount = amount
        self.start_hand()

    def start_hand(self):
        while True:
            bet = int(input("Place your bet: "))
            if self.validate_bet(bet):
                Play(self.deck)
                break

    def validate_bet(self, bet):
        if bet <= 0:
            print("Minimum amount of the bet is $1")
            return False
        elif bet > self.amount:
            print("You do not have sufficient funds.")
            return False
        else:
            return True

    def end_hand(self):
        pass


class Play:
    def __init__(self, deck):
        self.deck = deck
        self.deal()

    def deal(self):
        dealer_cards = []
        player_cards = []
        Deck.shuffle(self.deck)

        for deal in range(1, 5):
            card_idex = random.randint(0, len(self.deck))
            card = self.deck.pop(card_idex)
            if deal % 2 == 0:
                dealer_cards.append(card)
            else:
                player_cards.append(card)

        player_message = f"You are dealt: {player_cards[0]} {player_cards[1]}"
        dealer_message = f"The dealer is dealt: {dealer_cards[0]} {dealer_cards[1]}"

        print(player_message)
        print(dealer_message)


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

    @staticmethod
    def shuffle(deck):
        random.shuffle(deck)


game = BalckJack(500)


class Players:
    def __init__(self, name):
        self.name = name
