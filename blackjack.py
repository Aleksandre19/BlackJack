from validation import Validation

from play_hand import Play


class BlackJack:
    def __init__(self, amount=0):

        self.amount = amount

        Play(self.amount)

    def end(self):
        self.deck_already_made = False
        print(f"You left the game with {self.amount}")
