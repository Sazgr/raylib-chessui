from board import Board
from consts import screen_width, screen_height
import engine_util
from color_profile import *
from pyray import *
from threading import Thread
import time
from window import *

class UI:
    def __init__(self):
        self.board = Board()
        self.window_manager = WindowManager(self.board)
        self.window_manager.apply_layout(layout_2)
        #self.window_manager.add_window("board", 40, 40, None, None, 40, False)
        #self.window_manager.add_window("game_history", 1480, 40, 400, 800, 40, True)
        #self.window_manager.add_window("players", 480, 40, None, None, 40, False)
        #self.window_manager.add_window("search_data", 480, 200, 960, None, 40, False)
        #self.window_manager.add_window("theme_library", 40, 480, None, 360, 40, True)
    
    def initialize(self):
        set_target_fps(60)
        set_config_flags(ConfigFlags.FLAG_WINDOW_UNDECORATED | ConfigFlags.FLAG_MSAA_4X_HINT)
        init_window(screen_width, screen_height, 'raylib-chessui')
        
        if self.board.color_profile.background_image != None:
            background_image = load_image(self.board.color_profile.background_image)
            scale_factor = screen_height / background_image.height
            image_resize(background_image, int(scale_factor * background_image.width), screen_height)
            self.board.background_texture = load_texture_from_image(background_image)
            unload_image(background_image)
        
        piece_image = load_image("assets/pieces.png")
        self.board.piece_texture = load_texture_from_image(piece_image)
        unload_image(piece_image)
        
        init_audio_device()
        
        if is_window_ready():
            return True
    
    def main_loop(self):
        while not window_should_close():
            self.interact()
            self.draw()
            self.process_game_state()
    
    def interact(self):
        for window in self.window_manager.windows:
            window.interact()
    
    def draw(self):
        begin_drawing()
        
        clear_background(self.board.color_profile.background)
        if self.board.color_profile.background_image != None:
            draw_texture(self.board.background_texture, screen_width - self.board.background_texture.width, 0, WHITE)
        if self.board.color_profile.background_text != None:
            font = int(10 * screen_height / 128)
            draw_text(self.board.color_profile.background_text, font, screen_height - 2 * font, font, BLACK)
        
        for window in self.window_manager.windows:
            window.draw()
        
        if (self.board.game_end):
            text_length = measure_text("GAME END", 40)
            draw_rectangle(int(screen_width / 4), int(3 * screen_height / 8), screen_width // 2, screen_height // 4, self.board.color_profile.neutral)
            draw_rectangle(int(screen_width / 4) + 4, int(3 * screen_height / 8) + 4, screen_width // 2 - 8, screen_height // 4 - 8, self.board.color_profile.fill)
            draw_text("GAME END", int(screen_width / 2 - text_length / 2), int(screen_height / 2 - 20), 40, self.board.color_profile.neutral)
        draw_fps(0, 0)
        
        end_drawing()
    
    def process_game_state(self):
        with self.board.lock:
            if len(engine_util.get_movelist(self.board.engine.process)) == 0:
                self.board.game_end = True
        if (not self.board.game_end) and self.board.searching == False:
            if len(self.board.move_list) % 2 == 0 and not self.board.white_player: #white to move
                self.board.searching = True
                self.board.searching_thread = Thread(target=self.board.engine_move, args=(), daemon=True)
                self.board.searching_thread.start()
            
            if len(self.board.move_list) % 2 == 1 and not self.board.black_player: #black to move
                self.board.searching = True
                self.board.searching_thread = Thread(target=self.board.engine_move, args=(), daemon=True)
                self.board.searching_thread.start()
    
    def shutdown(self):
        close_window()
        while self.board.searching_thread != None:
            time.sleep(0.5)


if __name__ == '__main__':
    ui = UI()

    if (ui.initialize()):
        ui.main_loop()
    ui.shutdown()
