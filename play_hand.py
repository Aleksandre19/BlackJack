import random
from deck import Deck
from validation import Validation


class Play:
    def __init__(self, amount):
        self.deck = None
        self.amount = amount
        self.dealer_cards = []
        self.player_cards = []
        self.player_over_21 = False
        self.save_player_cards = None
        self.save_dealer_cards = None
        self.splitted = False
        self.split_aces = False
        self.split_doubled = False
        self.split_first_double = 0
        self.split_second_double = 0
        self.splitted_blackjack = False

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

                self.check_incurance()

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
            bet = input("Place your bet: ")
            if Validation.validate_bet(bet, self.amount):
                self.bet = int(bet)
                break

    def deal_card(self):

        Deck.shuffle(self.deck)

        self.dealing_cards_to_players()

        self.dealt_hand_info()

        # self.player_cards = []
        # test = ['2\u2666', '2\u2665']
        # self.player_cards.extend(test)

        # self.dealer_cards = []
        # test = ['2\u2666', '5\u2665']
        # self.dealer_cards.extend(test)

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
        dealer_message = f"The dealer is dealt: {self.dealer_cards[0]}, {unknown}"

        print(player_message)
        print(dealer_message)

    # Dedact a insurance case
    def check_incurance(self):

        if self.dealer_cards[0][0] == 'A':

            answer = input("Dealer has a A. Do you want to insurance? ")
            if Validation.yes_or_no(answer.lower()):

                if answer.lower() == 'no':
                    return False

                check_dealers_cards = Play.calculate_dealt_card_value(
                    self.dealer_cards)

                if check_dealers_cards == 21:

                    show_dealer_cards = Play.unpack_list(self.dealer_cards)

                    print(f"Dealer has a blackjack: {show_dealer_cards}.")
                    print(
                        f"You win {self.bet} for insurance and lose you initial bet: {self.bet}")

                    self.start_new_hand(self.amount)
                    return True

                else:
                    print(
                        f"Dealer doesn't have a blackjack. Dealer takes you insurance: {self.bet / 2}")
                    self.amount -= self.bet / 2

                return False

        return False

    # Check to see if a player has a BlackJack.
    # If no he/she continues with hit_or_stay()clear
    def is_there_blackjack(self, player=True):

        player_cards_sum = Play.calculate_dealt_card_value(self.player_cards)
        if player_cards_sum == 21:

            print(f"The dealer has {Play.unpack_list(self.dealer_cards)}")

            dealer_cards_sum = Play.calculate_dealt_card_value(
                self.dealer_cards)

            if dealer_cards_sum != 21:
                print(f"Blackjack! You win ${self.bet * 1.5} :)")

                if self.splitted:
                    self.splitted_blackjack = True

                if not self.splitted:
                    self.start_new_hand(self.amount + self.bet * 1.5)

            if dealer_cards_sum == 21:
                print(f"You tie. Your bet ${self.bet} has been returned.")

                if not self.splitted:
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

                if Validation.yes_or_no(answer.lower()):

                    if answer.lower() == 'no':
                        return False

                    self.splitted = True

                    # save the bet for a double down case
                    save_bet_for_split = self.bet

                    # Check if there are two aces and and play according to rule
                    if self.player_cards[0][0] == 'A' and self.player_cards[1][0] == 'A':
                        self.split_aces = True

                    # Play first splitted hand
                    first_hand = self.split_hand(1)

                    # Give back the second dealt card to the player
                    self.player_cards = self.save_player_cards

                    # Play second splitted hand
                    second_hand = self.split_hand(2)

                    hands = [first_hand, second_hand]

                    # Play hands with dealer
                    for key, hand in enumerate(hands):

                        # Restore a basic value of the bet
                        self.bet = save_bet_for_split

                        hand_number = "first" if key == 0 else "second"

                        if 'over_21' not in hand:

                            self.player_cards = hand

                            print("")
                            print(
                                f"In the {hand_number} hand you have {Play.unpack_list(hand)}")

                            # If there was a double down so determine the bet amount
                            if key == 0 and self.split_first_double != 0:
                                self.bet = self.split_first_double

                            if key == 1 and self.split_second_double != 0:
                                self.bet = self.split_second_double

                            # Dealer's turn
                            result = self.dealer_turn()

                            # Player wins
                            if result == "wins":

                                if self.splitted_blackjack:
                                    self.amount += self.bet * 1.5

                                if not self.splitted_blackjack:
                                    self.amount += self.bet

                                self.splitted_blackjack = False

                            # Dealer wins
                            elif result == "lose":
                                self.amount -= self.bet

                            # It's tie
                            elif result == "tie":
                                pass

                        else:

                            # Player gets over 21
                            print(
                                f"In the {hand_number} hand you bust. Dealer wins {self.bet}")
                            self.amount -= self.bet

                    self.splitted = False
                    self.split_aces = False
                    self.split_first_double = 0
                    self.split_second_double = 0

                    self.start_new_hand(self.amount)
                    return True

        else:
            return False

    def split_hand(self, split_hand):

        self.prepare_cards_for_split()

        print("")
        print(f"Now you play with a: {Play.unpack_list(self.player_cards)}")

        self.player_turn()

        if self.split_doubled and split_hand == 1:
            self.split_doubled = False
            self.split_first_double = self.bet * 2

        if self.split_doubled and split_hand == 2:
            self.split_doubled = False
            self.split_second_double = self.bet * 2

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

        while True:
            # If player has not cards over 21 so hit proccess starts.
            if self.calculate_dealt_card_value(self.player_cards) <= 21:

                # Manage a message appearance
                action, correct_action = self.manage_msg_appearance()

                if action.lower() in correct_action:

                    # User hits
                    if action.lower() == correct_action[0]:

                        # If a hand is splitted and there are two aces than by the
                        # rule player gets only one card.
                        # Otherwise he/she gets as many as wished
                        if self.split_aces:
                            self.hit()
                            break
                        else:
                            self.hit()

                    if action == "double":
                        if "double" in correct_action:
                            if self.double_down(action, correct_action):
                                break

                    if action.lower() == correct_action[correct_action.index("stay")]:
                        return False

                else:
                    print("Please write hit or stay. Try again.")
            else:
                self.player_over_21 = True

                if not self.splitted:
                    print(
                        f"Your cards value is over 21 and you lose ${self.bet}")
                    self.amount -= self.bet
                else:
                    print(
                        f"You have got a cards over 21 and you busts in this hand.")
                break

    # Dealers hand
    def dealer_turn(self):

        if self.splitted:
            if self.is_there_blackjack():
                return 'wins'

        print(f"The dealer has: {Play.unpack_list(self.dealer_cards)}")
        dealer_cards_sum = Play.calculate_dealt_card_value(self.dealer_cards)
        player_cards_sum = Play.calculate_dealt_card_value(self.player_cards)

        while dealer_cards_sum < 17:
            self.hit(player=False)

            dealer_cards_sum = Play.calculate_dealt_card_value(
                self.dealer_cards)
        else:

            if dealer_cards_sum > 21:
                print(f"The dealer busts, you win ${self.bet} :)")

                if not self.splitted:
                    self.start_new_hand(self.amount + self.bet)
                else:
                    return "wins"

            else:

                if dealer_cards_sum > player_cards_sum:
                    print("The dealer stays.")
                    print(f"The dealer wins, you lose ${self.bet} :(")

                    if not self.splitted:
                        self.start_new_hand(self.amount - self.bet)
                    else:
                        return "lose"

                if dealer_cards_sum < player_cards_sum:
                    print(f"You win and dealer lose ${self.bet} :)")

                    if not self.splitted:
                        self.start_new_hand(self.amount + self.bet)
                    else:
                        return "wins"

                if dealer_cards_sum == player_cards_sum:

                    tie_bet = self.bet / 2 \
                        if self.split_first_double > 0 or \
                        self.split_second_double > 0 \
                        else self.bet

                    print(f"You tie. Your bet ${tie_bet} has been returned.")

                    if not self.splitted:
                        self.start_new_hand(self.amount)
                    else:
                        return "tie"

    def manage_msg_appearance(self):

        correct_action = ['hit', 'stay']

        if len(self.player_cards) == 2:
            correct_action.insert(1, "double")
            action_msg = "hit, double or stay"
        else:
            correct_action = ['hit', 'stay']
            action_msg = "hit or stay"

        # Get a inout from user
        action = input(f"Would you like to {action_msg}? ")
        return action, correct_action

    # This implements double down rule in blackjack
    def double_down(self, action="", correct_action=[]):
        # Doubling down a hand
        if action.lower() == correct_action[1] and len(self.player_cards) == 2:

            # Check to see if there is split or no
            if not self.splitted:
                self.bet = self.bet * 2
            else:
                self.split_doubled = True

            # Add a card
            self.hit()

            # Check if a player goes over 21
            if self.calculate_dealt_card_value(self.player_cards) > 21:
                self.player_over_21 = True

            return True

    # If player parameter is Flase
    # it adds a card to the dealer
    def hit(self, player=True):

        # Deal a last card from the deck
        card = self.deck.pop(len(self.deck) - 1)

        unpack = None
        p_message = ""
        card_message = ""

        if player:  # Players turn
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
