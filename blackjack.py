from contextvars import copy_context
import random


class BlackJack:
    def __init__(self, amount=0, deck=None):
        self.amount = amount
        self.deck_already_made = False

        # If a player has a enough amount so play starts
        if self.amount <= 0:
            print(
                "You've ran out of money. Please restart this program to try again. Goodbye.")
        else:
            # Make new deck only begining of the game.
            # Otherwise use a already made one.
            if not self.deck_already_made:
                self.deck = Deck.make_deck()
                self.deck_already_made = True
            else:
                self.deck = deck

            self.start()

    def start(self):
        while True:
            play_or_no = input(
                f"You are starting with ${self.amount}. Would you like to play a hand? ")

            if play_or_no.lower() == 'yes':
                Hand(self.amount, self.deck)
                break

            if play_or_no.lower() == 'no':
                self.end()
                break

            BlackJack.start_game_validation(play_or_no)

    @staticmethod
    def start_game_validation(play_or_no):
        correct_options = ['yes', 'no']
        if play_or_no.lower() not in correct_options:
            print("This is not right format. Write eather yes or no. Try again")

    def end(self):
        self.deck_already_made = False
        print(f"You left the game with {self.amount}")


class Hand:
    def __init__(self, amount, deck):
        self.amount = amount
        self.deck = deck
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


class Play:
    def __init__(self, deck, bet, amount):
        self.deck = deck
        self.bet = bet
        self.amount = amount
        self.dealer_cards = []
        self.player_cards = []
        self.deal()

    def deal(self):

        Deck.shuffle(self.deck)

        self.dealing_cards_to_players()

        self.dealt_hand_info()

        # self.dealer_cards = []
        # test = ['8\u2666', '8\u2666']
        # self.dealer_cards.extend(test)
        # self.split_or_not()

        if self.is_there_blackjack():
            return

        self.hit_or_stay()

    # Dealing the cards
    def dealing_cards_to_players(self):
        for deal in range(1, 5):

            # Taiking a card from the deck.
            card_idex = random.randint(0, len(self.deck))
            card = self.deck.pop(card_idex)

            # Splting the dealing proccess according to the rule.
            # First card to the player second to the dealer.
            if deal % 2 == 0:
                self.dealer_cards.append(card)
            else:
                self.player_cards.append(card)

    # Showing dealt hand for both players.
    def dealt_hand_info(self):
        unknown = "Unknown"
        player_message = f"You are dealt: {Play.unpack_list(self.player_cards)}"
        dealer_message = f"The dealer is dealt: {self.dealer_cards[0]}, {unknown}"

        print(player_message)
        print(dealer_message)

    # Check to see if a player has a BlackJack.
    # If no he/she continues with hit_or_stay()clear

    def is_there_blackjack(self):
        player_cards_sum = Play.calculate_dealt_card_value(self.player_cards)
        if player_cards_sum == 21:

            print(f"The dealer has {Play.unpack_list(self.dealer_cards)}")
            dealer_cards_sum = Play.calculate_dealt_card_value(
                self.dealer_cards)

            if dealer_cards_sum != 21:
                print(f"Blackjack! You win ${self.bet * 1.5} :)")
                self.start_new_hand(self.amount + self.bet * 1.5)

            if dealer_cards_sum == 21:
                print(f"You tie. Your bet ${self.bet} has been returned.")
                self.start_new_hand(self.amount + self.bet)
            return True

        else:
            return False

    # Continue or keep the hand which was dealt.
    def hit_or_stay(self):
        correct_action = ['hit', 'stay']
        while True:
            # If player has not cards over 21 so hit proccess starts.
            if self.calculate_dealt_card_value(self.player_cards) <= 21:
                action = input("Would you like to hit or stay? ")

                if action.lower() in correct_action:

                    if action.lower() == correct_action[0]:
                        card = self.hit()
                        print(f"You are dealt: {card}")
                        print(
                            f"Now you have: {Play.unpack_list(self.player_cards)}")

                    if action.lower() == correct_action[1]:
                        self.dealers_hand()
                        break
                else:
                    print("Please write hit or stay. Try again.")
            else:
                print(
                    f"Your cards value is over 21 and you lose ${self.bet}")
                self.amount -= self.bet
                self.start_new_hand(self.amount)
                break

    # Dealers hand
    def dealers_hand(self):
        print(f"The dealer has: {Play.unpack_list(self.dealer_cards)}")
        dealer_cards_sum = Play.calculate_dealt_card_value(self.dealer_cards)
        player_cards_sum = Play.calculate_dealt_card_value(self.player_cards)

        while dealer_cards_sum < player_cards_sum:
            dealt_card = self.hit(player=False)
            print(f"The dealer hits and is dealt: {dealt_card}")
            print(f"The dealer has: {Play.unpack_list(self.dealer_cards)}")

            dealer_cards_sum = Play.calculate_dealt_card_value(
                self.dealer_cards)
        else:
            if dealer_cards_sum > 21:
                print(f"The dealer busts, you win ${self.bet} :)")
                self.start_new_hand(self.amount + self.bet)
            else:
                if dealer_cards_sum > player_cards_sum:
                    print("The dealer stays.")
                    print(f"The dealer wins, you lose ${self.bet} :(")
                    self.start_new_hand(self.amount - self.bet)

                if dealer_cards_sum == player_cards_sum:
                    print(f"You tie. Your bet ${self.bet} has been returned.")
                    self.start_new_hand(self.amount)

    # If player parameter is Flase
    # it adds a card to the dealer
    def hit(self, player=True):
        card_idex = random.randint(0, len(self.deck))
        card = self.deck.pop(card_idex)
        if player:
            self.player_cards.append(card)
        else:
            self.dealer_cards.append(card)
        return card

    # Start the new hand.
    def start_new_hand(self, amount):
        self.deck.extend(self.dealer_cards)
        self.deck.extend(self.player_cards)
        BlackJack(amount, self.deck)

    # Unpack the list to comma separated string
    @staticmethod
    def unpack_list(list):
        unpacked_list = ""
        comma = ", "
        for item in list:
            comma = "" if item == list[-1] else comma
            unpacked_list += item + comma
        return unpacked_list

    @staticmethod
    def calculate_dealt_card_value(list):
        # Unpacking list and if there is an Ace taking it and putting
        # it end of the list. Because with Ace end of the list it is
        # easy to determine the Ace value. Sould it be 11 or 1.
        sorted_list = []
        ace_list = ['A\u2666', 'A\u2665', 'A\u2663', 'A\u2660']
        last_append = []
        for item in list:
            if item in ace_list:
                last_append.append(item)
            else:
                sorted_list.append(item)
        sorted_list.extend(last_append)

        sum = 0
        face_cards = ['T', 'J', 'Q', 'K']
        card_without_suit = ""
        for item in sorted_list:

            # Grabbing a value without a suit
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
                       '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
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
