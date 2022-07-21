from play_hand import Play
"""
In this file you can test various combinations in the 
BlackJack without waitting to get it durring play.
For example if you wish to see how the Split rule
is implemented in this game you can simply find a
appropriate section, uncomment it, comment an other
combination (which is uncommented) and run this
file instead of main.py in to your terminl.

Easy way to comment/uncomment:
command + / on the mac and ctr + / on the windows.

The combinations are seperated by descriptions
in the multi-line comments.

By default the combination by which a player
has a BlackJack is uncommented. 
"""

# Suits of the cards
dimond_suit = "\u2666"
heart_suit = "\u2665"

"""
Player has a BlackJack.
"""
player_hand = [f'A{dimond_suit}', f'K{heart_suit}']
dealer_hand = [f'A{dimond_suit}', f'2{heart_suit}']

"""
Dealer has a BlackJack.
"""
# player_hand = [f'A{dimond_suit}', f'5{heart_suit}']
# dealer_hand = [f'K{dimond_suit}', f'A{heart_suit}']

"""
Split rule.
"""
# player_hand = [f'T{dimond_suit}', f'T{heart_suit}']
# dealer_hand = [f'7{dimond_suit}', f'A{heart_suit}']

"""
Split rule with Aces.
"""
# player_hand = [f'A{dimond_suit}', f'A{heart_suit}']
# dealer_hand = [f'7{dimond_suit}', f'A{heart_suit}']

"""
Insurance rule when a dealer has a BlackJack.
"""
# player_hand = [f'T{dimond_suit}', f'6{heart_suit}']
# dealer_hand = [f'A{dimond_suit}', f'K{heart_suit}']

"""
Insurance rule when a dealer doesn't have a BlackJack.
"""
# player_hand = [f'T{dimond_suit}', f'6{heart_suit}']
# dealer_hand = [f'A{dimond_suit}', f'2{heart_suit}']

"""
Double down rule.
"""
# player_hand = [f'7{dimond_suit}', f'4{heart_suit}']
# dealer_hand = [f'7{dimond_suit}', f'2{heart_suit}']


class VariousScenarios(Play):
    def __init__(self, amount):

        # Calling the parent's constructor.
        super().__init__(amount=amount)

    def deal_card(self):
        self.player_cards = player_hand
        self.dealer_cards = dealer_hand

        super().dealt_hand_info()


VariousScenarios(500)
