# 🐍 Samar's Snake Game

A feature-rich Snake game built with Python and Pygame, supporting both keyboard and joystick controls!

> **🤖 Built with Amazon Q Developer**: This project was created by Samar using Amazon Q's AI-powered coding assistance. Samar had no prior Python knowledge when starting this project - it's a testament to the power of AI-assisted learning and development!

## 🎮 Features

### Gameplay
- Classic snake gameplay with modern enhancements
- Pause/resume functionality (SPACE or joystick button)
- Progressive speed increase as score grows
- Persistent high score tracking
- Game over screen with restart option

### Controls
- **Keyboard**: Arrow keys for movement, SPACE to pause, ESC to quit
- **Joystick**: D-pad or analog stick for movement, Button 0 to pause
- **Restart**: Press R after game over

### Audio
- Sound effects for eating food (pitch increases with score)
- Subtle movement sounds
- Game over sound
- Volume-balanced audio experience

### Visual Enhancements
- Different colors for snake head vs body
- Animated blinking food
- Grid background for better navigation
- Bordered snake segments
- Clean UI with sidebar layout
- Real-time speed counter

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation
1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install pygame numpy
   ```

### Running the Game
```bash
python snake_game.py
```

## 🎯 How to Play
- Control the snake to eat red food
- Avoid hitting walls or your own body
- Score increases with each food eaten
- Game gets faster as your score grows
- Try to beat your high score!

## 🛠️ Development

### Project Structure
- `snake_game.py` - Main game file
- `joystick_test.py` - Joystick testing utility
- `highscore.txt` - Persistent high score storage

### Testing Joystick
Run the joystick test to check controller compatibility:
```bash
python joystick_test.py
```

## 🏆 High Scores
High scores are automatically saved and persist between game sessions.

## 🤝 Contributing
This is Samar's learning project! Feel free to suggest improvements or report bugs.

## 📝 License
This project is open source and available under the MIT License.

---
*Built with ❤️ by Samar*
