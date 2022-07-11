class Validation:
    @staticmethod
    def start_game_validation(play_or_no):
        correct_options = ['yes', 'no']
        if play_or_no.lower() not in correct_options:
            print("This is not right format. Write eather yes or no. Try again")

    @staticmethod
    def validate_bet(bet, amount):
        if bet <= 0:
            print("Minimum amount of the bet is $1")
            return False
        elif bet > amount:
            print("You do not have sufficient funds.")
            return False
        else:
            return True

    @staticmethod
    def confirm_start(amount):
        while True:
            play_or_no = input(
                f"You are starting with ${amount}. Would you like to play a hand? ")

            if play_or_no.lower() == 'yes':
                return True
                break

            if play_or_no.lower() == 'no':
                return False
                break

            Validation.start_game_validation(play_or_no)

    @staticmethod
    def validate_split(answer):
        valid_options = ['yes', 'no']

        if answer not in valid_options:
            print("Please enter yes or no ")
            return False

        return True
