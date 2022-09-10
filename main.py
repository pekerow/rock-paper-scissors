import random

valid_moves = ['rock', 'paper', 'scissor']


class Player:
    # parent player class: always plays rock

    def __init__(self):
        self.score = 0

    def play(self):
        # Return the player move in a string (always rock)
        return valid_moves[0]

    def learn(self, last_opponent_move):
        # Save the move made by the opponent on the last round.
        # Not used by parent class
        pass


class RandomPlayer(Player):
    # Chooses its move at random
    def play(self):
        # Return the player move in a string (random)
        index = random.randint(0, 2)
        return valid_moves[index]


class ReflectPlayer(Player):
    # Remembers what move the opponent played last round & plays that move this round
    def __init__(self):
        Player.__init__(self)
        self.last_opponent_move = None

    def play(self):
        # Return the player move in a string (last opponent move)
        if self.last_opponent_move is None:
            return Player.play(self)
        return self.last_opponent_move

    def learn(self, last_opponent_move):
        # Save the move made by the opponent on the last round.
        self.last_opponent_move = last_opponent_move


class CyclePlayer(Player):
    # Remembers what move it played last round & cycles through the different moves
    def __init__(self):
        Player.__init__(self)
        self.last_move = None

    def play(self):
        # Return the player move in a string (cycle)
        # move = None
        if self.last_move is None:
            move = Player.play(self)
        else:
            index = valid_moves.index(self.last_move) + 1
            if index >= len(valid_moves):
                index = 0
            move = valid_moves[index]
        self.last_move = move
        return move


class HumanPlayer(Player):
    # Ask the user to play their move
    def play(self):
        player_move = input('Enter your move (' +
                            ', '.join(valid_moves) + '):\n')
        while player_move not in valid_moves:
            player_move = input('Invalid move, try again\n')
        return player_move


class Game:
    # Play a match or a single round of Rock Paper Scissor

    def __init__(self):
        self.player1 = HumanPlayer()
        self.player2 = CyclePlayer()

    def play_match(self):
        # Start match, display welcome message at the start and final score at the end
        print("Let\'s play Rock, Paper or Scissors!\n\n")
        try:
            while True:
                self.play_round()
                print('The score is: ' + str(self.player1.score) + ' x ' +
                      str(self.player2.score) + '\n')
                input('Press enter to play again or ctrl+c to quit\n')
        except KeyboardInterrupt:
            print('\n\nThanks for playing!')
            if self.player1.score > self.player2.score:
                print('Player 1 won!')
            elif self.player1.score > self.player2.score:
                print('Player 2 won!')
            else:
                print('The game was a draw!')
            print('The final score was ' + str(self.player1.score) + ' x ' +
                  str(self.player2.score))

    def play_round(self):
        # Play a round & display result at the end
        player1_move = self.player1.play()
        player2_move = self.player2.play()
        result = Game.check_result(player1_move, player2_move)

        self.player1.learn(player2_move)
        self.player2.learn(player1_move)

        print('Player 1 plays "' + player1_move + '" and player 2 plays "' +
              player2_move + '"')
        if result == 1:
            self.player1.score += 1
            print('=> Player 1 won!\n')
        elif result == 2:
            self.player2.score += 1
            print('=> Player 2 won!\n')
        else:
            print('=> Draw!\n')

    @classmethod
    def check_result(cls, move1, move2):
        """Check the result of a round.

        Args:
            move1 (string): Player 1 move.
            move2 (string): Player 2 move.

        Returns:
            1 if player 1 won, 2 if player 2 won or 0 on a draw.
        """
        if Game.is_move_stronger(move1, move2):
            return 1
        elif Game.is_move_stronger(move2, move1):
            return 2
        else:
            return 0

    @classmethod
    def is_move_stronger(cls, move1, move2):
        """Check if the first move is stronger than the second.

        Args:
            move1 (string): Player 1 move.
            move2 (string): Player 2 move.

        Returns:
            True if move1 is stronger, False otherwise.
        """
        if move1 == 'rock' and move2 == 'scissor':
            return True
        elif move1 == 'scissor' and move2 == 'paper':
            return True
        elif move1 == 'paper' and move2 == 'rock':
            return True
        return False


# Control: create new Game instance and start a match.
game = Game()
game.play_match()
