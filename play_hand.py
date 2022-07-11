import random
from deck import Deck
from validation import Validation
# import asyncio


class Play:
    def __init__(self, amount):
        self.deck = None
        self.amount = amount
        self.dealer_cards = []
        self.player_cards = []
        self.player_over_21 = False
        self.save_player_cards = None
        self.save_dealer_cards = None
        self.splited = False
        self.start_hand()

    def start_hand(self):

        # True when a player goes over 21
        self.player_over_21 = False

        # Check if a user has a sufficient amount
        if self.check_balance():

            # Check if a user wants to start play or not
            if Validation.confirm_start(self.amount):

                self.place_bet()

                self.deal_card()

                # Check to see if a player got a BlackJack
                if self.is_there_blackjack():
                    return

                if self.split():
                    return

                # Player's turn
                if not self.player_turn():

                    # If a player doesn't goes over 21 by adding the cards
                    if not self.player_over_21:

                        # Dealer's turn
                        self.dealer_turn()

                    else:
                        # If a player goes over 21 than starting a new hand
                        self.start_new_hand(self.amount)

    def check_balance(self):
        # If a player has a enough amount so play starts
        # and maiking a deck of cards
        if self.amount <= 0:
            print(
                "You've ran out of money. Please restart this program to try again. Goodbye.")
            return False
        else:
            # Make a deck of cards
            self.deck = Deck.make_deck()
            return True

    def place_bet(self):
        while True:
            bet = int(input("Place your bet: "))
            if Validation.validate_bet(bet, self.amount):
                self.bet = bet
                break

    def deal_card(self):

        Deck.shuffle(self.deck)

        self.dealing_cards_to_players()

        self.dealt_hand_info()

        self.player_cards = []
        test = ['2\u2666', '2\u2665']
        self.player_cards.extend(test)
        # self.split_or_not()

    # Dealing the cards

    def dealing_cards_to_players(self):
        for deal in range(1, 5):

            # Taiking a card from the deck.
            card_idex = random.randint(0, len(self.deck) - 1)
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
        dealer_message = f"The dealer is dealt: {unknown}, {self.dealer_cards[1]}"

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

    def split(self):
        # Grabbing only digits from the player's cards
        # and checking if they are equal to each other.
        if self.player_cards[0][0] == self.player_cards[1][0]:
            while True:
                print(
                    f"You have two {self.player_cards[0]}, {self.player_cards[1]}")
                answer = input("Would you like to split? yes/no: ")

                if Validation.validate_split(answer.lower()):

                    if answer.lower() == 'no':
                        return False

                    self.splited = True

                    # Play first splited hand
                    first_hand = self.split_hand()

                    # Give back the second dealt card to the player
                    self.player_cards = self.save_player_cards

                    # Play second splited hand
                    second_hand = self.split_hand()

                    hands = [first_hand, second_hand]

                    # Save dealer's starting cards for second hand
                    self.save_dealer_cards = tuple(self.dealer_cards)

                    # Play hands with dealer
                    for key, hand in enumerate(hands):
                        hand_number = "first" if key == 0 else "second"

                        if 'over_21' not in hand:

                            self.player_cards = hand

                            print(
                                f"You play {hand_number} hand. In this hand you have {Play.unpack_list(hand)}")

                            # Dealer's turn
                            result = self.dealer_turn()

                            # Returning a starting hand to dealer
                            self.dealer_cards = list(self.save_dealer_cards)

                            # Player wins
                            if result == "wins":
                                self.amount += self.bet

                            # Dealer wins
                            elif result == "lose":
                                self.amount -= self.bet

                            # It's tie
                            elif result == "tie":
                                print(
                                    f"You tie. Your bet ${self.bet} has been returned.")

                        else:
                            # Player gets over 21
                            print(
                                f"In the {hand_number} you bust. Dealer wins {self.bet}")

                    self.splited = False

                    self.start_new_hand(self.amount)

                    return True
        else:
            return False

    def split_hand(self):
        self.prepare_cards_for_split()

        print(f"Now you play with a: {Play.unpack_list(self.player_cards)}")

        self.player_turn()

        # If player gets over 21 than the cards
        # doesn't add in to the player's stock.
        # Instead it adds 'over_21'message
        if self.player_over_21:
            self.player_cards = ['over_21']

        return self.player_cards

    def prepare_cards_for_split(self):

        self.player_over_21 = False

        # Save player's cards
        self.save_player_cards = self.player_cards

        # Cleaning player's stock
        self.player_cards = []

        # Adding first card to the player's stock
        self.player_cards.append(self.save_player_cards.pop(0))

    # Continue or keep the hand which was dealt.
    def player_turn(self):
        correct_action = ['hit', 'stay']
        while True:
            # If player has not cards over 21 so hit proccess starts.
            if self.calculate_dealt_card_value(self.player_cards) <= 21:
                action = input("Would you like to hit or stay? ")

                if action.lower() in correct_action:

                    if action.lower() == correct_action[0]:
                        self.hit()

                    if action.lower() == correct_action[1]:
                        return False
                        break
                else:
                    print("Please write hit or stay. Try again.")
            else:
                self.player_over_21 = True

                if not self.splited:
                    print(
                        f"Your cards value is over 21 and you lose ${self.bet}")
                    self.amount -= self.bet
                else:
                    print(
                        f"You have got a cards over 21 and you busts in this hand.")
                break

    # Dealers hand
    def dealer_turn(self):
        print(f"The dealer has: {Play.unpack_list(self.dealer_cards)}")
        dealer_cards_sum = Play.calculate_dealt_card_value(self.dealer_cards)
        player_cards_sum = Play.calculate_dealt_card_value(self.player_cards)

        while dealer_cards_sum < player_cards_sum:
            self.hit(player=False)

            dealer_cards_sum = Play.calculate_dealt_card_value(
                self.dealer_cards)
        else:

            if dealer_cards_sum > 21:
                print(f"The dealer busts, you win ${self.bet} :)")

                if not self.splited:
                    self.start_new_hand(self.amount + self.bet)
                else:
                    return "wins"

            else:

                if dealer_cards_sum > player_cards_sum:
                    print("The dealer stays.")
                    print(f"The dealer wins, you lose ${self.bet} :(")

                    if not self.splited:
                        self.start_new_hand(self.amount - self.bet)
                    else:
                        return "lose"

                if dealer_cards_sum == player_cards_sum:
                    print(f"You tie. Your bet ${self.bet} has been returned.")

                    if not self.splited:
                        self.start_new_hand(self.amount)
                    else:
                        return "tie"

    # If player parameter is Flase
    # it adds a card to the dealer

    def hit(self, player=True):

        # Deal a last card from the deck
        card = self.deck.pop(len(self.deck) - 1)
        unpack = None
        p_message = ""
        card_message = ""

        if player:
            self.player_cards.append(card)
            unpack = self.player_cards
            p_message = "You are dealt: "
            card_message = "Now you have: "
        else:  # Here is dealer's turn
            self.dealer_cards.append(card)
            unpack = self.dealer_cards
            p_message = "The dealer hits and is dealt: "
            card_message = "The dealer has: "

        print(f"{p_message} {card}")
        print(
            f"{card_message} {Play.unpack_list(unpack)}")

        return card

    # Start the new hand.
    def start_new_hand(self, amount):
        self.amount = amount
        self.player_cards = []
        self.dealer_cards = []
        self.start_hand()

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
        # easy to determine the Ace value, Sould it be 11 or 1.
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
