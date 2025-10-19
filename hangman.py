import random
import re

class HangmanRules:
    def __init__(self, pattern=r'[a-z]', required_length=1):
        self.input_pattern = re.compile(pattern)
        self.required_length = required_length

    def check_letter_correctness(self, letter) -> bool:
        """
        By default, checks that the player entered a lowercase English letter.
        Or if it agrees with any other pattern you passed into __init__.

        :param letter: letter to check
        """
        if self.input_pattern.match(letter) is None:
            print('Please, enter a lowercase letter from the English alphabet.')
            return False
        return True

    def check_if_single_letter(self, letter) -> bool:
        """ Checks whether players enter exactly one letter. """
        if len(letter) != self.required_length:
            print('Please, input a single letter.')
            return False
        return True

    @staticmethod
    def letter_not_repeated(letter, reference_iterable: set | list | tuple | str) -> bool:
        """ Checks whether a letter is repeated. """
        result = True
        if letter in reference_iterable:
            print("You've already guessed this letter.")
            result = False
        return result

    def check_input_correctness(self, letter, reference_iterable):
        """
        Launches user input correctness checking.

        Uses methods defined in HangmanRules (above).
        None of the three errors described above should reduce the number of remaining attempts!

        :param letter: letter to check
        :param reference_iterable: iterable of letters to check

        :return: True if all letters are correct, False otherwise
        """
        return (self.check_if_single_letter(letter)
                and self.check_letter_correctness(letter)
                and self.letter_not_repeated(letter, reference_iterable))


class HangmanGame(HangmanRules):
    secret_words = ['python', 'java', 'swift', 'javascript']
    initial_message = 'H A N G M A N  # 8 attempts'
    input_message = 'Input a letter: '
    stop_message = 'Thanks for playing!'
    wins_lost_messages = {
        0: "\nYou lost!",
        1: "You guessed the word <PLACEHOLDER>!\nYou survived!",
    }

    def __init__(self, attempts: int, input_pattern=r'[a-z]'):
        super().__init__(input_pattern)
        self.secret_word: str = random.choice(HangmanGame.secret_words)
        self.shadowed_secret_word = "-" * len(self.secret_word)
        self.attempts = attempts
        self.letters_position = {}
        self.user_wins = 0
        self.letters_used = set()

        self.__get_letters_position()

    def __get_letters_position(self):
        for index, letter in enumerate(self.secret_word):
            self.letters_position.setdefault(letter, []).append(index)

    def play(self):
        print(HangmanGame.initial_message, end='\n\n')
        print(self.shadowed_secret_word, end='\n')

        while self.attempts > 0:
            correct_answer = self.single_move(input(HangmanGame.input_message))

            if self.secret_word == self.shadowed_secret_word:
                self.user_wins = 1
                self.attempts = 0

            if not correct_answer:
                self.attempts -= 1

            if self.attempts <= 0:

                message_prefix = f'\n{self.shadowed_secret_word}\n' if '-' not in self.shadowed_secret_word else ''
                print(self.__return_stop_message(message_prefix))
            else:
                print(f'\n{self.shadowed_secret_word}', end='\n')

    def single_move(self, letter) -> bool:
        result = False

        if not self.check_input_correctness(letter, self.letters_used):
            return True

        # add letter to letters_used set for check it in further moves
        self.letters_used.add(letter)

        found_index = self.secret_word.find(letter)

        if found_index == -1:
            print(f"That letter doesn't appear in the word.  # {self.attempts - 1} attempts")
        elif letter in self.shadowed_secret_word:
            print("No improvements.")
        else:
            for index in self.letters_position[letter]:
                if index < len(self.shadowed_secret_word) - 1:
                    self.shadowed_secret_word = (f'{self.shadowed_secret_word[:index]}{letter}'
                                                 f'{self.shadowed_secret_word[index + 1:]}')
                else:
                    self.shadowed_secret_word = f'{self.shadowed_secret_word[:index]}{letter}'
            result = True
        return result

    def __return_stop_message(self, message_prefix):
        msg = f'{message_prefix}{HangmanGame.wins_lost_messages.get(self.user_wins)}'
        if '<PLACEHOLDER>' in msg:
            msg = msg.replace('<PLACEHOLDER>', self.secret_word)
        return msg


if __name__ == '__main__':
    hangman = HangmanGame(8)
    hangman.play()
