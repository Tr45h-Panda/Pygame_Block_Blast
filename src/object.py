import pygame
import random

class BlockObject:
    def __init__(self, x, y, color, size, shape):
        self.x = x
        self.y = y
        self.color = color
        self.size = size  # Size of each cell in the block
        self.shape = shape  # 2D array representing the block's shape
        self.dragging = False
        self.placed = False  # Whether the block has been placed on the grid
        self.offset_x = 0
        self.offset_y = 0

    def update(self):
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Update the block's position using the offset
            self.x = mouse_x - self.offset_x
            self.y = mouse_y - self.offset_y

    def render(self, screen):
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:  # Only render filled cells
                    rect = pygame.Rect(
                        self.x + col_idx * self.size,
                        self.y + row_idx * self.size,
                        self.size,
                        self.size,
                    )
                    render_3d_block(screen, rect, self.color)

def render_3d_block(screen, rect, color):
    # Base color
    pygame.draw.rect(screen, color, rect)

    # Add exaggerated 3D effect
    inner_rect = rect.inflate(-8, -8)  # Smaller inner square
    light_color = tuple(min(c + 80, 255) for c in color[:3])  # Much lighter shade
    dark_color = tuple(max(c - 80, 0) for c in color[:3])  # Much darker shade
    side_color = tuple((light_color[i] + dark_color[i]) // 2 for i in range(3))  # Mid-tone for sides

    # Top highlight
    pygame.draw.polygon(screen, light_color, [
        rect.topleft,
        rect.topright,
        inner_rect.topright,
        inner_rect.topleft
    ])

    # Bottom shadow
    pygame.draw.polygon(screen, dark_color, [
        rect.bottomleft,
        rect.bottomright,
        inner_rect.bottomright,
        inner_rect.bottomleft
    ])

    # Left side shading
    pygame.draw.polygon(screen, side_color, [
        rect.topleft,
        rect.bottomleft,
        inner_rect.bottomleft,
        inner_rect.topleft
    ])

    # Right side shading
    pygame.draw.polygon(screen, side_color, [
        rect.topright,
        rect.bottomright,
        inner_rect.bottomright,
        inner_rect.topright
    ])

# Block templates
BLOCK_SHAPES = {

    "3x3_block": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
    "2x2_block": [[1, 1], [1, 1]],
    "1x1_block": [[1]],

    "2x3_horizontal": [[1, 1, 1], [1, 1, 1]],
    "2x3_vertical": [[1, 1], [1, 1], [1, 1]],

    "T_block": [[0, 1, 0], [1, 1, 1]],
    "T_block_upside_down": [[1, 1, 1], [0, 1, 0]],
    "T_block_left": [[1, 0], [1, 1], [1, 0]],
    "T_block_right": [[0, 1], [1, 1], [0, 1]],


    "L_block_right": [[1, 0], [1, 0], [1, 1]],
    "L_block__right_one_rotation": [[1, 1, 1], [1, 0, 0]],
    "L_block_right_two_rotation": [[1, 1], [0, 1], [0, 1]],
    "L_block_right_three_rotation": [[1, 1], [1, 0], [1, 0]],




    "L_large_block": [[1, 1, 1], [1, 0, 0], [1, 0, 0]],
    "L_large_block_one_rotation": [[1, 1, 1], [0, 0, 1], [0, 0, 1]],
    "L_large_block_two_rotation": [[0, 0, 1], [0, 0, 1], [1, 1, 1]],
    "L_large_block_three_rotation": [[1, 0, 0], [1, 0, 0], [1, 1, 1]],



    "corner_left": [[1, 1], [0, 1]],
    "corner_right": [[1, 0], [1, 1]],
    "corner_left_upside_down": [[0, 1], [1, 1]],
    "corner_right_upside_down": [[1, 1], [1, 0]],

    "z_block": [[1, 1, 0], [0, 1, 1]],
    "z_block_one_rotation": [[0, 1], [1, 1], [1, 0]],
    "z_block_two_rotation": [[1, 0], [1, 1], [0, 1]],

    "s_block": [[0, 1, 1], [1, 1, 0]],
    "s_block_one_rotation": [[1, 0], [1, 1], [0, 1]],
    "s_block_two_rotation": [[1, 1, 0], [0, 1, 1]],


    "1x5_horizontal": [[1, 1, 1, 1, 1]],
    "1x4_horizontal": [[1, 1, 1, 1]],
    "1x3_horizontal": [[1, 1, 1]],
    "1x2_horizontal": [[1, 1]],

    "1x5_vertical": [[1], [1], [1], [1], [1]],
    "1x4_vertical": [[1], [1], [1], [1]],
    "1x3_vertical": [[1], [1], [1]],
    "1x2_vertical": [[1], [1]],



}

def spawn_random_block(x, y, preview=False):
    # Predefined neon colors
    NEON_COLORS = [
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (255, 255, 0),  # Yellow
        (255, 0, 0),    # Bright Red
        (0, 255, 0),    # Bright Green
        (0, 0, 255),    # Bright Blue
        (255, 128, 0),  # Neon Orange
        (128, 0, 255),  # Neon Purple
    ]

    # Randomly select a block shape
    shape_name = random.choice(list(BLOCK_SHAPES.keys()))
    shape = BLOCK_SHAPES[shape_name]

    # Randomly select a neon color
    color = random.choice(NEON_COLORS)

    # Adjust size for preview blocks
    size = 25 if preview else 50

    # Create and return the block object
    return BlockObject(x, y, color, size, shape)