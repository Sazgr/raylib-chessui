from color_profile import *
from consts import screen_width, screen_height
import engine_util
from pyray import *

class ScrollBar:
    def __init__(self, board, x, y, height, font, shown, total):
        self.board = board
        self.x = x
        self.y = y
        self.height = height
        self.font = font
        self.shown = shown
        self.total = total
        self.update(shown, total)
        self.scroll_y = 0
        self.dragging = False
    
    def update(self, shown, total):
        changed = False
        if shown != None and shown != self.shown:
            self.shown = shown
            changed = True
        if total != None and total != self.total:
            self.total = total
            changed = True
        self.scroll_area_size = self.height - self.font
        self.scroll_bar_size = int(self.scroll_area_size * self.shown / self.total)
        if changed:
            self.scroll_y = self.scroll_area_size - self.scroll_bar_size
        
    def visible(self):
        return self.shown < self.total
    
    def draw(self, color_profile):
        if not self.visible():
            return
            
        pixel_size = self.font // 10
        draw_rectangle(self.x, self.y + int(self.font * 0.4), 6 * pixel_size, int(self.scroll_area_size + self.font * 0.2), color_profile.neutral)
        draw_rectangle(self.x + int(self.font * 0.1), self.y + int(self.font * 0.5), 4 * pixel_size, int(self.scroll_area_size), color_profile.fill)
        
        draw_rectangle(self.x + int(self.font * 0.1), self.y + int(self.font * 0.5 + self.scroll_y), 4 * pixel_size, int(self.scroll_bar_size), color_profile.neutral)
    
    def interact(self):
        if not self.visible():
            return
        
        mouse_pos = get_mouse_position()
        mouse_x = mouse_pos.x
        mouse_y = mouse_pos.y
        
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and self.x + int(self.font * 0.1) <= mouse_x and mouse_x < self.x + int(self.font * 0.5) and self.y + int(self.font * 0.5) + self.scroll_y <= mouse_y and mouse_y < self.y + int(self.font * 0.5) + self.scroll_y + int(self.scroll_bar_size):
            self.dragging = True
        
        if is_mouse_button_released(MOUSE_BUTTON_LEFT):
            self.dragging = False
        
        if self.dragging:
            mouse_delta = get_mouse_delta()
            mouse_delta_y = mouse_delta.y
            
            self.scroll_y += mouse_delta_y
            self.scroll_y = min(max(0, self.scroll_y), self.scroll_area_size - self.scroll_bar_size)
    
    def get_index(self):
        if not self.visible():
            return 0
        
        return min(self.total - self.shown, int(self.scroll_y / ((self.scroll_area_size - self.scroll_bar_size) / (self.total - self.shown + 1))))

