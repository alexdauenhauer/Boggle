import time
import os
from random import randint, shuffle

'''
This is a command line version of the classic game Boggle. The user 
will run "python boggle.py" from the command line and will enter the 
game at that point. The general idea, which is explained better in the 
Instructions and Rules class, is that the player will have two minutes to 
enter as many words as they can find on the board. Once the time is up, they 
will be presented with a score and what words they missed and what 
words scored points.
'''

class Board:
    """This class is the class that controls the display of letters 
    that the user sees. The input is the size of the board as an int. 
    The board will always be a square, so the input is only a single 
    int for the current version. The output is a Board object which 
    can be shuffled and displayed.
    """

    # boggle letter block distribution. Each entry represents a 
    # six-sided cube, with each letter representing a side.
    letterBlocks = [
        'AAEEGN',
        'ABBJOO',
        'ACHOPS',
        'AFFKPS',
        'AOOTTW',
        'CIMOTV',
        'DELRVY',
        'DEILRX',
        'DISTTY',
        'EEGHNW',
        'EEINSU',
        'EHRTVW',
        'EIOSST',
        'ELRTTY',
        'HIMNQU',
        'HLNNRZ',
    ]

    def __init__(self, size=4):
        """The only allowable size that is currently implemented is 
        size = 4 (4x4 grid). This is the standard size of the boggle 
        board. Future iterations may include the ability to expand the 
        size the standard size letter blocks. Leaving it as an input 
        variable in case I have time later to implement different 
        board sizes
        """
        if size != 4:
            raise NotImplementedError(
                """board sizes other than four are not implemented at 
                this time"""
            )
        else:
            self.size = size

    def shuffle_board(self):
        """
        Arrange all the letter blocks and then "shake" the board so 
        that each space on the board shows a single side of each of 
        the letterBlocks.
        """

        self.board = [Board.letterBlocks[j] for j in range(self.size**2)]
        shuffle(self.board)
        self.board = [self.board[i][randint(0, 5)]
                      for i in range(len(self.board))]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        self.presenter = [[self.board[j + i * 4] for j in range(self.size)]
                          for i in range(self.size)]
        for i, row in enumerate(self.presenter):
            self.presenter[i] = '  '.join(row)
        self.presenter = '\n\n'.join(self.presenter)
        return self.presenter


class Instructions:
    """This class contains the gameplay instructions and a method to 
    display them. There are no unique instancecs of this class, so no 
    need for an __init__ method.
    """

    instructions = [
        "This is a 1-player version of a classic game of word search",
        "When you start a new game, the board's letters will be shuffled",
        "and the board will be presented to you. You will then have",
        "two minutes to find as many words as you can and enter them into",
        "the input cell. When the two minutes is up, the round will end",
        "and you will be presented with your score."
    ]

    def show():
        for line in Instructions.instructions:
            line.lstrip()
            print(line)


