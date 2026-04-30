/**
 * Minesweeper 4D Game Engine
 * Converts the 4D game logic from Python to JavaScript
 */

class Game4D {
    constructor(size, bombs) {
        this.size = size; // { X, Y, Z, W } - dimensions
        this.bombs = bombs;
        this.table = this.initializeTable();
        this.placeBombs();
        this.discovered = new Set();
        this.flagged = new Set();
        this.gameOver = false;
        this.gameWon = false;
    }

    /**
     * Initialize a 4D table with zeros
     */
    initializeTable() {
        const table = [];
        for (let w = 0; w < this.size.W; w++) {
            const wLayer = [];
            for (let z = 0; z < this.size.Z; z++) {
                const zLayer = [];
                for (let y = 0; y < this.size.Y; y++) {
                    const yLayer = [];
                    for (let x = 0; x < this.size.X; x++) {
                        yLayer.push(0);
                    }
                    zLayer.push(yLayer);
                }
                wLayer.push(zLayer);
            }
            table.push(wLayer);
        }
        return table;
    }

    /**
     * Place bombs randomly in the 4D space
     */
    placeBombs() {
        let bombsPlaced = 0;
        while (bombsPlaced < this.bombs) {
            const coords = [
                Math.floor(Math.random() * this.size.W),
                Math.floor(Math.random() * this.size.Z),
                Math.floor(Math.random() * this.size.Y),
                Math.floor(Math.random() * this.size.X),
            ];

            if (this.getCell(coords) !== -1) {
                // Place bomb
                this.setCell(coords, -1);

                // Increment neighbors
                for (let dw = -1; dw <= 1; dw++) {
                    for (let dz = -1; dz <= 1; dz++) {
                        for (let dy = -1; dy <= 1; dy++) {
                            for (let dx = -1; dx <= 1; dx++) {
                                const neighborCoords = [
                                    coords[0] + dw,
                                    coords[1] + dz,
                                    coords[2] + dy,
                                    coords[3] + dx,
                                ];

                                if (this.isValidCoords(neighborCoords) &&
                                    this.getCell(neighborCoords) !== -1) {
                                    this.incrementCell(neighborCoords);
                                }
                            }
                        }
                    }
                }

                bombsPlaced++;
            }
        }
    }

    /**
     * Get cell value from 4D coordinates [W, Z, Y, X]
     */
    getCell([w, z, y, x]) {
        return this.table[w]?.[z]?.[y]?.[x] ?? undefined;
    }

    /**
     * Set cell value
     */
    setCell([w, z, y, x], value) {
        if (this.isValidCoords([w, z, y, x])) {
            this.table[w][z][y][x] = value;
        }
    }

    /**
     * Increment cell value
     */
    incrementCell([w, z, y, x]) {
        if (this.isValidCoords([w, z, y, x])) {
            this.table[w][z][y][x]++;
        }
    }

    /**
     * Check if coordinates are valid
     */
    isValidCoords([w, z, y, x]) {
        return (
            w >= 0 && w < this.size.W &&
            z >= 0 && z < this.size.Z &&
            y >= 0 && y < this.size.Y &&
            x >= 0 && x < this.size.X
        );
    }

    /**
     * Get unique key for coordinates
     */
    getCoordsKey([w, z, y, x]) {
        return `${w},${z},${y},${x}`;
    }

    /**
     * Dig a cell
     */
    dig(coords) {
        if (this.gameOver || this.gameWon) return false;
        if (this.flagged.has(this.getCoordsKey(coords))) return false;
        if (this.discovered.has(this.getCoordsKey(coords))) return false;

        const key = this.getCoordsKey(coords);
        const cellValue = this.getCell(coords);

        if (cellValue === -1) {
            // Hit a bomb!
            this.gameOver = true;
            this.revealAllBombs();
            return true;
        }

        // Dig the cell
        this.discovered.add(key);

        // If empty, recursively dig neighbors
        if (cellValue === 0) {
            this.digNeighbors(coords);
        }

        // Check win condition
        this.checkWinCondition();

        return true;
    }

    /**
     * Recursively dig neighbors of an empty cell
     */
    digNeighbors([w, z, y, x]) {
        for (let dw = -1; dw <= 1; dw++) {
            for (let dz = -1; dz <= 1; dz++) {
                for (let dy = -1; dy <= 1; dy++) {
                    for (let dx = -1; dx <= 1; dx++) {
                        const neighborCoords = [
                            w + dw,
                            z + dz,
                            y + dy,
                            x + dx,
                        ];

                        if (this.isValidCoords(neighborCoords)) {
                            const key = this.getCoordsKey(neighborCoords);
                            const cellValue = this.getCell(neighborCoords);

                            if (!this.discovered.has(key) && 
                                !this.flagged.has(key) && 
                                cellValue !== -1) {
                                this.discovered.add(key);

                                if (cellValue === 0) {
                                    this.digNeighbors(neighborCoords);
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    /**
     * Toggle flag on a cell
     */
    toggleFlag(coords) {
        if (this.gameOver || this.gameWon) return false;
        if (this.discovered.has(this.getCoordsKey(coords))) return false;

        const key = this.getCoordsKey(coords);
        if (this.flagged.has(key)) {
            this.flagged.delete(key);
        } else {
            this.flagged.add(key);
        }

        return true;
    }

    /**
     * Reveal all bombs (game over)
     */
    revealAllBombs() {
        for (let w = 0; w < this.size.W; w++) {
            for (let z = 0; z < this.size.Z; z++) {
                for (let y = 0; y < this.size.Y; y++) {
                    for (let x = 0; x < this.size.X; x++) {
                        const coords = [w, z, y, x];
                        if (this.getCell(coords) === -1) {
                            this.discovered.add(this.getCoordsKey(coords));
                        }
                    }
                }
            }
        }
    }

    /**
     * Check if player has won
     */
    checkWinCondition() {
        const totalCells = this.size.W * this.size.Z * this.size.Y * this.size.X;
        const discoveredNonBombs = this.discovered.size;
        const expectedNonBombs = totalCells - this.bombs;

        if (discoveredNonBombs === expectedNonBombs) {
            this.gameWon = true;
        }
    }

    /**
     * Get game state for rendering
     */
    getCellState(coords) {
        const key = this.getCoordsKey(coords);
        const cellValue = this.getCell(coords);

        if (!this.discovered.has(key)) {
            if (this.flagged.has(key)) {
                return 'flagged';
            }
            return 'hidden';
        }

        if (cellValue === -1) {
            return 'bomb';
        }

        if (cellValue === 0) {
            return 'empty';
        }

        return 'number';
    }

    /**
     * Get total cells
     */
    getTotalCells() {
        return this.size.W * this.size.Z * this.size.Y * this.size.X;
    }

    /**
     * Get stats
     */
    getStats() {
        return {
            discovered: this.discovered.size,
            flagged: this.flagged.size,
            bombsRemaining: this.bombs - this.flagged.size,
            totalCells: this.getTotalCells(),
        };
    }
}

// Export for use in UI
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Game4D;
}
