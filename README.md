# Boggle
a command line version of the game boggle

# Operation:

The player will run the game from the command line. Once the program is 
executed, the user will enter into the game and enter their player name and 
read the instructions and the rules. After they have read the rules, the game 
will start. The player will be shown the board at this point which is a 4x4 
grid of letters. The object of the game is to find as many words as you can in 
the grid (word search). The player will have two minutes to enter as many 
words as they can and when the two minutes are up, they will be presented with 
their score, as well as a list of words that were illegal, and a list of words 
that were legal, and thus scored points. The player will then be asked if they 
want to play again and if they do, then they will be shown a new board to play 
on. If not, the program will end.

# Class structure:

- The first class is the Board class. The Board sets the layout of the letters 
that the user will use to find words. The traditional game is tray with cube 
shaped cutouts that hold six-sided dice with different letters on each of 
them. Then you just shake the board and the dice fall into the tray with a 
particular letter on the up side. I tried to replicate this behavior by 
hardcoding the letterBlocks as six-character strings and then randomly 
selecting a particular side to display. Then I shuffle all the sides so that 
each block lands in a different position on the board with a different side 
up. 

- The next two classes are the Instructions and Rules classes. The 
Instructions class simply displays the intructions with a show() method. That 
is its only method. The Rules class also displays the rules with a show() 
method, but additionally applies those rules to the word list that the player 
creates while playing. Boggle uses the same allowed words dictionary as 
Scrabble, so I have recycled the sowpods.txt file for use in determining 
whether or not a word is allowed. Additionally, all letters of the word have 
to be connected either vertically, horizontally or diagonally within the 
board, this class also applies that rule to the word list that the player 
creates. This class also scores the words left in the word_list after the 
rules have been applied and illegal words have been filtered out.

- The next class is the Player class. This class defines the Player that is 
playing the game and stores the words that this player has found, the words 
that were illegal from that Player's list (after the rules have been applied) 
and the score of . It also has methods to display both I wrote it this way so 
that future iterations could in theory add multiple players who would take 
turns on the same board and then could compare scores against each other (
trying to simulate real game play on an actual board).

- The final class is the Game class. This is the engine of the program. All 
other classes interact directly with this class or directly with other classes 
that interact directly with this class. There is a start_game() method which 
instantiates a Player and displays Rules and Instructions. There is a 
play_game() method which instantiates the Board and runs the actual game play. 
There is an end_game() method which applies the rules to the Player's word 
list and then scores the word list, and then ends the game and exits the 
program.

# Testing this project:

You should test this project by playing it from the command line! However, I 
also included a cleaned up version of my testing notebook titled 
boggle_TestLab that I was using during debugging. You can run through this and 
modify it as you see fit. I think it should test all aspects that need to be 
tested. I think running it this way, there are parts that could break 
independently, but run as intended as a whole program from the command line, 
it should not break.