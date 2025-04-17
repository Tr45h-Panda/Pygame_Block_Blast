import pygame

class InputHandler:
    def __init__(self, blocks):
        self.blocks = blocks

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for block in self.blocks:
                if self.is_mouse_on_block(block):
                    block.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            for block in self.blocks:
                if block.dragging:
                    block.dragging = False

    def is_mouse_on_block(self, block):
        # Check if the mouse is over any part of the block
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for row_idx, row in enumerate(block.shape):
            for col_idx, cell in enumerate(row):
                if cell:  # Only check filled cells
                    cell_rect = pygame.Rect(
                        block.x + col_idx * block.size,
                        block.y + row_idx * block.size,
                        block.size,
                        block.size
                    )
                    if cell_rect.collidepoint(mouse_x, mouse_y):
                        return True
        return False