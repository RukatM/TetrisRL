import pygame

def draw_text(text, x, y,size,background, screen):
    font = pygame.font.SysFont("arialblack",size)
    text_color = (0,0,0)
    
    img = font.render(text, True, text_color)
    text_rect = img.get_rect(center=(x, y))

    if background:
        border_width = 3
        border_rect = pygame.Rect(text_rect.left - border_width, text_rect.top - border_width, text_rect.width + 2 * border_width, text_rect.height + 2 * border_width)
        pygame.draw.rect(screen, (0,0,0), border_rect)
        pygame.draw.rect(screen, (147,129,255), text_rect)

    screen.blit(img, text_rect)
