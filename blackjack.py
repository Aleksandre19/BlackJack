import random


class BlackJack:
    def __init__(self, amount):
        self.amount = amount
        self.deck = Deck.make_deck()
        self.start()

    def start(self):
        while True:
            play_or_no = input(
                f"You are starting with ${self.amount}. Would you like to play a hand? ")

            if play_or_no.lower() == 'yes':
                Hand(self.deck, self.amount)
                break

            if play_or_no.lower() == 'no':
                break

            self.start_game_validation(play_or_no)

    def start_game_validation(self, play_or_no):
        if play_or_no.lower() != "yes" or play_or_no.lower() != "no":
            print("This is not right format. Write eather yes or no. Try again")

    def end(self):
        pass


class Hand:
    def __init__(self, deck, amount):
        self.deck = deck
        self.amount = amount
        self.bet = 0
        self.start_hand()

    def start_hand(self):
        while True:
            bet = int(input("Place your bet: "))
            if self.validate_bet(bet):
                self.bet = bet
                Play(self.deck, self.bet, self.amount)
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
    def __init__(self, deck, bet, amount):
        self.deck = deck
        self.bet = bet
        self.amount = amount
        self.dealer_cards = []
        self.player_cards = []
        self.deal()

    def deal(self):
        unknown = "Unknown"
        Deck.shuffle(self.deck)

        for deal in range(1, 5):
            card_idex = random.randint(0, len(self.deck))
            card = self.deck.pop(card_idex)
            if deal % 2 == 0:
                self.dealer_cards.append(card)
            else:
                self.player_cards.append(card)

        player_message = f"You are dealt: {self.player_cards[0]} {self.player_cards[1]}"
        dealer_message = f"The dealer is dealt: {self.dealer_cards[0]} {unknown}"

        print(player_message)
        print(dealer_message)

        # dealer_cards = ['A\u2666', '7\u2666', '6\u2666']
        # Play.calculate_dealt_card_value(player_cards)
        self.hit_or_stay()

    def hit_or_stay(self):
        while True:
            # If player has not cards over 21 so hit proccess starts.
            if self.calculate_dealt_card_value(self.player_cards) <= 21:
                action = input("Would you like to hit or stay? ")
                if action.lower() == "hit" or action.lower() == "stay":

                    if action.lower() == "hit":
                        card = self.hit()
                        print(f"You are dealt: {card}")
                        print(f"Now you have: {self.player_cards}")

                    if action.lower() == "stay":
                        pass
                        break
                else:
                    print("Please write hit or stay. Try again.")
            else:
                print(
                    f"Your cards value is over 21 and you lose ${self.bet}")
                self.amount -= self.bet
                BlackJack(self.amount)
                break

    # If player parameter is True
    # it adds a card to the player

    def hit(self, player=True):
        card_idex = random.randint(0, len(self.deck))
        card = self.deck.pop(card_idex)
        if player:
            self.player_cards.append(card)
        else:
            self.dealer_cards.append(card)

        return card

    @staticmethod
    def calculate_dealt_card_value(list):
        # Sort a list to push Ace to the end of the list.
        # It is easy to calculate Ace value end of the list.
        sorted_list = sorted(list)

        sum = 0
        face_cards = ['J', 'Q', 'K']
        card_without_suit = ""
        for item in sorted_list:
            # Chek to find if card begins with 1
            # If so it means that it is 10 and that is way
            # We grabb first two letters.
            # If not we grabb only one letter
            if item[0] == "1":
                card_without_suit = item[:2]
            else:
                card_without_suit = item[0]

            # If letter is face card so it's value is 10
            if card_without_suit in face_cards:
                sum += 10
            # If the sum and a Ace is more than 21 or equals to 21
            # then Ace value is 11 else it is 1
            elif card_without_suit.upper() == "A":
                if (sum + 11) <= 21:
                    sum += 11
                else:
                    sum += 1
            # If letter is digit it adds to sum converted
            # to the integer
            else:
                sum += int(card_without_suit)

        return sum


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


game = BlackJack(500)


class Players:
    def __init__(self, name):
        self.name = name
