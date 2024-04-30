import pygame, sys
from scripts.settings import *

class Chat:
    def __init__(self, player_name, toggle_chat):
        # general setup
        self.player_name = player_name
        self.toggle_chat = toggle_chat
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)
        
        self.input_text_lower = ''
        self.output_text_lines = []
        
        # option
        self.width = 500
        self.height = 300
        self.space1 = 30 
        self.space2 = 10 
        
        self.padding = 8
        
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((200,200,200))
        self.input_rect_upper = pygame.Rect(self.space1 + self.space2, SCREEN_HEIGHT - self.space1 - self.image.get_height() + self.space2, self.image.get_width() - self.space2 * 2, 220)  # Khung nhập liệu trên
        self.input_rect_lower = pygame.Rect(self.space1 + self.space2, SCREEN_HEIGHT - self.space1 - 50 - self.space2, self.image.get_width() - self.space2 * 2, 50)  # Khung nhập liệu dưới
        
        self.chating = False
        self.has_chat = False
        self.scroll_pos = 0  # Vị trí cuộn
        
    def draw_text(self, surface, text, font, color, rect):
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, (rect.x + 5, rect.y + 5))    
        
    def input(self):
        keys = pygame.key.get_pressed()
        # keys = pygame.key.get_just_pressed()
        
        if keys[pygame.K_ESCAPE]:
            self.toggle_chat()
        
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect_lower.collidepoint(event.pos):
                    self.chating = True
                else:
                    self.chating = False

            if event.type == pygame.KEYDOWN:
                if self.chating:
                    if event.key == pygame.K_RETURN:
                        present = f'[{self.player_name}]~ {self.input_text_lower}'
                        self.output_text_lines.append(present)  # Thêm nội dung của khung dưới vào danh sách dòng
                        self.has_chat = True
                        self.input_text_lower = ''  # Xóa nội dung của khung dưới
                        # Cập nhật vị trí cuộn để hiển thị dòng mới
                        self.scroll_pos = max(0, len(self.output_text_lines) *FONT_SIZE - self.input_rect_upper.height)
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text_lower = self.input_text_lower[:-1]  # Xóa ký tự cuối cùng khi nhấn Backspace
                    else:
                        if event.key != pygame.K_ESCAPE:
                            self.input_text_lower += event.unicode  # Thêm ký tự vào biến self.input_text_lower
            
            # Bắt sự kiện cuộn bằng chuột hoặc bàn phím
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                self.scroll_pos = max(0, self.scroll_pos -FONT_SIZE)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                self.scroll_pos = min(self.scroll_pos +FONT_SIZE, max(0, len(self.output_text_lines) *FONT_SIZE - self.input_rect_upper.height))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.scroll_pos = max(0, self.scroll_pos -FONT_SIZE)
                if event.key == pygame.K_DOWN:
                    self.scroll_pos = min(self.scroll_pos +FONT_SIZE, max(0, len(self.output_text_lines) *FONT_SIZE - self.input_rect_upper.height))
                    
        # Tính toán vị trí và chiều cao của cửa sổ cuộn
        total_lines_height = len(self.output_text_lines) * FONT_SIZE
        visible_lines_height = self.input_rect_upper.height
        scrollable_area = max(0, total_lines_height - visible_lines_height)
        scrollable_ratio = scrollable_area / visible_lines_height
        
        if scrollable_ratio > 0:
            scroll_bar_height = visible_lines_height * visible_lines_height / total_lines_height
            scroll_bar_rect = pygame.Rect(self.input_rect_upper.right - 10, self.input_rect_upper.top + (self.scroll_pos / scrollable_area * (visible_lines_height - scroll_bar_height)), 10, scroll_bar_height)
            pygame.draw.rect(self.display_surface, (0,0,0), scroll_bar_rect)

        # Hiển thị nội dung của khung trên dựa trên self.scroll_pos
        text_y = self.input_rect_upper.y - self.scroll_pos - (20 if self.scroll_pos > 0 else 0)
        for line in self.output_text_lines:
            if text_y >= self.input_rect_upper.y and text_y < self.input_rect_upper.bottom - FONT_SIZE:
                self.draw_text(self.display_surface, line, self.font, (255,255,255), pygame.Rect(self.input_rect_upper.x, text_y, self.input_rect_upper.width, FONT_SIZE))
            text_y += FONT_SIZE
            
        self.draw_text(self.display_surface, self.input_text_lower, self.font, (255,255,255), self.input_rect_lower)
        
    
    
    def update(self):
        self.input()
        self.display_surface.blit(self.image, (self.space1, SCREEN_HEIGHT - self.height - self.space1), special_flags=pygame.BLEND_RGB_MULT)
        pygame.draw.rect(self.display_surface, (255,255,255), self.input_rect_upper, 2, 10)
        pygame.draw.rect(self.display_surface, (255,255,255), self.input_rect_lower, 2, 5)
        
        