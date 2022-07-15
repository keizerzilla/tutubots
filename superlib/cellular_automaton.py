import numpy as np
from PIL import Image

class CellularAutomaton:
    
    def __init__(self, rows=64, cols=64, prob=[0.5, 0.5]):
        self.rows = rows
        self.cols = cols
        self.prob = prob
        self.grid = np.random.choice(a=[0, 1], size=(rows, cols), p=prob)
    
    def generate(self, birth=[3], survival=[2, 3], steps=8):
        for step in range(steps):
            new_grid = np.copy(self.grid)
            
            for i in range(self.rows):
                for j in range(self.cols):
                    neigh = self.grid[i, (j-1) % self.cols] +\
                            self.grid[i, (j+1) % self.cols] +\
                            self.grid[(i-1) % self.rows, j] +\
                            self.grid[(i+1) % self.rows, j] +\
                            self.grid[(i-1) % self.rows, (j-1) % self.cols] +\
                            self.grid[(i-1) % self.rows, (j+1) % self.cols] +\
                            self.grid[(i+1) % self.rows, (j-1) % self.cols] +\
                            self.grid[(i+1) % self.rows, (j+1) % self.cols]
                    
                    if self.grid[i, j] == 1:
                        if neigh not in survival:
                            new_grid[i, j] = 0
                    else:
                        if neigh in birth:
                            new_grid[i, j] = 1
            
            self.grid = new_grid
    
    def padding(self, size=1):
        for i in range(size):
            self.grid[i, :] = 0
            self.grid[:, i] = 0
            self.grid[self.rows-1-i, :] = 0
            self.grid[:, self.cols-1-i] = 0
    
    def draw(self, filepath, width=512, height=512):
        img_data = self.grid.astype(np.uint8) * 255
        img = Image.fromarray(img_data)
        img = img.resize((width, height), Image.NEAREST)
        img.save(filepath)


if __name__ == "__main__":
    """
    """
    
    game = CellularAutomaton()
    steps = game.generate(birth=[5, 6, 7, 8], survival=[4, 5, 6, 7, 8])
    game.padding()
    game.draw("cave.bmp")
    
    
