# Block Blast Game

## Overview
Block Blast is a fun and engaging game built using Pygame. The objective of the game is to clear lines by strategically placing blocks. This README provides an overview of the project, setup instructions, and game rules.

## Project Structure
```
block-blast
├── src
│   ├── main.py          # Entry point of the game
│   ├── game.py          # Main game logic
│   ├── object.py        # Game object representation
│   ├── clear_line.py    # Logic for clearing lines
│   └── utils
│       └── __init__.py  # Utility functions and constants
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
└── .gitignore            # Files to ignore in Git
```

## Setup Instructions
1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd block-blast
   ```

2. **Create a virtual environment (optional but recommended):**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the game:**
   ```
   python src/main.py
   ```

## Game Rules
- Players must place blocks strategically to create complete lines.
- Completed lines will be cleared, earning points for the player.
- The game continues until the blocks reach the top of the screen.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.