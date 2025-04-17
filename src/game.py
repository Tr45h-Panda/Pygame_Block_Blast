import pygame
from object import BlockObject, spawn_random_block
from clear_line import ClearLine

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False  # Track if the game is over

        # Grid setup (8x8)
        self.grid_size = 8
        self.cell_size = 50
        self.grid_width = self.grid_size * self.cell_size
        self.grid_height = self.grid_size * self.cell_size

        # Center the grid on the screen
        self.grid_x = (self.screen_width - self.grid_width) // 2
        self.grid_y = (self.screen_height - self.grid_height) // 2

        # Initialize the grid
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Define spawn positions for preview blocks
        self.block_spawn_positions = [
            (self.grid_x + i * (self.cell_size + 50), self.grid_y + self.grid_height + 20)
            for i in range(3)
        ]

        # Create preview blocks (small icons)
        self.preview_blocks = [self.spawn_preview_block(pos) for pos in self.block_spawn_positions]
        self.active_block = None  # The full-size block being dragged
        self.active_block_original_position = None  # Store the original position of the active block
        self.active_block_index = None  # Track which preview block was picked up
        self.placed_blocks = 0  # Counter for placed blocks

        # Initialize ClearLine
        self.clear_line = ClearLine(self.grid)

    def spawn_preview_block(self, position):
        x, y = position
        return spawn_random_block(x, y, preview=True)

    def spawn_full_block(self, preview_block):
        # Create a full-size block based on the preview block's shape and color
        return BlockObject(
            preview_block.x,  # Start at the same position as the preview block
            preview_block.y,
            preview_block.color,  # Use the same color
            50,  # Full-size block
            preview_block.shape,  # Use the same shape
        )

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if not self.game_over:
                    self.handle_events(event)

            if not self.game_over:
                self.update()
            self.render()
            self.clock.tick(60)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, preview_block in enumerate(self.preview_blocks):
                if self.is_mouse_on_block(preview_block):
                    # Spawn the full-size block and start dragging it
                    self.active_block = self.spawn_full_block(preview_block)
                    self.active_block.dragging = True
                    self.active_block_original_position = (preview_block.x, preview_block.y)
                    self.active_block_index = i  # Track which preview block was picked up
                    del self.preview_blocks[i]  # Remove the preview block
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.active_block and self.active_block.dragging:
                self.active_block.dragging = False
                if self.snap_to_grid(self.active_block):
                    self.active_block.placed = True
                    self.placed_blocks += 1
                    self.active_block = None  # Clear the active block

                    # Check if all blocks in the current set have been placed
                    if self.placed_blocks == 3:
                        self.spawn_new_set_of_blocks()
                else:
                    # If not placed, return the block to its original position
                    self.active_block.x, self.active_block.y = self.active_block_original_position
                    self.active_block.size = 25  # Resize it back to preview size
                    self.preview_blocks.insert(self.active_block_index, self.active_block)  # Restore it to the preview list
                    self.active_block = None  # Clear the active block

    def spawn_new_set_of_blocks(self):
        # Spawn a new set of preview blocks
        self.preview_blocks = [self.spawn_preview_block(pos) for pos in self.block_spawn_positions]
        self.placed_blocks = 0  # Reset the counter for the new set

    def update(self):
        # Update logic for the active block
        if self.active_block:
            self.active_block.update()

        # Check and clear full lines
        self.clear_line.check_and_clear()

        # Only check for game over if there are no active blocks and preview blocks exist
        if not self.active_block and self.preview_blocks:
            self.check_game_over()

    def check_game_over(self):
        # Check if any preview block can be placed on the grid
        for block in self.preview_blocks:
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    if self.can_place_block(block, col, row):
                        print(f"Block {block.shape} can be placed at ({col}, {row})")
                        return  # At least one valid move exists, so the game is not over
        print("No valid moves left. Game Over.")
        self.game_over = True  # No valid moves, game over

    def render(self):
        self.screen.fill((0, 0, 0))  # Clear the screen
        self.draw_grid()  # Draw the grid

        # Render preview blocks
        for preview_block in self.preview_blocks:
            preview_block.render(self.screen)

        # Render the ghost block (if any)
        if self.active_block and self.active_block.dragging:
            self.render_ghost_block(self.active_block)

        # Render the active block (if any)
        if self.active_block:
            self.active_block.render(self.screen)

        # Render game over message
        if self.game_over:
            self.render_game_over()

        pygame.display.flip()

    def render_ghost_block(self, block):
        # Calculate the ghost block's position on the grid
        grid_x = (block.x - self.grid_x) // self.cell_size
        grid_y = (block.y - self.grid_y) // self.cell_size

        # Check if the block fits on the grid
        if not self.can_place_block(block, grid_x, grid_y):
            return  # Don't render the ghost block if it doesn't fit

        # Render the ghost block with reduced opacity
        for row_idx, row in enumerate(block.shape):
            for col_idx, cell in enumerate(row):
                if cell:  # Only render filled cells
                    rect = pygame.Rect(
                        self.grid_x + (grid_x + col_idx) * self.cell_size,
                        self.grid_y + (grid_y + row_idx) * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    )
                    # Render with higher opacity for debugging
                    ghost_color = (*block.color[:3], 150)  # Increase alpha to 150 for better visibility
                    surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                    surface.fill(ghost_color)
                    self.screen.blit(surface, rect.topleft)

    def render_game_over(self):
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text, text_rect)

    def can_place_block(self, block, grid_x, grid_y):
        # Check if the block can be placed at the given grid position
        for row_idx, row in enumerate(block.shape):
            for col_idx, cell in enumerate(row):
                if cell:  # Only check filled cells
                    grid_row = grid_y + row_idx
                    grid_col = grid_x + col_idx
                    if (
                        grid_row < 0 or grid_row >= self.grid_size or  # Out of vertical bounds
                        grid_col < 0 or grid_col >= self.grid_size or  # Out of horizontal bounds
                        self.grid[grid_row][grid_col] != 0  # Cell already occupied
                    ):
                        return False  # Block doesn't fit
        return True

    def draw_grid(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                rect = pygame.Rect(
                    self.grid_x + col * self.cell_size,
                    self.grid_y + row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                if self.grid[row][col] != 0:  # Filled cell
                    pygame.draw.rect(self.screen, self.grid[row][col], rect)  # Use the stored color
                else:  # Empty cell
                    pygame.draw.rect(self.screen, (50, 50, 50), rect)  # Dark gray for empty cells
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)  # Grid border

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
                        block.size,
                    )
                    if cell_rect.collidepoint(mouse_x, mouse_y):
                        return True
        return False

    def snap_to_grid(self, block):
        # Snap the block to the grid if it fits
        grid_x = (block.x - self.grid_x) // self.cell_size
        grid_y = (block.y - self.grid_y) // self.cell_size

        # Check if the block fits within the grid
        for row_idx, row in enumerate(block.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_row = grid_y + row_idx
                    grid_col = grid_x + col_idx
                    if (
                        grid_row < 0 or grid_row >= self.grid_size or
                        grid_col < 0 or grid_col >= self.grid_size or
                        self.grid[grid_row][grid_col] != 0
                    ):
                        return False  # Block doesn't fit

        # Place the block on the grid with its color
        for row_idx, row in enumerate(block.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_row = grid_y + row_idx
                    grid_col = grid_x + col_idx
                    self.grid[grid_row][grid_col] = block.color  # Store the block's color

        # Snap the block's position to the grid
        block.x = self.grid_x + grid_x * self.cell_size
        block.y = self.grid_y + grid_y * self.cell_size
        return True