class Rules:
    """This class contains the rules of the game and methods to 
    display the rules, as well as to apply the rules to the word list 
    and score the legal words. There are no unique instancecs of this 
    class, so no need for an __init__ method.
    """

    rules = [
        "Words that are not allowed: Pronouns, contractions, hyphenated words",
        "and foreign words that are not in the English dictionary.",
        "",
        "Scoring:",
        "Words less than 3 letters in length are worth 0 points. Words 3 or 4",
        "letters in length are worth 1 point. All words greater than 4 are",
        "worth N+1 - 4 points, where N is the length of the word.",
        "The following table will help illustrate the scoring:",
        " Number of letters | Points ",
        "               < 3 | 0      ",
        "               3-4 | 1      ",
        "                 5 | 2      ",
        "                 6 | 3      ",
        "                 7 | 4      ",
        "",
        "Words are formed from adjoining letters. You may not skip over",
        "letters. Letters must join in the proper sequence to spell a word.",
        "They may join horizontally, vertically or or diagonally",
        "",
        "Example: FANG",
        "",
        "         G D I W",
        "         |      ",
        "         N T E M",
        "          \\    ",
        "         T A-F C",
        "         E R I J",
    ]

    # Boggle uses the same allowed words dictionary as Scrabble. 
    # Therefore, import sowpods as allowed_words
    with open('sowpods.txt', 'r') as sowpods:
        text = sowpods.readlines()
        allowed_words = [line.strip('\n') for line in text]

    def show():
        for line in Rules.rules:
            line.lstrip()
            print(line)

    def apply_rules(word_list, Board):
        """This method applies the rules that are explained in 
        Rules.rules. The first thing it does is check that the 
        words in the list are in sowpods. Words that are not in 
        sowpods are added to the illegal words list and removed from 
        the word_list. Words that are in sowpods are left in word_list

        Once the words are determined to be in the sowpods dictionary, 
        they are checked to make sure all their letters are present in 
        the board. After that, the path of the word is checked to make 
        sure that it follows the allowed path described in the "FANG" 
        example in Rules.rules.
        """

        board = Board.board
        size = Board.size
        ill = list(set(word_list).difference(Rules.allowed_words))
        word_list = list(set(word_list).intersection(Rules.allowed_words))
        # sub_list is the list of allowed positions that next letter 
        # in the word can be, relative the position of the letter you 
        # are currently on.
        sub_list = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                    (0, 1), (1, -1), (1, 0), (1, 1)]
        for word in word_list:
            i = 0
            flag = True
            # check that all letters are present on the board
            if any([letter not in board for letter in word]):
                flag = False
                ill.append(word)
            else:
                # get the indices of all board positions of the first 
                # letter in the word and convert them to (row,col) 
                # subscripts
                inds1 = [j for j, x in enumerate(board) if x == word[i]]
                subs1 = [(ind // size, ind % size) for ind in inds1]
            while flag:
                if i == len(word) - 1:
                    break
                else:
                    # get the indices of all the board positions of 
                    # the second letter in the word and convert to 
                    # (row, col) subscripts
                    inds2 = [j for j, x in enumerate(board)
                             if x == word[i + 1]
                             ]
                    subs2 = [(ind // size, ind % size) for ind in inds2]
                    # find the positions of all instances of the 
                    # second letter, relative to the first letter
                    diffs = [(subs2[j],
                              (subs1[k][0] - subs2[j][0],
                               subs1[k][1] - subs2[j][1]
                               )
                              )
                             for j in range(len(subs2))
                             for k in range(len(subs1))
                             ]
                    subs1 = []
                    # Keep only the instances of the second letter 
                    # that are legal as defined in sub_list. Then use 
                    # only those positions to repeat the process 
                    # looking for the next leter.
                    for diff in diffs:
                        if diff[1] in sub_list:
                            subs1.append(diff[0])
                    if not subs1:
                        ill.append(word)
                        break
                i += 1
        word_list = sorted(set(word_list).difference(ill))
        ill = sorted(ill)      
        return word_list, ill

    def score_words(Player):
        """This method applies the scoring described in Rules.rules to 
        the word_list. The word_list is turned into a word_dict with 
        the word as the key and the score of that word as the value
        """
        w = {}
        for word in Player.word_list:
            if len(word) < 3:
                w[word] = 0
                Player.total_score += 0
            elif len(word) < 5:
                w[word] = 1
                Player.total_score += 1
            elif len(word) >= 5:
                w[word] = (2 + (len(word) - 5))
                Player.total_score += (2 + (len(word) - 5))
        Player.word_list = w


class Player:
    """This class defines a player to play the game. The input is the 
    player's name and the output is a Player object with a word_list, 
    an illegal_word_list and methods to display each list.
    """

    def __init__(self, name):
        self.name = name
        self.total_score = 0
        self.illegal_words = []
        self.word_list = []

    def display_illegal_words(self):
        self.illegal_words = '\n'.join(self.illegal_words)
        print('The following words are not allowed:')
        print(self.illegal_words)
        print('')

    def display_legal_words(self):
        self.legal_words = [[k, str(v)] for k, v in self.word_list.items()]
        self.legal_words = [' '.join(self.legal_words[i]) 
                            for i in range(len(self.legal_words))
                           ]
        self.legal_words = '\n'.join(self.legal_words)
        print('The following words scored points:')
        print(self.legal_words)
        print('')

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Game:
    """
    This class is the driving engine. It runs all pieces of the game 
    and player interactions. Upon launching the .py file from the 
    command line, the Game object will run the start_game() method and 
    the game will begin. When the game is over, the Game will run the 
    end_game() method and the game will end.
    """

    def __init__(self, Board):
        self.Board = Board

    def clear(self):
        """This method clears the terminal window"""
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def add_player(self):
        """This method adds a player to the Game object"""
        player_name = input("Please enter your name: ")
        self.Player = Player(player_name)
        print(
            "Good luck to you,",
            self.Player,
            "on this epic word search journey"
        )

    def start_game(self):
        """This method starts the game. The Player will be asked if 
        they want to see the instructions, rules, and whether or not 
        they are ready to start. After that the game will start.
        """
        self.clear()
        print(
            "Welcome to command-line Boggle! Prepare to play the greatest",
            "computer game ever created by man!"
        )
        self.add_player()
        questions = {
            'Would you like to see the instructions? (y/n): ': Instructions,
            'Would you like to read the rules? (y/n): ': Rules,
            'Ready to play? (y/n): ': ''
        }
        while True:
            for q, r in questions.items():
                resp = input(q)
                if q == list(questions.keys())[-1]:
                    if resp == 'y':
                        break
                    elif resp == 'n':
                        pass
                    else:
                        print('Response not understood')
                        break
                elif resp == 'y':
                    self.clear()
                    r.show()
                elif resp == 'n':
                    pass
                else:
                    print('Response not understood')
                    break
            if q == list(questions.keys())[-1]:
                if resp == 'y':
                    break
                else:
                    pass

    def play_game(self):
        """This method drives the gameplay. The start_game method is 
        called to start the game. The Board is the shuffled and the 
        game begins. The Player then has 2 min to enter words and 
        those words will be added to the Player's word list which will 
        have rules applied to it in the apply_rules method.
        """
        self.clear()
        # self.start_game()
        self.Board.shuffle_board()
        self.clear()
        print(self.Board)
        start_time = time.time()
        while time.time() - start_time < 120:
            word = input('Enter a word: ')
            self.Player.word_list.append(word.upper())
            self.clear()
            print(self.Board)
        self.end_game()

    def end_game(self):
        """This method ends the game and displays the Player's legal 
        words and illegal words. Then shows the Player's score and 
        asks if they want to play again. If they do not, method ends.
        """
        w, ill = Rules.apply_rules(self.Player.word_list, self.Board)
        self.Player.word_list = w
        self.Player.illegal_words = ill
        Rules.score_words(self.Player)
        self.Player.display_illegal_words()
        self.Player.display_legal_words()
        print(self.Player, "you played a great game!")
        print("Your total score is: ", self.Player.total_score)
        response = input("Would you like to play again? (y/n): ")
        if response == 'y':
            self.play_game()
        else:
            print("Thanks for playing command-line Boggle")


if __name__ == '__main__':
    boggle = Game(Board(4))
    boggle.start_game()
    boggle.play_game()
