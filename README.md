<h1 align="center">BlackJack</h1>

### Description.

This is a popular casino game - Blackjack which runs in to the terminal. It is intented for only one player who plays aginst dealer. In this game all blackJack rules are implemented incluiding: split, double down and insurance.

<h2 align="center"><img src="https://i.ibb.co/vqNC70R/terminal-screenshot.jpg"></h2>

### How to run the game?

In order to run the game it is necessary to download all files and run a main.py file in to your terminal.

### How to download?

Click on the green code button located above to the right corner of the listed files section and choose one of the download options.

### Various scenarios.

If you wish to test a separate rule of the Blackjack without waitting to get it during the game you can run the file named by various_scenarious.py in to your terminal instead of the main.py. Before runing it make sure that you read the description how to run which located on the top of the file.

<h2 align="center"><img src="https://i.ibb.co/qWqPB7w/various-scenarios.jpg"></h2>

###Technologies:

- Python 3.9.1
- Object Oriented Programming.
- Progamm is divided into five modules.
  - main.py - to run the game.
  - blackjack.py - It initiates a starting amount and starts the play.
  - play_hand.py - for all the logics of the game.
  - deck.py - for handling a deck.
  - validation.py - for the validation methods.
  - various_scenarios.py - testing for various combinations.

### Objective.

The objective of Blackjack is to end the hand/round with a hand that has a higher value than the hand the dealer has, without going over 21. The value of your hand is determined by the cards in it. Any face card (King, Queen or Jack) is given a value of 10, an ace can have a value of 1 or 11 (whichever benefits you more) and all other cards have a value equal to their number (i.e. all threes have a value of 3). For example, if you have a hand containing a three, two, king and ace your hand has a value of 16; in this case the ace is treated at 1 because if it were to be treated as 11 you would have 26 and be over 21. If at any point the value of your hand is over 21 you immediately lose, and your bet is lost, this is called a bust.

### General Hand/round flow.

The dealer deals two cards to the player and two cards to itself one by one. Dealers first card is visible. After dealing a cards the player makes a bet. Then a player has a general three option hit, double or stay. Hit to add a card, double to double the current bet and a stay option to keep the current cards. After doubling the bet a player gets only one card. After the player's turn it is a dealer's turn. In the end the player's and the dealer's hands sums up. The one wins whos hand is more than an other's without overcomign 21.

### Rules:

- #### Blackjack.
  If a player is dealt a hand with a value of 21 this is considered a natural or "blackjack". If the player has a natural and the dealer does not the dealer pays the player 1,5 times their original bet and the hand is immediately over. If dealer has also Blackjack then it is tie and original bet returns to the player.
  <h2 align="center"><img src="https://i.ibb.co/jRRCZ8R/blackjack-player-wins.jpg"></h2>
  <h2 align="center"><img src="https://i.ibb.co/35bKkRs/blackjack-tie-example.jpg"></h2>
- #### Split.
  If a player gets two same card for example 7 and 7 he/she gets right to split the hand. In case of split the bet doubles and each hands playes separately as a usually one.
  <h2 align="center"><img src="https://i.ibb.co/gvNz9yf/split-example.jpg"></h2>
- #### Insurance.
  If a dealer's first card is a ace then a player has a option to insurance aginst Blackjack by betting half of his original bet. If a player makes a insurance then the dealer checks if there is a blackjack or not. If so the dealer pays 2:1 of the insurance amount and takes the original bet. And if there is no blackjack then the player loses the bet of the insurance and game continues as usual.
  <h2 align="center"><img src="https://i.ibb.co/1K9cR3d/insurance-example.jpg"></h2>
- #### More information.
  For more information please visit to the [Wikipedia](https://en.wikipedia.org/wiki/Blackjack).
