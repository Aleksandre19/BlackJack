import random
from deck import Deck
from validation import Validation


class Play:
    def __init__(self, amount):
        self.deck = None
        # self.bet = bet
        self.amount = amount
        self.dealer_cards = []
        self.player_cards = []
        self.player_over_21 = False
        # self.deal()
        self.start_hand()

    def start_hand(self):
        self.player_over_21 = False
        if self.check_balance():  # Check if a user has a sufficient amount

            # Check if a user wants to start play or not
            if Validation.confirm_start(self.amount):

                self.place_bet()

                self.deal_card()

                if self.is_there_blackjack():
                    return

                if not self.hit_or_stay():  # When a player stayes

                    if not self.player_over_21:
                        self.dealers_hand()  # Dealer playes
                    else:
                        self.start_new_hand(self.amount)

    def check_balance(self):
        # If a player has a enough amount so play starts
        if self.amount <= 0:
            print(
                "You've ran out of money. Please restart this program to try again. Goodbye.")
            return False
        else:
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

        # self.dealer_cards = []
        # test = ['8\u2666', '8\u2666']
        # self.dealer_cards.extend(test)
        # self.split_or_not()

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
                        return False
                        break
                else:
                    print("Please write hit or stay. Try again.")
            else:
                self.player_over_21 = True
                print(
                    f"Your cards value is over 21 and you lose ${self.bet}")
                self.amount -= self.bet
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
