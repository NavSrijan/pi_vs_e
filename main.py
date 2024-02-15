import chess
import time
from fentoimage.board import BoardImage
from create_win_img import write_over_image
import numpy as np
import pickle

board = chess.Board()
pi_digits = np.load('pi.npy')
e_digits = np.load('e.npy')
path_to_save = "images/{}img.png"

class Game():

    def __init__(self, elo, pi_digits, e_digits, current_index_pi=0, current_index_e=0):
        self.elo = elo
        self.current_index_pi = current_index_pi
        self.current_index_e = current_index_e
        self.moves = []
        self.fens = []

        self.board = chess.Board()

        self.load_progress()
        self.pi_digits = pi_digits
        self.e_digits = e_digits

    def reset_game(self, elo):
        self.elo = elo
        #self.current_index_pi = current_index_pi
        self.save_progress()
        self.moves = []
        self.fens = []

        self.board = chess.Board()

    def get_next_digit_pi(self):
        to_return = self.pi_digits[self.current_index_pi] 
        self.current_index_pi+=1
        #print(self.current_index_pi)
        return to_return

    def get_9_digits_pi(self):
        # Returns 9 digits from pi
        to_return = ""
        ind = -4
        for i in range(9):
            to_return+=str(self.pi_digits[self.current_index_pi+ind+i])
        return to_return

    def get_9_digits_e(self):
        # Returns 9 digits from e
        to_return = ""
        ind = -4
        for i in range(9):
            to_return+=str(self.e_digits[self.current_index_e+ind+i])
        return to_return

    def get_next_digit_e(self):
        to_return = self.e_digits[self.current_index_e]
        self.current_index_e+=1
        #print(self.current_index_e)
        return to_return

    def get_multiple_sliced_list(self, digit, ll):
        # Returns only the items present at the multiple of digit
        multiples = []
        for i in range(0, len(ll), digit):
            multiples.append(ll[i])
        return multiples

    def choose_move_pi(self):
        # Choose one move from the set of legal moves
        digit = self.get_next_digit_pi()
        legal_moves = list(self.board.legal_moves)

        n = len(legal_moves)

        def select_when_digit_less_than_n(digit, n, legal_moves):
            pick = digit%n
            if pick==0:
                return legal_moves[-1]
            return legal_moves[pick-1]

        # If digit-1 == len(legal_moves): return legal_moves[digit]
        #print(f"Digit: {digit} n: {n}")
        if (digit+1)==n:
            return legal_moves[digit]
        elif digit>=n:
            multiples = self.get_multiple_sliced_list(digit, legal_moves)
            digit = self.get_next_digit_pi()
            while len(multiples)>=digit:
                if digit==0:
                    return legal_moves[0]
                multiples = self.get_multiple_sliced_list(digit, legal_moves)
                digit = self.get_next_digit_pi()
            return select_when_digit_less_than_n(digit, n, legal_moves)
        elif digit<n:
            return select_when_digit_less_than_n(digit, n, legal_moves)

    def choose_move_e(self):
        # Choose one move from the set of legal moves
        digit = self.get_next_digit_e()
        legal_moves = list(self.board.legal_moves)

        n = len(legal_moves)

        def select_when_digit_less_than_n(digit, n, legal_moves):
            pick = digit%n
            if pick==0:
                return legal_moves[-1]
            return legal_moves[pick-1]

        # If digit-1 == len(legal_moves): return legal_moves[digit]
        #print(f"Digit: {digit} n: {n}")
        if (digit+1)==n:
            return legal_moves[digit]
        elif digit>=n:
            multiples = self.get_multiple_sliced_list(digit, legal_moves)
            digit = self.get_next_digit_e()
            while len(multiples)>=digit:
                if digit==0:
                    return legal_moves[0]
                multiples = self.get_multiple_sliced_list(digit, legal_moves)
                digit = self.get_next_digit_e()
            return select_when_digit_less_than_n(digit, n, legal_moves)
        elif digit<n:
            return select_when_digit_less_than_n(digit, n, legal_moves)

    def check_end(self, who):
        if self.board.is_stalemate():
            self.draw_score+=1
            write_over_image("Stalemate", 160, path_to_save)
            return True, "Stalemate"
        elif self.board.is_checkmate():
            if who=="e":
                self.e_score+=1
                write_over_image("e Won!", 160, path_to_save)
            else:
                self.pi_score+=1
                write_over_image("Pi Won!", 160, path_to_save)
            return True, f"Checkmate {who}"
        elif self.board.can_claim_threefold_repetition():
            self.draw_score+=1
            write_over_image("            Draw  \nThree Fold repitition", 100, path_to_save)
            return True, "draw"
        elif self.board.can_claim_fifty_moves():
            self.draw_score+=1
            write_over_image("        Draw  \nFifty Move rule", 100, path_to_save)
            return True, "draw"
        return False, ""

    def move_pi(self):
        # pi's move
        try:
            move = str(self.choose_move_pi())
        except Exception as e:
            pass
        self.board.push_san(move)
        self.moves.append(move)
        self.fens.append(self.board.fen())
        #print(str(move))

    def move_e(self):
        # e's move
        try:
            move = str(self.choose_move_e())
        except Exception as e:
            pass
        self.board.push_san(move)
        self.moves.append(move)
        self.fens.append(self.board.fen())
        #print(str(move))

    def save_progress(self):
        data = {
            "current_pi_index": self.current_index_pi,
            "current_e_index": self.current_index_e,
            "pi_score": self.pi_score,
            "e_score": self.e_score,
            "draw_score": self.draw_score
        }
        with open("progress.pickle", "wb") as f:
            pickle.dump(data, f)

    def load_progress(self):
        try:
            with open("progress.pickle", "rb") as f:
                data = pickle.load(f)
                self.current_index_pi = data["current_pi_index"]
                self.current_index_e = data["current_e_index"]
                self.pi_score = data["pi_score"]
                self.e_score = data["e_score"]
                self.draw_score = data["draw_score"]
        except FileNotFoundError:
            self.current_pi_index_pi = 0
            self.current_index_e = 0
            self.pi_score = 0
            self.e_score = 0
            self.draw_score = 0

    def save_image(self):
        path_to_save = "images/img.png"
        renderer = BoardImage(self.board.fen())
        image = renderer.render()
        image.save(path_to_save)

    def format_moves(self, moves, n):
        # n is the number of pairs to show
        formatted_moves = []
        required_pairs = n
        x = len(moves)
        if x<n*2:
            if x%2==0:
                n = x
                last_moves = moves[-n*2:]
            else:
                n = int((x+1)/2)
                last_moves = moves[(-n*2)-1:]
                last_moves.append("-")
        else:
            if x%2==0:
                last_moves = moves[-n*2:]
            else:
                n-=1
                last_moves = moves[(-n*2)-1:]
                last_moves.append(" -  ")

        # Create a formatted string with elements in last_moves in pairs
        if required_pairs>=int((len(moves)+1)/2):
            base_n=1
        else:
            base_n = int((len(moves)+1)/2)-required_pairs+1

        i=0
        j=0
        while i<len(last_moves)-1:
            formatted_moves.append(f"{base_n+j}. {last_moves[i]} {last_moves[i+1]}")
            i+=2
            j+=1
        return "\n".join(formatted_moves)

    def run_game(self, delay=0):
        while True:
                #print(len(self.moves))
            self.move_pi()
            last_10_moves = self.format_moves(self.moves, 10)
            self.save_image()
            is_end, what = self.check_end("pi")
            time.sleep(delay)
            if is_end:
                #print(what)
                break

            self.move_e()
            last_10_moves = self.format_moves(self.moves, 10)
            self.save_image()
            is_end, what = self.check_end("e")
            time.sleep(delay)
            if is_end:
                #print(what)
                break
        return what

if __name__=="__main__":
    game = Game(100, pi_digits, e_digits)
    e = game.e_score
    pi = game.pi_score
    draw = game.draw_score
    score = f"e: {game.e_score}\npi: {game.pi_score}\ndraw: {game.draw_score}"
    print(score)
    while True:
        winner = game.run_game()
        time.sleep(3)
        if winner=="Checkmate e":
            #game.e_score+=1
            pass
        elif winner=="Checkmate pi":
            #game.pi_score+=1
            pass
        elif winner=="draw":
            #game.draw_score+=1
            pass
        #print(game.moves)
        game.reset_game(100)
        score = f"e: {game.e_score}\npi: {game.pi_score}\ndraw: {game.draw_score}\ntotal: {game.e_score+game.pi_score+game.draw_score}"
        print(score)
        print('')

    print("")


