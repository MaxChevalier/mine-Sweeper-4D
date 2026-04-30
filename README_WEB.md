# Minesweeper 4D - Web Version

This is the web version of Minesweeper 4D, converted from the original PyQt application to a modern web-based game.

## 🎮 How to Play

### Gameplay
- **Left Click**: Dig a cell to reveal what's underneath
- **Right Click**: Place or remove a flag to mark suspected mines
- **Navigation**: Use the "Previous" and "Next" buttons to explore different layers of the 4D space

### Settings
- **Grid Size**: Set the size of each dimension (2-5 cells per dimension)
- **Number of Bombs**: Choose how many bombs to place (1-50)
- **Visible Dimension**: Select which W layer to view (0-3 for a 4D grid)

### Game Rules
- Uncover all non-bomb cells to win
- Each number indicates how many bombs are adjacent to that cell in 4D space
- Empty cells (0) automatically reveal neighboring cells
- Reach the bottom of the board to see more cells

## 🚀 Running Locally

### Option 1: Using Python
```bash
python -m http.server 8000
```
Then open `http://localhost:8000` in your browser.

### Option 2: Direct File Access
Simply open `index.html` directly in your web browser.

### Option 3: Using Node.js http-server
```bash
npx http-server
```

## 🌐 Playing Online

The game is automatically deployed to GitHub Pages. Visit:
[https://maxchevalier.github.io/mine-Sweeper-4D/](https://maxchevalier.github.io/mine-Sweeper-4D/)

## 📁 Project Structure

```
.
├── index.html           # Main HTML file
├── styles.css          # Styling and layout
├── game.js             # Game logic (4D Minesweeper engine)
├── ui.js               # User interface handling
├── package.json        # Project metadata
├── .nojekyll           # GitHub Pages config (disables Jekyll)
└── .github/
    └── workflows/
        └── deploy.yml  # GitHub Actions deployment workflow
```

## 🔄 Automatic Deployment

The project uses GitHub Actions to automatically deploy to GitHub Pages:
- Triggered on every push to the `main` branch
- Deploys the entire repository as a static website
- No build process required (pure HTML/CSS/JavaScript)

## 🎨 Features

- **4D Game Engine**: Full 4D Minesweeper logic implemented in JavaScript
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Layer Navigation**: Explore different dimensions of the game board
- **Real-time Stats**: Track discovered cells, placed flags, and remaining bombs
- **Smooth Animations**: Intuitive visual feedback for all interactions
- **Dark Mode Compatible**: Adapts to system preferences

## 🧮 Game Algorithm

The game implements a 4-dimensional space where:
- Each cell has up to 80 neighbors (3^4 - 1)
- Bombs and their positions are calculated in 4D
- Number hints reflect adjacent bombs in all 4 dimensions

## 📱 Browser Support

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Improve the UI/UX
- Optimize the game logic

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Original Developer

- [MaxChevalier](https://github.com/MaxChevalier/)

## 🔗 Resources

- Original PyQt Version: [GitHub Repository](https://github.com/MaxChevalier/mine-Sweeper-4D)
- GitHub Pages Documentation: [Getting Started](https://pages.github.com/)
- Minesweeper Rules: [Wikipedia](https://en.wikipedia.org/wiki/Minesweeper_(video_game))
