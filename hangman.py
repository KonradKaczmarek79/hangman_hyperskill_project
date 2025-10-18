import random


class HangmanGame:
    secret_words = ['python', 'java', 'swift', 'javascript']
    initial_message = 'H A N G M A N  # 8 attempts'
    input_message = 'Input a letter: '
    stop_message = 'Thanks for playing!'
    wins_lost_messages = {
        0: "\nYou lost!",
        1: "You guessed the word!\nYou survived!",
    }

    def __init__(self, attempts: int):
        self.secret_word: str = random.choice(HangmanGame.secret_words)
        self.shadowed_secret_word = "-" * len(self.secret_word)
        self.attempts = attempts
        self.letters_position = {}
        self.user_wins = 0

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
                print(f'{message_prefix}{HangmanGame.wins_lost_messages.get(self.user_wins)}')
            else:
                print(f'\n{self.shadowed_secret_word}', end='\n')

    def single_move(self, letter) -> bool:
        letter = letter.lower()
        found_index = self.secret_word.find(letter)
        result = False

        if found_index == -1:
            print(f"That letter doesn't appear in the word.")
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


if __name__ == '__main__':
    hangman = HangmanGame(8)
    hangman.play()
