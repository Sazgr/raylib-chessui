from pyray import *

hop_white = Color(238, 238, 239, 255)
hop_bold_gray = Color(205, 207, 210, 255)
hop_dark_gray = Color(155, 160, 166, 255)
hop_maroon = Color(120, 47, 64, 255)
        
class ColorProfile:
    def __init__(self, background = DARKGRAY, background_image = None, background_text = "default", fill = DARKGRAY, neutral = LIGHTGRAY, color_white = WHITE, color_black = BLACK, neutral_hl = YELLOW, white_hl = GREEN, black_hl = RED, neutral_hl_2 = YELLOW, white_hl_2 = GREEN, black_hl_2 = RED):
        self.background = background
        self.background_image = background_image
        self.background_text = background_text
        
        self.fill = fill
        self.neutral = neutral
        self.color_white = color_white
        self.color_black = color_black
        
        self.neutral_hl = neutral_hl
        self.white_hl = white_hl
        self.black_hl = black_hl
        
        self.neutral_hl_2 = neutral_hl_2
        self.white_hl_2 = white_hl_2
        self.black_hl_2 = black_hl_2
    
    def draw(self, x, y, font, color_profile):
        pixel_size = font // 10
        font = 10 * pixel_size
        
        draw_rectangle(x, y + 2 * pixel_size, 4 * font + 2 * pixel_size, 7 * pixel_size, color_profile.neutral)
        
        draw_rectangle(x + 1 * pixel_size, y + 3 * pixel_size, 5 * pixel_size, 5 * pixel_size, self.background)
        draw_rectangle(x + 6 * pixel_size, y + 3 * pixel_size, 5 * pixel_size, 5 * pixel_size, self.fill)
        draw_rectangle(x + 11 * pixel_size, y + 3 * pixel_size, 5 * pixel_size, 5 * pixel_size, self.neutral)
        draw_rectangle(x + 16 * pixel_size, y + 3 * pixel_size, 5 * pixel_size, 5 * pixel_size, self.neutral_hl)
        draw_rectangle(x + 21 * pixel_size, y + 3 * pixel_size, 5 * pixel_size, 5 * pixel_size, self.color_white)
        draw_rectangle(x + 26 * pixel_size, y + 3 * pixel_size, 5 * pixel_size, 5 * pixel_size, self.white_hl)
        draw_rectangle(x + 31 * pixel_size, y + 3 * pixel_size, 5 * pixel_size, 5 * pixel_size, self.color_black)
        draw_rectangle(x + 36 * pixel_size, y + 3 * pixel_size, 5 * pixel_size, 5 * pixel_size, self.black_hl)

default = ColorProfile()

chess_com = ColorProfile(
    Color(47, 46, 43, 255), #dark gray
    None,
    "chess.com",
    
    Color(126, 149, 94, 255), #dark green
    Color(255, 255, 255, 255), #white
    Color(248, 248, 248, 255), #off white
    Color(85, 83, 82, 255), #dark gray
    
    Color(221, 209, 60, 255), #yellow
    Color(189, 201, 91, 255), #green
    Color(108, 128, 81, 255), #dark green
    
    Color(221, 209, 60, 128), #yellow
    Color(189, 201, 91, 128), #green
    Color(108, 128, 81, 128), #dark green
)

hop_theme_1 = ColorProfile(
    Color(238, 238, 238, 255), #hop white
    None,
    "hopkins school | 1",
    
    Color(238, 238, 238, 255), #hop white
    Color(155, 160, 166, 255), #hop dark gray
    Color(120, 47, 64, 255), #hop maroon
    Color(0, 0, 0, 255), #black
    
    Color(205, 207, 210, 255), #hop bold gray
    Color(179, 142, 151, 255), #hop light maroon
    Color(119, 119, 119, 255), #black
    
    Color(205, 207, 210, 128), #hop bold gray
    Color(179, 142, 151, 128), #hop light maroon
    Color(119, 119, 119, 128), #black
)

