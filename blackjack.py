"""
This file initiates a parent class with a
start amount and calls to the Play class.
"""
from play_hand import Play


class BlackJack:
    def __init__(self, amount=0):
        self.amount = amount
        Play(self.amount)