class Window:
    def __init__(self, board, window_type, x, y, width, height, font, scrollable):
        self.board = board
        self.window_type = window_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.scrollable = scrollable
        self.scroll_bar = None
        if self.scrollable:
            if self.window_type == "game_history":
                self.scroll_bar = ScrollBar(self.board, x + width - font, y, height, font, height // font - 1, max(1, (len(self.board.move_list) + 1) // 2))
            if self.window_type == "theme_library":
                self.scroll_bar = ScrollBar(self.board, x + width - font, y + font, height - font, font, height // font - 2, len(theme_library))
    
    def draw(self):
        if self.window_type == "board":
            assert not self.scrollable
            self.draw_board(self.x, self.y, self.width, self.height, self.font)
        elif self.window_type == "game_history":
            assert self.scrollable
            self.draw_game_history(self.x, self.y, self.width, self.height, self.font)
        elif self.window_type == "players":
            assert not self.scrollable
            self.draw_players(self.x, self.y, self.width, self.height, self.font)
        elif self.window_type == "player_black":
            assert not self.scrollable
            self.draw_player_black(self.x, self.y, self.width, self.height, self.font)
        elif self.window_type == "player_white":
            assert not self.scrollable
            self.draw_player_white(self.x, self.y, self.width, self.height, self.font)
        elif self.window_type == "search_data":
            assert not self.scrollable
            self.draw_search_data(self.x, self.y, self.width, self.height, self.font)
        elif self.window_type == "theme_library":
            assert self.scrollable
            self.draw_theme_library(self.x, self.y, self.width, self.height, self.font)
        else:
            assert False, "Unsupported window type"
    
    def interact(self):
        if self.window_type == "board":
            assert not self.scrollable
            self.interact_board(self.x, self.y, self.width, self.height, self.font)
        elif self.window_type == "game_history":
            assert self.scrollable
            self.interact_game_history(self.x, self.y, self.width, self.height, self.font)
        elif self.window_type == "players":
            assert not self.scrollable
            self.interact_players(self.x, self.y, self.width, self.height, self.font)
        elif self.window_type == "player_black":
            assert not self.scrollable
            self.interact_player_black(self.x, self.y, self.width, self.height, self.font)
        elif self.window_type == "player_white":
            assert not self.scrollable
            self.interact_player_white(self.x, self.y, self.width, self.height, self.font)
        elif self.window_type == "search_data":
            pass
        elif self.window_type == "theme_library":
            assert self.scrollable
            self.interact_theme_library(self.x, self.y, self.width, self.height, self.font)
        else:
            assert False, "Unsupported window type"
    
    def _draw_piece(self, piece_type, x, y, size, piece_color):
        piece_indexes = {"r" : 0, "n" : 1, "b" : 2, "q" : 3, "k" : 4, "p" : 5}
        offset = piece_indexes[piece_type.lower()] * 10
        s_rec = Rectangle(offset, 0, 10, 10)
        d_rec = Rectangle(x, y, size, size)
        draw_texture_pro(self.board.piece_texture, s_rec, d_rec, (0, 0), 0, piece_color)
    
    def draw_board(self, x, y, width, height, font, color_profile=None):
        if width == None:
            width = font * 10
        if height == None:
            height = font * 10
        
        if color_profile == None:
            color_profile = self.board.color_profile
        
        pixel_size = font // 10
        
        draw_rectangle(x, y, width, height, color_profile.neutral)
        draw_rectangle(x + pixel_size, y + pixel_size, width - 2 * pixel_size, height - 2 * pixel_size, color_profile.fill)
        
        base_size = 8 * font
        board_size = ((min(width, height) - 2 * font) // base_size) * base_size
        size = board_size + (2 * font)
        square_size = board_size // 8
        
        x += (width - size) // 2
        y += (height - size) // 2
        
        for i in range(8):
            draw_text(str(8 - i), x + int(font * 0.7), y + int(square_size * i + font * 0.5 + (square_size - font) / 2), font, color_profile.neutral)
        for j in range(8):
            if board_size == base_size:
                draw_text(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'][j], x + int(square_size * j + font * 1.7), y + int(square_size * 8 + font * 0.5), font, color_profile.neutral)
            else:
                draw_text(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'][j], x + int(square_size * j + font * 1.5 + (square_size - font) / 2), y + int(square_size * 8 + font * 0.5), font, color_profile.neutral)
        
        x += int(font * 1.5)
        y += int(font * 0.4)
        
        with self.board.lock:
            if len(self.board.move_list) >= 2:
                highlight_color = color_profile.black_hl_2 if len(self.board.move_list) % 2 else color_profile.white_hl_2
                i, j = engine_util.square_to_coord(self.board.move_list[-2][0:2])
                draw_rectangle(x + int(square_size * i), y + int(square_size * j), square_size, square_size, highlight_color)
                highlight_color = color_profile.black_hl if len(self.board.move_list) % 2 else color_profile.white_hl
                i, j = engine_util.square_to_coord(self.board.move_list[-2][2:4])
                draw_rectangle(x + int(square_size * i), y + int(square_size * j), square_size, square_size, highlight_color)
            if len(self.board.move_list) >= 1:
                highlight_color = color_profile.white_hl_2 if len(self.board.move_list) % 2 else color_profile.black_hl_2
                i, j = engine_util.square_to_coord(self.board.move_list[-1][0:2])
                draw_rectangle(x + int(square_size * i), y + int(square_size * j), square_size, square_size, highlight_color)
                highlight_color = color_profile.white_hl if len(self.board.move_list) % 2 else color_profile.black_hl
                i, j = engine_util.square_to_coord(self.board.move_list[-1][2:4])
                draw_rectangle(x + int(square_size * i), y + int(square_size * j), square_size, square_size, highlight_color)
            
            self.board.board = engine_util.get_board_moves(self.board.engine.process, self.board.move_list)
        
        if self.board.selected != None:
            i, j = self.board.selected
            draw_rectangle(x + int(square_size * i), y + int(square_size * j), square_size, square_size, color_profile.neutral_hl)
            for move in self.board.valid_moves:
                if move[:2] == engine_util.coord_to_square(i, j):
                    k, l = engine_util.square_to_coord(move[2:4])
                    draw_rectangle(x + int(square_size * k), y + int(square_size * l), square_size, square_size, color_profile.neutral_hl_2)
        
        x += int(square_size * 0.2)
        y += int(square_size * 0.1)
        
        for i in range(8):
            for j in range(8):
                if (self.board.board[i][j] == '.'):
                    draw_text(self.board.board[i][j], x + int(square_size * j), y + square_size * i, square_size, color_profile.neutral)
                elif (self.board.board[i][j].islower()):
                    self._draw_piece(self.board.board[i][j], x + int(square_size * j), y + square_size * i, square_size, color_profile.color_black)
                else:
                    self._draw_piece(self.board.board[i][j], x + int(square_size * j), y + square_size * i, square_size, color_profile.color_white)
    
    def draw_game_history(self, x, y, width, height, font, color_profile=None):
        if color_profile == None:
            color_profile = self.board.color_profile
        
        self.scroll_bar.update(None, max(1, (len(self.board.move_list) + 1) // 2))
        
        pixel_size = font // 10
        font = pixel_size * 10
        scroll_index = self.scroll_bar.get_index()
        
        draw_rectangle(x, y, width, height, color_profile.neutral)
        draw_rectangle(x + pixel_size, y + pixel_size, width - 2 * pixel_size, height - 2 * pixel_size, color_profile.fill)
        
        for i in range(min(len(self.board.move_list), 2 * self.scroll_bar.shown)):
            if i % 2 == 0:
                draw_text(str(scroll_index + 1 + i // 2) + ".", x + int(font * 0.5), y + int(font * ((i // 2) + 0.5)), font, color_profile.neutral)
                #if scroll_index * 2 + i < len(self.board.move_list):
                draw_text(self.board.move_list[scroll_index * 2 + i], x + int(font * 2.5), y + int(font * ((i // 2) + 0.5)), font, color_profile.color_white)
            else:
                if scroll_index * 2 + i < len(self.board.move_list):
                    draw_text(self.board.move_list[scroll_index * 2 + i], x + int(font * 6), y + int(font * ((i // 2) + 0.5)), font, color_profile.color_black)
        
        self.scroll_bar.draw(color_profile)
    
    def draw_players(self, x, y, width, height, font, color_profile=None):
        assert width == None
        assert height == None
        
        if color_profile == None:
            color_profile = self.board.color_profile
        
        pixel_size = font // 10
        font = pixel_size * 10
        width = font * 14
        height = font * 3
        
        draw_rectangle(x, y, width, height, color_profile.neutral)
        draw_rectangle(x + pixel_size, y + pixel_size, width - 2 * pixel_size, height - 2 * pixel_size, color_profile.fill)
        
        draw_rectangle(x + int(font * (4 * (not self.board.white_player) + 5.5)), y + int(font * 0.5), 4 * font, font, color_profile.white_hl)
        draw_text("white:", x + int(font * 0.7), y + int(font * 0.5), font, color_profile.color_white)
        draw_text("human", x + int(font * 5.7), y + int(font * 0.5), font, color_profile.color_white)
        draw_text("engine", x + int(font * 9.7), y + int(font * 0.5), font, color_profile.color_white)
        
        draw_rectangle(x + int(font * (4 * (not self.board.black_player) + 5.5)), y + int(font * 1.5), 4 * font, font, color_profile.black_hl)
        draw_text("black:", x + int(font * 0.7), y + int(font * 1.5), font, color_profile.color_black)
        draw_text("human", x + int(font * 5.7), y + int(font * 1.5), font, color_profile.color_black)
        draw_text("engine", x + int(font * 9.7), y + int(font * 1.5), font, color_profile.color_black)
    
    def draw_player_black(self, x, y, width, height, font, color_profile=None):
        assert width == None
        assert height == None
        
        if color_profile == None:
            color_profile = self.board.color_profile
        
        pixel_size = font // 10
        font = pixel_size * 10
        width = font * 14
        height = font * 2
        
        draw_rectangle(x, y, width, height, color_profile.neutral)
        draw_rectangle(x + pixel_size, y + pixel_size, width - 2 * pixel_size, height - 2 * pixel_size, color_profile.fill)
        
        draw_rectangle(x + int(font * (4 * (not self.board.black_player) + 5.5)), y + int(font * 0.5), 4 * font, font, color_profile.black_hl)
        draw_text("black:", x + int(font * 0.7), y + int(font * 0.5), font, color_profile.color_black)
        draw_text("human", x + int(font * 5.7), y + int(font * 0.5), font, color_profile.color_black)
        draw_text("engine", x + int(font * 9.7), y + int(font * 0.5), font, color_profile.color_black)
    
    def draw_player_white(self, x, y, width, height, font, color_profile=None):
        assert width == None
        assert height == None
        
        if color_profile == None:
            color_profile = self.board.color_profile
        
        pixel_size = font // 10
        font = pixel_size * 10
        width = font * 14
        height = font * 2
        
        draw_rectangle(x, y, width, height, color_profile.neutral)
        draw_rectangle(x + pixel_size, y + pixel_size, width - 2 * pixel_size, height - 2 * pixel_size, color_profile.fill)
        
        draw_rectangle(x + int(font * (4 * (not self.board.white_player) + 5.5)), y + int(font * 0.5), 4 * font, font, color_profile.white_hl)
        draw_text("white:", x + int(font * 0.7), y + int(font * 0.5), font, color_profile.color_white)
        draw_text("human", x + int(font * 5.7), y + int(font * 0.5), font, color_profile.color_white)
        draw_text("engine", x + int(font * 9.7), y + int(font * 0.5), font, color_profile.color_white)
    
    def draw_search_data(self, x, y, width, height, font, color_profile=None):
        assert height == None
        
        if color_profile == None:
            color_profile = self.board.color_profile
        
        pixel_size = font // 10
        font = pixel_size * 10
        height = font * 6
        
        draw_rectangle(x, y, width, height, color_profile.neutral)
        draw_rectangle(x + pixel_size, y + pixel_size, width - 2 * pixel_size, height - 2 * pixel_size, color_profile.fill)
        
        draw_text("time", x + int(font * 0.7), y + int(font * 0.5), font, color_profile.neutral)
        draw_text("eval", x + int(font * 4.7), y + int(font * 0.5), font, color_profile.neutral)
        draw_text("depth", x + int(font * 8.7), y + int(font * 0.5), font, color_profile.neutral)
        draw_text("pv", x + int(font * 12.7), y + int(font * 0.5), font, color_profile.neutral)
        
        with self.board.search_engine_1.lock:
            if len(self.board.search_engine_1.search_data):
                data = self.board.search_engine_1.search_data[-1].split()
                
                if len(data) >= 13:
                    seconds_elapsed = int(data[11]) // 1000
                    draw_text(f"{seconds_elapsed // 60}:{seconds_elapsed % 60:02d}", x + int(font * 0.7), y + int(font * 1.5), font, color_profile.color_white)
                    
                    draw_text(f"{float(data[3]) / 100:.2f}", x + int(font * 4.7), y + int(font * 1.5), font, color_profile.color_white)
                    
                    draw_text(data[5], x + int(font * 8.7), y + int(font * 1.5), font, color_profile.color_white)
                    
                    x_position = x + int(font * 12.7)
                    y_offset = 0
                    for i in range(0, len(data) - 13):
                        if x_position + 3 * font >= x + width:
                            y_offset += 1
                            x_position = x + int(font * 12.7)
                        
                        if y_offset >= 2:
                            break
                        
                        draw_text(data[13 + i], x_position, y + int(font * (1.5 + y_offset)), font, color_profile.color_white)
                        x_position += 4 * font
        
        with self.board.search_engine_2.lock:
            if len(self.board.search_engine_2.search_data):
                data = self.board.search_engine_2.search_data[-1].split()
                
                if len(data) >= 13:
                    seconds_elapsed = int(data[11]) // 1000
                    draw_text(f"{seconds_elapsed // 60}:{seconds_elapsed % 60:02d}", x + int(font * 0.7), y + int(font * 3.5), font, color_profile.color_black)
                    
                    draw_text(f"{float(data[3]) / 100:.2f}", x + int(font * 4.7), y + int(font * 3.5), font, color_profile.color_black)
                    
                    draw_text(data[5], x + int(font * 8.7), y + int(font * 3.5), font, color_profile.color_black)
                    
                    x_position = x + int(font * 12.7)
                    y_offset = 0
                    for i in range(0, len(data) - 13):
                        if x_position + 3 * font >= x + width:
                            y_offset += 1
                            x_position = x + int(font * 12.7)
                        
                        if y_offset >= 2:
                            break
                        
                        draw_text(data[13 + i], x_position, y + int(font * (3.5 + y_offset)), font, color_profile.color_black)
                        x_position += 4 * font
    
    def draw_theme_library(self, x, y, width, height, font, color_profile=None):
        if color_profile == None:
            color_profile = self.board.color_profile
        
        pixel_size = font // 10
        font = pixel_size * 10
        if width == None:
            width = 18 * font
        height = (height // font) * font
        scroll_index = self.scroll_bar.get_index()
        
        draw_rectangle(x, y, width, height, color_profile.neutral)
        draw_rectangle(x + pixel_size, y + pixel_size, width - 2 * pixel_size, height - 2 * pixel_size, color_profile.fill)
        
        draw_text("themes", x + int(font * 0.7), y + int(font * 0.5), font, color_profile.neutral)
        for i in range(min(len(theme_library), self.scroll_bar.shown)):
            if theme_library[scroll_index + i].background_text == color_profile.background_text:
                draw_rectangle(x + int(font * 0.5), y + int(font * (1.5 + i)), int(width - 7 * font), font, color_profile.neutral_hl)
            
            text_to_draw = theme_library[scroll_index + i].background_text
            if measure_text(text_to_draw, font) >= width - 7.5 * font:
                while measure_text(text_to_draw + "...", font) >= width - 7.5 * font:
                    text_to_draw = text_to_draw[:-1]
            
            draw_text(text_to_draw + "...", x + int(font * 0.7), y + int(font * (1.5 + i)), font, color_profile.neutral)
            theme_library[scroll_index + i].draw(x + int(width - font * 5.8), y + int(font * (1.5 + i)), font, color_profile)
        
        self.scroll_bar.draw(color_profile)
    
    def interact_board(self, x, y, width, height, font):
        if self.board.searching:
            self.board.selected = None
            return
        
        if width == None:
            width = font * 10
        if height == None:
            height = font * 10
        
        pixel_size = font // 10
        
        base_size = 8 * font
        board_size = ((min(width, height) - 2 * font) // base_size) * base_size
        size = board_size + (2 * font)
        square_size = board_size // 8
        
        x += (width - size) // 2 + int(font * 1.5)
        y += (height - size) // 2 + int(font * 0.4)
        
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
            mouse_pos = get_mouse_position()
            mouse_x = mouse_pos.x
            mouse_y = mouse_pos.y
            
            ind_x = int(mouse_x - x) // square_size
            ind_y = int(mouse_y - y) // square_size
            
            if 0 <= ind_x and ind_x < 8 and 0 <= ind_y and ind_y < 8:
                if self.board.selected == None:
                    with self.board.lock:
                        if self.board.board[ind_y][ind_x] != '.':
                            if (len(self.board.move_list) % 2 == 0 and not self.board.board[ind_y][ind_x].islower()) or (len(self.board.move_list) % 2 == 1 and self.board.board[ind_y][ind_x].islower()):
                                self.board.selected = (ind_x, ind_y)
                elif self.board.selected == (ind_x, ind_y):
                    pass
                else:
                    move = engine_util.coord_to_square(self.board.selected[0], self.board.selected[1]) + engine_util.coord_to_square(ind_x, ind_y)
                    
                    if move in self.board.valid_moves:
                        with self.board.lock:
                            self.board.make_move(move)
                            self.board.selected = None
                    elif (move + "q") in self.board.valid_moves: #promotion
                        with self.board.lock:
                            self.board.make_move(move + "q")
                            self.board.selected = None
                    else:
                        with self.board.lock:
                            if self.board.board[ind_y][ind_x] != '.':
                                if (len(self.board.move_list) % 2 == 0 and not self.board.board[ind_y][ind_x].islower()) or (len(self.board.move_list) % 2 == 1 and self.board.board[ind_y][ind_x].islower()):
                                    self.board.selected = (ind_x, ind_y)
    
    def interact_game_history(self, x, y, width, height, font):
        self.scroll_bar.interact()
    
    def interact_players(self, x, y, width, height, font):
        assert width == None
        assert height == None
        
        font = (font // 10) * 10
        width = font * 14
        height = font * 3
        
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
            mouse_pos = get_mouse_position()
            mouse_x = mouse_pos.x
            mouse_y = mouse_pos.y
            
            if x + int(font * 5.5) <= mouse_x and mouse_x < x + int(font * 13.5):
                if y + int(font * 0.5) <= mouse_y and mouse_y < y + int(font * 1.5):
                    self.board.white_player = not self.board.white_player
                elif y + int(font * 1.5) <= mouse_y and mouse_y < y + int(font * 2.5):
                    self.board.black_player = not self.board.black_player
    
    def interact_player_black(self, x, y, width, height, font):
        assert width == None
        assert height == None
        
        font = (font // 10) * 10
        width = font * 14
        height = font * 2
        
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
            mouse_pos = get_mouse_position()
            mouse_x = mouse_pos.x
            mouse_y = mouse_pos.y
            
            if x + int(font * 5.5) <= mouse_x and mouse_x < x + int(font * 13.5) and y + int(font * 0.5) <= mouse_y and mouse_y < y + int(font * 1.5):
                self.board.black_player = not self.board.black_player
    
    def interact_player_white(self, x, y, width, height, font):
        assert width == None
        assert height == None
        
        font = (font // 10) * 10
        width = font * 14
        height = font * 2
        
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
            mouse_pos = get_mouse_position()
            mouse_x = mouse_pos.x
            mouse_y = mouse_pos.y
            
            if x + int(font * 5.5) <= mouse_x and mouse_x < x + int(font * 13.5) and y + int(font * 0.5) <= mouse_y and mouse_y < y + int(font * 1.5):
                self.board.white_player = not self.board.white_player
    
    def interact_theme_library(self, x, y, width, height, font):
        pixel_size = font // 10
        font = pixel_size * 10
        if width == None:
            width = 18 * font
        rows = height // font - 1
        height = (height // font) * font
        scroll_index = self.scroll_bar.get_index()
        mouse_pos = get_mouse_position()
        mouse_x = mouse_pos.x
        mouse_y = mouse_pos.y
        
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
            for i in range(min(len(theme_library), rows - 1)):
                if x + int(font * 0.5) <= mouse_x and mouse_x < x + int(width - font * 6.5) and y + int(font * (1.5 + i)) <= mouse_y and mouse_y < y + int(font * (2.5 + i)):
                    self.board.color_profile = theme_library[scroll_index + i]
                    if self.board.color_profile.background_image != None:
                        background_image = load_image(self.board.color_profile.background_image)
                        scale_factor = screen_height / background_image.height
                        image_resize(background_image, int(scale_factor * background_image.width), screen_height)
                        self.board.background_texture = load_texture_from_image(background_image)
                        unload_image(background_image)
        
        self.scroll_bar.interact()

class Layout:
    def __init__(self, windows):
        self.windows = windows

layout_1 = Layout([
    ("board", 40, 40, None, None, 40, False),
    ("game_history", 1480, 40, 400, 800, 40, True),
    ("players", 480, 40, None, None, 40, False),
    ("search_data", 480, 200, 960, None, 40, False),
    ("theme_library", 40, 480, 720, 360, 40, True)
])

layout_2 = Layout([
    ("board", 40, 160, 720, 760, 40, False),
    ("game_history", 800, 320, 400, 720, 40, True),
    ("player_black", 40, 40, None, None, 40, False),
    ("player_white", 40, 960, None, None, 40, False),
    ("search_data", 800, 40, 1080, None, 40, False),
    ("theme_library", 1240, 320, 640, 720, 40, True)
])

class WindowManager:
    def __init__(self, board):
        self.windows = []
        self.board = board
        
    def add_window(self, window_type, x, y, width, height, font, scrollable):
        self.windows.append(Window(self.board, window_type, x, y, width, height, font, scrollable))
    
    def apply_layout(self, layout):
        for window_args in layout.windows:
            print(window_args)
            self.add_window(*window_args)