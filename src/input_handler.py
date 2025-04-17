import pygame

class InputHandler:
    def __init__(self, blocks):
        self.blocks = blocks

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for block in self.blocks:
                is_on_block, row_idx, col_idx = self.is_mouse_on_block(block)
                if is_on_block:
                    block.dragging = True

                    # Calculate the center of the clicked cell
                    clicked_cell_center_x = block.x + col_idx * block.size + block.size // 2
                    clicked_cell_center_y = block.y + row_idx * block.size + block.size // 2

                    # Calculate the offset between the mouse and the center of the clicked cell
                    block.offset_x = mouse_x - clicked_cell_center_x
                    block.offset_y = mouse_y - clicked_cell_center_y

                    break  # Only allow dragging one block at a time

        elif event.type == pygame.MOUSEBUTTONUP:
            for block in self.blocks:
                if block.dragging:
                    block.dragging = False
                    # Reset the offset when dragging stops
                    block.offset_x = 0
                    block.offset_y = 0

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
                        # Return the clicked cell's row and column indices
                        return True, row_idx, col_idx
        return False, None, None