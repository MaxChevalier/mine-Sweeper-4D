/**
 * Minesweeper 4D UI Handler
 * Manages the user interface and game interactions
 */

class Game4DUI {
    constructor() {
        this.game = null;
        this.initializeEventListeners();
        this.startNewGame();
    }

    initializeEventListeners() {
        document.getElementById('newGameBtn').addEventListener('click', () => this.startNewGame());
        document.getElementById('resetBtn').addEventListener('click', () => this.resetGame());

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
        document.getElementById('gameStatus').textContent = '';
        document.getElementById('gameStatus').className = 'status';
        this.render();
    }

    resetGame() {
        this.startNewGame();
    }

    render() {
        this.renderBoard();
        this.updateStats();
    }

    renderBoard() {
        const boardContainer = document.getElementById('gameBoard');
        boardContainer.innerHTML = '';

        const size = this.game.size;

        // Create W layers
        for (let w = 0; w < size.W; w++) {
            const wLayer = document.createElement('div');
            wLayer.className = 'w-layer';

            const wLabel = document.createElement('div');
            wLabel.className = 'w-layer-label';
            wLabel.textContent = `W = ${w}`;
            wLayer.appendChild(wLabel);

            const zZone = document.createElement('div');
            zZone.className = 'z-zone';

            // Create Z grids within W layer
            for (let z = 0; z < size.Z; z++) {
                const zGrid = document.createElement('div');
                zGrid.className = 'z-grid';

                const yZone = document.createElement('div');
                yZone.className = 'y-zone';

                // Create Y rows within Z grid
                for (let y = 0; y < size.Y; y++) {
                    const xZone = document.createElement('div');
                    xZone.className = 'x-zone';

                    // Create X columns within Y row
                    for (let x = 0; x < size.X; x++) {
                        const coords = [w, z, y, x];
                        const cell = this.createCellElement(coords);
                        xZone.appendChild(cell);
                    }

                    yZone.appendChild(xZone);
                }

                zGrid.appendChild(yZone);
                zZone.appendChild(zGrid);
            }

            wLayer.appendChild(zZone);
            boardContainer.appendChild(wLayer);
        }
    }

    createCellElement(coords) {
        const cell = document.createElement('button');
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

        // Hover effect for neighbors
        cell.addEventListener('mouseenter', (e) => {
            this.highlightNeighbors(coords, true);
        });

        cell.addEventListener('mouseleave', (e) => {
            this.highlightNeighbors(coords, false);
        });

        return cell;
    }

    highlightNeighbors(coords, highlight) {
        if (this.game.gameOver || this.game.gameWon) return;

        const [w, z, y, x] = coords;
        const size = this.game.size;

        // Get all cells and highlight neighbors in 4D space
        for (let dw = -1; dw <= 1; dw++) {
            for (let dz = -1; dz <= 1; dz++) {
                for (let dy = -1; dy <= 1; dy++) {
                    for (let dx = -1; dx <= 1; dx++) {
                        const nw = w + dw;
                        const nz = z + dz;
                        const ny = y + dy;
                        const nx = x + dx;

                        if (nw >= 0 && nw < size.W && nz >= 0 && nz < size.Z &&
                            ny >= 0 && ny < size.Y && nx >= 0 && nx < size.X) {
                            const neighborKey = `${nw},${nz},${ny},${nx}`;
                            const neighborCell = this.getCellElement(nw, nz, ny, nx);
                            if (neighborCell && !neighborCell.classList.contains('discovered') && !neighborCell.classList.contains('flagged')) {
                                if (highlight) {
                                    neighborCell.style.background = '#E0E0FF';
                                } else {
                                    neighborCell.style.background = '';
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    getCellElement(w, z, y, x) {
        const boardContainer = document.getElementById('gameBoard');
        const wLayers = boardContainer.querySelectorAll('.w-layer');
        if (w < wLayers.length) {
            const wLayer = wLayers[w];
            const zGrids = wLayer.querySelectorAll('.z-grid');
            if (z < zGrids.length) {
                const zGrid = zGrids[z];
                const yZones = zGrid.querySelectorAll('.y-zone > .x-zone');
                if (y < yZones.length) {
                    const xZone = yZones[y];
                    const cells = xZone.querySelectorAll('.cell');
                    if (x < cells.length) {
                        return cells[x];
                    }
                }
            }
        }
        return null;
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
}

// Initialize the game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new Game4DUI();
});
