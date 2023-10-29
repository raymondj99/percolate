class UnionFind:
    """Union Find implementation"""
    def __init__(self, N:int):
        self._array = [i for i in range(N)]

    def root(self, i:int) -> int:
        while i != self._array[i]:
            # Set new root to grandfather node 
            self._array[i] = self._array[self._array[i]]
            i = self._array[i]
        return i

    def connected(self, p:int, q:int) -> bool:
        return self.root(p) == self.root(q)

    def union(self, p: int, q: int) -> None:
        root_p = self.root(p)
        root_q = self.root(q)
        self._array[root_p] = root_q
