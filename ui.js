/**
 * Minesweeper 4D UI Handler
 * Manages the user interface and game interactions
 */

class Game4DUI {
    constructor() {
        this.game = null;
        this.currentDimension = 0;
        this.initializeEventListeners();
        this.startNewGame();
    }

    initializeEventListeners() {
        document.getElementById('newGameBtn').addEventListener('click', () => this.startNewGame());
        document.getElementById('resetBtn').addEventListener('click', () => this.resetGame());
        document.getElementById('prevDim').addEventListener('click', () => this.previousDimension());
        document.getElementById('nextDim').addEventListener('click', () => this.nextDimension());

        // Update stats when settings change
        document.getElementById('gridSize').addEventListener('change', () => this.startNewGame());
        document.getElementById('bombCount').addEventListener('change', () => this.startNewGame());
    }

    startNewGame() {
        const gridSize = parseInt(document.getElementById('gridSize').value);
        const bombCount = parseInt(document.getElementById('bombCount').value);

        const size = {
            X: gridSize,
            Y: gridSize,
            Z: gridSize,
            W: gridSize,
        };

        this.game = new Game4D(size, bombCount);
        this.currentDimension = 0;
        document.getElementById('gameStatus').textContent = '';
        document.getElementById('gameStatus').className = 'status';
        this.render();
    }

    resetGame() {
        this.startNewGame();
    }

    previousDimension() {
        if (this.currentDimension > 0) {
            this.currentDimension--;
            this.render();
        }
    }

    nextDimension() {
        const maxDim = this.game.size.W - 1;
        if (this.currentDimension < maxDim) {
            this.currentDimension++;
            this.render();
        }
    }

    render() {
        this.renderBoard();
        this.updateStats();
        this.updateDimensionControls();
    }

    renderBoard() {
        const boardContainer = document.getElementById('gameBoard');
        boardContainer.innerHTML = '';

        const w = this.currentDimension;
        const size = this.game.size;

        // Create cells for the 3D slice at dimension W
        for (let z = 0; z < size.Z; z++) {
            for (let y = 0; y < size.Y; y++) {
                for (let x = 0; x < size.X; x++) {
                    const coords = [w, z, y, x];
                    const cell = this.createCellElement(coords);
                    boardContainer.appendChild(cell);
                }
            }
        }
    }

    createCellElement(coords) {
        const cell = document.createElement('div');
        cell.className = 'cell';

        const state = this.game.getCellState(coords);
        const cellValue = this.game.getCell(coords);

        if (state === 'hidden') {
            cell.textContent = '';
        } else if (state === 'flagged') {
            cell.classList.add('flagged');
            cell.textContent = '🚩';
        } else if (state === 'discovered') {
            cell.classList.add('discovered');
            if (cellValue === 0) {
                cell.classList.add('empty');
                cell.textContent = '';
            } else if (cellValue > 0) {
                cell.classList.add('number', `number${cellValue >= 4 ? '4' : cellValue}`);
                cell.textContent = cellValue;
            }
        } else if (state === 'bomb') {
            cell.classList.add('discovered', 'bomb');
            cell.textContent = '💣';
        } else if (state === 'empty') {
            cell.classList.add('discovered', 'empty');
            cell.textContent = '';
        } else if (state === 'number') {
            cell.classList.add('discovered', 'number', `number${cellValue >= 4 ? '4' : cellValue}`);
            cell.textContent = cellValue;
        }

        // Add event listeners
        cell.addEventListener('click', (e) => {
            e.preventDefault();
            this.handleCellClick(coords, false);
        });

        cell.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            this.handleCellClick(coords, true);
        });

        return cell;
    }

    handleCellClick(coords, isRightClick) {
        if (this.game.gameOver || this.game.gameWon) {
            return;
        }

        if (isRightClick) {
            this.game.toggleFlag(coords);
        } else {
            const hitBomb = this.game.dig(coords);
            if (hitBomb && this.game.getCell(coords) === -1) {
                this.endGame(false);
            }
        }

        if (this.game.gameWon) {
            this.endGame(true);
        }

        this.render();
    }

    endGame(won) {
        const statusElement = document.getElementById('gameStatus');
        if (won) {
            statusElement.textContent = '🎉 You Won! All mines cleared!';
            statusElement.className = 'status success';
        } else {
            statusElement.textContent = '💥 Game Over! You hit a bomb!';
            statusElement.className = 'status danger';
        }
    }

    updateStats() {
        const stats = this.game.getStats();
        document.getElementById('bombsRemaining').textContent = Math.max(0, stats.bombsRemaining);
        document.getElementById('discoveredCount').textContent = stats.discovered;
        document.getElementById('flagCount').textContent = stats.flagged;
    }

    updateDimensionControls() {
        const maxDim = this.game.size.W - 1;
        document.getElementById('prevDim').disabled = this.currentDimension === 0;
        document.getElementById('nextDim').disabled = this.currentDimension === maxDim;
        document.getElementById('currentDim').textContent = 
            `Layer ${this.currentDimension} of ${maxDim}`;
    }
}

// Initialize the game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new Game4DUI();
});