hop_theme_2 = ColorProfile(
    Color(238, 238, 238, 255), #hop white
    None,
    "hopkins school | 2",
    
    Color(238, 238, 238, 255), #hop white
    Color(120, 47, 64, 255), #hop maroon
    Color(155, 160, 166, 255), #hop dark gray
    Color(0, 0, 0, 255), #black
    
    Color(179, 142, 151, 255), #hop light maroon
    Color(205, 207, 210, 255), #hop bold gray
    Color(119, 119, 119, 255), #black
    
    Color(179, 142, 151, 128), #hop light maroon
    Color(205, 207, 210, 128), #hop bold gray
    Color(119, 119, 119, 128), #black
)

val_chamber_theme = ColorProfile(
    Color(100, 92, 82, 255), #brown
    "assets/chamber_pixel.png",
    "valorant | chamber",
    
    Color(100, 92, 82, 255), #brown
    Color(236, 188, 42, 255), #gold
    Color(255, 112, 164, 255), #light red
    Color(200, 99, 255, 255), #light purple
    
    Color(255, 216, 55, 255), #light gold
    Color(222, 78, 120, 255), #red
    Color(156, 49, 181, 255), #purple
    
    Color(255, 216, 55, 128), #light gold
    Color(222, 78, 120, 128), #red
    Color(156, 49, 181, 128), #purple
)

val_cypher_theme = ColorProfile(
    Color(100, 92, 82, 255), #brown
    "assets/cypher_pixel.png",
    "valorant | cypher",
    
    Color(220, 221, 220, 255), #light gray
    Color(195, 140, 104, 255), #bronze
    Color(90, 140, 206, 255), #blue
    Color(38, 40, 46, 255), #black
    
    Color(255, 173, 143, 255), #light orange
    Color(122, 162, 230, 255), #light blue
    Color(144, 148, 160, 255), #gray
    
    Color(255, 173, 143, 128), #light orange
    Color(122, 162, 230, 128), #light blue
    Color(144, 148, 160, 128), #gray
)

val_deadlock_theme = ColorProfile(
    Color(100, 92, 82, 255), #brown
    "assets/deadlock_pixel.png",
    "valorant | deadlock",
    
    Color(232, 221, 216, 255), #light gray
    #Color(206, 194, 154, 255), #blue
    Color(94, 159, 232, 255), #light blue
    Color(96, 169, 128, 255), #green
    Color(140, 130, 125, 255), #gray
    
    Color(180, 168, 97, 255), #light orange
    Color(57, 107, 91, 255), #dark green
    Color(90, 77, 66, 255), #dark gray
    
    Color(180, 168, 97, 128), #light orange
    Color(57, 107, 91, 128), #dark green
    Color(90, 77, 66, 128), #dark gray
)

val_jett_theme = ColorProfile(
    Color(116, 102, 93, 255), #brown
    "assets/jett_pixel.png",
    "valorant | jett",
    
    Color(236, 252, 252, 255), #off white
    Color(93, 118, 153, 255), #dark blue
    Color(132, 181, 184, 255), #light blue
    Color(90, 94, 112, 255), #gray
    
    Color(164, 185, 202, 255), #gray blue
    Color(184, 216, 218, 255), #light blue
    Color(188, 198, 204, 255), #light gray
    
    Color(164, 185, 202, 128), #gray blue
    Color(184, 216, 218, 128), #light blue
    Color(188, 198, 204, 128), #light gray
)

val_killjoy_theme = ColorProfile(
    Color(100, 92, 82, 255), #brown
    "assets/killjoy_pixel.png",
    "valorant | killjoy",
    
    Color(227, 216, 124, 255),
    #Color(250, 222, 49, 255), #yellow
    Color(49, 49, 11, 255), #black
    Color(164, 69, 51, 255), #pink
    Color(57, 97, 74, 255), #green
    
    Color(201, 153, 52, 255), #yellow
    Color(234, 137, 255, 255), #pink
    Color(85, 156, 113, 255), #green
    
    Color(201, 153, 52, 128), #yellow
    Color(234, 137, 255, 128), #pink
    Color(85, 156, 113, 128), #green
)

