import random


class HangmanGame:
    secret_words = ['python', 'java', 'swift', 'javascript']
    initial_message = 'H A N G M A N  # 8 attempts'
    input_message = 'Input a letter: '
    stop_message = 'Thanks for playing!'

    def __init__(self, attempts: int):
        self.secret_word: str = random.choice(HangmanGame.secret_words)
        self.shadowed_secret_word = "-" * len(self.secret_word)
        self.attempts = attempts
        self.letters_position = {}

        self.__get_letters_position()

    def __get_letters_position(self):
        for index, letter in enumerate(self.secret_word):
            self.letters_position.setdefault(letter, []).append(index)

    def play(self):
        print(HangmanGame.initial_message, end='\n\n')

        while self.attempts > 0:
            self.attempts -= 1
            print(self.shadowed_secret_word)
            self.single_move(input(HangmanGame.input_message))
            print()
            if self.attempts < 1:
                print(HangmanGame.stop_message)

    def single_move(self, letter):
        letter = letter.lower()
        found_index = self.secret_word.find(letter)

        if found_index == -1:
            print(f"That letter doesn't appear in the word.")
        else:
            for index in self.letters_position[letter]:
                if index < len(self.shadowed_secret_word) - 1:
                    self.shadowed_secret_word = (f'{self.shadowed_secret_word[:index]}{letter}'
                                                 f'{self.shadowed_secret_word[index + 1:]}')
                else:
                    self.shadowed_secret_word = f'{self.shadowed_secret_word[:index]}{letter}'


if __name__ == '__main__':
    hangman = HangmanGame(8)
    hangman.play()
