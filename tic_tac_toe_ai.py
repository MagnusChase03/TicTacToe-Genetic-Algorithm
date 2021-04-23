# 9 inputs
# 3 hidden
# 1 output

import math
import random


class NeuralNetwork:
    def __init__(self, randomize=False, bot_number=None):
        self.inputs = []
        self.weights = []
        self.hidden_layer = []
        self.weights2 = []
        self.output = 0
        self.fitness = 0

        self.randomize_weights()
        if not randomize:
            f = open("bot%s.dat" % bot_number, "r")
            data = f.read()
            data = data.split("\n")
            for i in range(0, 9):
                for k in range(0, 3):
                    self.weights[i][k] = float(data[(3 * i)+k])

            for i in range(0, 3):
                self.weights2[i] = float(data[27 + i])


    def randomize_weights(self):
        for i in range(0, 9):

            self.weights.append([])
            for k in range(0, 3):
                self.weights[i].append(random.random() * 10 - 5)

        for i in range(0, 3):
            self.weights2.append(random.random() * 10 - 5)

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def guess(self):
        for i in range(0, 3):

            total = 0
            for k in range(0, 9):
                total = total + (self.inputs[k] * self.weights[k][i])

            total = self.sigmoid(total)
            self.hidden_layer.append(total)

        total = 0
        for i in range(0, 3):
            total = total + (self.hidden_layer[i] * self.weights2[i])

        self.output = int(total)


def create_bots():

    best_bots = []
    game_bots = []
    for t in range(0, 5):
        best_bots.append(NeuralNetwork(False, t))
        game_bots.append(NeuralNetwork(False, t))

    for t in range(0, 15):
        game_bots.append(create_child(best_bots))

    return game_bots

def check_rows(board):
    for row in range(0, 3):
        if (not board[3 * row] == 0) and board[3 * row] == board[(3 * row) + 1] and board[3 * row] == board[(3 * row) + 2]:
            return True

    return False


def check_cols(board):
    for col in range(0, 3):
        if (not board[col] == 0) and board[col] == board[col + 3] and board[col] == board[col + 6]:
            return True

    return False


def check_diag(board):
    if (not board[0] == 0) and board[0] == board[4] and board[0] == board[8]:
        return True

    elif (not board[2] == 0) and board[2] == board[4] and board[2] == board[6]:
        return True

    return False


def check_bot_rows(board):
    for row in range(0, 3):
        if (board[3 * row] == 2) and board[3 * row] == board[(3 * row) + 1] and board[3 * row] == board[(3 * row) + 2]:
            return True

    return False


def check_bot_cols(board):
    for col in range(0, 3):
        if (board[col] == 2) and board[col] == board[col + 3] and board[col] == board[col + 6]:
            return True

    return False


def check_bot_diag(board):
    if (board[0] == 2) and board[0] == board[4] and board[0] == board[8]:
        return True

    elif (board[2] == 2) and board[2] == board[4] and board[2] == board[6]:
        return True

    return False


def filled(board):
    for i in board:
        if i == 0:
            return False
    return True


def win(board):
    return check_rows(board) or check_cols(board) or check_diag(board)


def get_fitness(board):
    score = 0
    if check_bot_diag(board) or check_bot_rows(board) or check_bot_cols(board):
        counter = 0
        for num in game_board:
            if num == 2:
                counter = counter + 1

        score = 50 - counter

    else:
        counter = 0
        for num in game_board:
            if num == 2:
                counter = counter + 1

        score = counter

    return score


def save_top_5(bots):
    for i in range(0, 5):
        best_fitness = 0
        best_bot = NeuralNetwork(True)
        for bot in bots:
            if bot.fitness >= best_fitness:
                best_fitness = bot.fitness
                best_bot = bot

        f = open("bot%s.dat" % i, "w")
        for row in best_bot.weights:
            for num in row:
                f.write("%s\n" % str(num))
                f.flush()

        for num in best_bot.weights2:
            f.write("%s\n" % str(num))
            f.flush()

        bots.remove(best_bot)


def create_child(bots):
    bot1 = random.choice(bots)
    bot2 = random.choice(bots)
    child = NeuralNetwork(True)

    for i in range(0, 9):
        for k in range(0, 3):
            dominant = random.randint(1, 2)
            if dominant == 1:
                child.weights[i][k] = bot1.weights[i][k]

            else:
                child.weights[i][k] = bot2.weights[i][k]

            if random.random() < 0.1:
                child.weights[i][k] = random.random() * 10 - 5


    for i in range(0, 3):
        dominant = random.randint(1, 2)
        if dominant == 1:
            child.weights2[i] = bot1.weights2[i]

        else:
            child.weights2[i] = bot2.weights2[i]

        if random.random() < 0.1:
            child.weights2[i] = random.random() * 10 - 5

    return child


game_bots = create_bots()

for x in range(0, 2):
    for i in range(0, 20):
        game_board = [0, 0, 0,
                      0, 0, 0,
                      0, 0, 0]
        bot = game_bots[i]
        playerTurn = True

        while not win(game_board) or not filled(game_board):
            print(game_board[0:3])
            print(game_board[3:6])
            print(game_board[6:9])
            print("")
            if playerTurn:
                placement = input("Where do you want to go (1-9)? ")
                game_board[int(placement) - 1] = 1
                playerTurn = False

            else:
                bot.inputs = game_board
                bot.guess()
                if bot.output >= 0 and bot.output <= 8 and game_board[bot.output] == 0:
                    game_board[bot.output] = 2
                    playerTurn = True

                else:
                    break

        bot.fitness = get_fitness(game_board)

        print(game_board[0:3])
        print(game_board[3:6])
        print(game_board[6:9])
        print("--------------------------")

    save_top_5(game_bots)
    game_bots = create_bots()

