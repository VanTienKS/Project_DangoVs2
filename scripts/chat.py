import pygame
import sys
from scripts.settings import *

# Khởi tạo Pygame
pygame.init()

# Cài đặt màn hình và các biến liên quan
WIDTH, HEIGHT = 800, 600
FONT_SIZE = 32
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
input_text_lower = ''
output_text_lines = []

# Tạo màn hình
pygame.display.set_caption("Input Box Example")

# Tạo font
font = pygame.font.SysFont(None, FONT_SIZE)

# Khởi tạo khung nhập liệu
container_rect = pygame.Rect(SCREEN_WIDTH - 500, SCREEN_HEIGHT - 400, 500, 400)  # Khung bao quát
input_rect_upper = pygame.Rect(SCREEN_WIDTH - 475, SCREEN_HEIGHT - 300, 450, 200)  # Khung nhập liệu trên
input_rect_lower = pygame.Rect(SCREEN_WIDTH - 475, SCREEN_HEIGHT - 75, 450, 50)  # Khung nhập liệu dưới
input_color = pygame.Color('lightskyblue3')
active_upper = False
active_lower = False

# Tạo biến cho cuộn nội dung
# scroll_pos = 0


class Chat:
    def __init__(self, player, chat_box):
        # general setup
        self.player = player
        self.toggle_menu = chat_box
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)

        # options
        self.width = 400
        self.space = 10
        self.padding = 8

        # movement
        self.index = 0
        self.input_active = False  # Cờ chỉ trạng thái hiển thị ô nhập liệu
        self.input_text = ""  # Chuỗi lưu dữ liệu nhập vào
        self.scroll_pos = 0  # Vị trí cuộn
        self.input()
    
    def draw_text(self, surface, text, font, color, rect):
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, (rect.x + 5, rect.y + 5))

    def input(self):
        global input_text_lower, active_upper, active_lower
        keys = pygame.key.get_pressed()
        # keys = pygame.key.get_just_pressed()
        
        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()
        
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect_upper.collidepoint(event.pos):
                    active_upper = True
                    active_lower = False
                elif input_rect_lower.collidepoint(event.pos):
                    active_lower = True
                    active_upper = False
                else:
                    active_upper = False
                    active_lower = False
            if event.type == pygame.KEYDOWN:
                if active_lower:
                    if event.key == pygame.K_RETURN:
                        present = f'[{self.player.name}]~ {input_text_lower}'
                        output_text_lines.append(present)  # Thêm nội dung của khung dưới vào danh sách dòng
                        input_text_lower = ''  # Xóa nội dung của khung dưới
                        # Cập nhật vị trí cuộn để hiển thị dòng mới
                        self.scroll_pos = max(0, len(output_text_lines) * FONT_SIZE - input_rect_upper.height)
                    elif event.key == pygame.K_BACKSPACE:
                        input_text_lower = input_text_lower[:-1]  # Xóa ký tự cuối cùng khi nhấn Backspace
                    else:
                        if event.key != pygame.K_ESCAPE:
                            input_text_lower += event.unicode  # Thêm ký tự vào biến input_text_lower
            # Bắt sự kiện cuộn bằng chuột hoặc bàn phím
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                self.scroll_pos = max(0, self.scroll_pos - FONT_SIZE)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                self.scroll_pos = min(self.scroll_pos + FONT_SIZE, max(0, len(output_text_lines) * FONT_SIZE - input_rect_upper.height))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.scroll_pos = max(0, self.scroll_pos - FONT_SIZE)
                if event.key == pygame.K_DOWN:
                    self.scroll_pos = min(self.scroll_pos + FONT_SIZE, max(0, len(output_text_lines) * FONT_SIZE - input_rect_upper.height))

        # Vẽ khung bao quát
        pygame.draw.rect(self.display_surface, BLACK, container_rect, 2)
        # Vẽ khung nhập liệu trên
        pygame.draw.rect(self.display_surface, input_color, input_rect_upper, 2)
        # Vẽ khung nhập liệu dưới
        pygame.draw.rect(self.display_surface, input_color, input_rect_lower, 2)
        
        # Tính toán vị trí và chiều cao của cửa sổ cuộn
        total_lines_height = len(output_text_lines) * FONT_SIZE
        visible_lines_height = input_rect_upper.height
        scrollable_area = max(0, total_lines_height - visible_lines_height)
        scrollable_ratio = scrollable_area / visible_lines_height
        if scrollable_ratio > 0:
            scroll_bar_height = visible_lines_height * visible_lines_height / total_lines_height
            scroll_bar_rect = pygame.Rect(input_rect_upper.right - 10, input_rect_upper.top + (self.scroll_pos / scrollable_area * (visible_lines_height - scroll_bar_height)), 10, scroll_bar_height)
            pygame.draw.rect(self.display_surface, BLACK, scroll_bar_rect)

        # Hiển thị nội dung của khung trên dựa trên self.scroll_pos
        text_y = input_rect_upper.y - self.scroll_pos
        for line in output_text_lines:
            if text_y >= input_rect_upper.y and text_y < input_rect_upper.bottom - FONT_SIZE:
                self.draw_text(self.display_surface, line, font, BLACK, pygame.Rect(input_rect_upper.x, text_y, input_rect_upper.width, FONT_SIZE))
            text_y += FONT_SIZE
        
        # Hiển thị nội dung của khung dưới
        self.draw_text(self.display_surface, input_text_lower, font, BLACK, input_rect_lower)

        # pygame.display.flip()
    
    def update(self):
        self.input()







            
            