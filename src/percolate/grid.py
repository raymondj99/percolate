import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

from .utils.union_find import UnionFind

class PercolationGrid:
    """An abstract representation of a physical percolation model"""
    def __init__(self, length:int, height:int, vacancy_percentage: float):
        self.length = int(length)
        self.height = int(height)
        self.grid = [random.random() >= vacancy_percentage for _ in range(self.length * self.height)]
        self.uf = self._construct_trees()

    def _construct_trees(self) -> UnionFind:
        uf = UnionFind(self.length * self.height)
        for g_ind, g in enumerate(self.grid):
            for adj_ind in self._adj_inds(g_ind):
                if g and self.grid[adj_ind]:
                    uf.union(g_ind, adj_ind)
        return uf

    def draw_grid(self, ax) -> None:
        data = np.array(self.grid)
        cmap = colors.ListedColormap(['white', 'black'])
        norm = colors.BoundaryNorm([0, 0.5, 1], cmap.N)
        ax.imshow(data.reshape(self.height, self.length), cmap=cmap, norm=norm)
        ax.set_title(f"Percolates? {self.percolates}")

    def _adj_inds(self, index: int) -> list[int]:
        row = index // self.length
        col = index % self.length
        
        adj_indxs = []
        if row != 0:
            adj_indxs.append(index - self.length)
        if col != 0:
            adj_indxs.append(index - 1) 
        if row != (self.height - 1):
            adj_indxs.append(index + self.length)
        if col != (self.length - 1):
            adj_indxs.append(index + 1) 
        return adj_indxs

    @property
    def percolates(self) -> bool:
        N = self.length * self.height
        for i in range(self.length - 1):
            for j in range(N - 1, N - self.length - 2, -1):
                if self.uf.connected(i, j):
                    return True
        return False
