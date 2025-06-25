from color_profile import *
from consts import *
from engine import Engine
import engine_util
from pyray import *
import subprocess
from threading import RLock

class Board:
    def __init__(self):
        self.lock = RLock()
        self.selected = None
        self.color_profile = val_sage_theme
        self.searching = False
        self.move_list = []
        self.white_player = True
        self.black_player = False
        self.game_end = False
        self.engine = Engine()
        self.search_engine_1 = Engine()
        self.search_engine_2 = Engine()
        self.search_engine = None
        self.board = engine_util.get_board_moves(self.engine.process, self.move_list)
        self.valid_moves = engine_util.get_movelist(self.engine.process)
        self.background_texture = None
        self.searching_thread = None
    
    def reset(self):
        self.selected = None
        self.searching = False
        self.move_list = []
        self.game_end = False
        self.engine = Engine()
        self.search_engine_1 = Engine()
        self.search_engine_2 = Engine()
        self.search_engine = None
        self.board = engine_util.get_board_moves(self.engine.process, self.move_list)
        self.valid_moves = engine_util.get_movelist(self.engine.process)
    
    def engine_move(self, debug=False):
        if debug:
            print("daemon started")
        
        move_time = 100
        if len(self.move_list) % 2 == 0:
            self.search_engine = self.search_engine_1
        else:
            self.search_engine = self.search_engine_2
        
        with self.lock:
            engine_util.make_moves(self.search_engine.process, self.move_list)
        
        best_move = self.search_engine.search(move_time)
        
        if debug:
            print("daemon:", best_move)
        
        with self.lock:
            self.make_move(best_move)
            self.searching = False
            self.searching_thread = None
        
        if debug:
            print("daemon finished")
        
    
    def make_move(self, move):
        with self.lock:
            self.move_list.append(move)
            self.board = engine_util.get_board_moves(self.engine.process, self.move_list)
            self.valid_moves = engine_util.get_movelist(self.engine.process)