val_neon_theme = ColorProfile(
    Color(111, 99, 87, 255), #brown
    "assets/neon_pixel.png",
    "valorant | neon",
    
    Color(52, 64, 88, 255), #dark blue
    Color(177, 249, 248, 255), #teal
    Color(203, 200, 71, 255), #yellow
    Color(90, 137, 255, 255), #blue
    
    Color(66, 110, 155, 255), #dark teal
    Color(255, 255, 160, 255), #light yellow
    Color(180, 197, 255, 255), #light blue
    
    Color(66, 110, 155, 128), #dark teal
    Color(255, 255, 160, 128), #light yellow
    Color(180, 197, 255, 128), #light blue
)

val_reyna_theme = ColorProfile(
    Color(100, 92, 82, 255), #brown
    "assets/reyna_pixel.png",
    "valorant | reyna",
    
    Color(66, 61, 90, 255), #dark gray
    Color(156, 123, 99, 255), #bronze
    Color(224, 85, 235, 255), #pink
    Color(143, 152, 186, 255), #gray
    
    Color(244, 183, 137, 255), #light bronze
    Color(250, 151, 250, 255), #light pink
    Color(199, 203, 220, 255), #light gray
    
    Color(244, 183, 137, 128), #bronze
    Color(250, 151, 250, 128), #light pink
    Color(199, 203, 220, 128), #light gray
)

val_sage_theme = ColorProfile(
    Color(102, 92, 82, 255), #brown
    "assets/sage_pixel.jpg",
    "valorant | sage",
    
    Color(234, 225, 239, 255), #white
    Color(123, 87, 53, 255), #bronze
    Color(11, 178, 176, 255), #teal
    Color(24, 21, 21, 255), #black
    
    Color(183, 160, 100, 255), #light orange
    Color(63, 225, 192, 255), #light teal
    Color(160, 142, 142, 255), #gray
    
    Color(183, 160, 100, 128), #light orange
    Color(63, 225, 192, 128), #light teal
    Color(160, 142, 142, 128), #gray
)

val_viper_theme = ColorProfile(
    Color(114, 101, 92, 255), #brown
    "assets/viper_pixel.png",
    "valorant | viper",
    
    Color(30, 30, 38, 255), #black
    Color(162, 198, 85, 255), #light green
    Color(8, 147, 60, 255), #green
    Color(93, 82, 126, 255), #jet
    
    Color(96, 114, 62, 255), #yellow green
    Color(19, 89, 49, 255), #dark green
    Color(62, 56, 82, 255), #jet
    
    Color(96, 114, 62, 128), #yellow green
    Color(19, 89, 49, 128), #dark green
    Color(62, 56, 82, 128), #jet
)

val_vyse_theme = ColorProfile(
    Color(102, 92, 82, 255), #brown
    "assets/vyse_pixel.png",
    "valorant | vyse",
    
    Color(176, 186, 212, 255), #gray
    Color(127, 114, 153, 255), #dark gray
    Color(135, 27, 182, 255), #magenta
    Color(79, 0, 219, 255), #purple
    
    Color(254, 222, 80, 255), #light yellow
    Color(155, 106, 197, 255), #magenta
    Color(127, 93, 216, 255), #purple
    
    Color(253, 168, 77, 128), #light orange
    Color(155, 106, 197, 128), #magenta
    Color(127, 93, 216, 128), #purple
)

theme_library = [
    default,
    chess_com,
    hop_theme_1,
    hop_theme_2,
    val_chamber_theme,
    val_cypher_theme,
    val_deadlock_theme,
    val_jett_theme,
    val_killjoy_theme,
    val_neon_theme,
    val_reyna_theme,
    val_sage_theme,
    val_viper_theme,
    val_vyse_theme,
]
