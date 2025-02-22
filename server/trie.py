class TrieNode:
    def __init__(self) -> None:
        self.root = {}
        self.movie_id: list[int] = []
        self.movie_index: list[int] = []

    def get(self, char: str) -> "TrieNode":
        char = char.lower()
        return self.root.get(char, None)

    def get_root(self):
        return self.root

    def contains(self, char: str) -> bool:
        char = char.lower()
        return char in self.root

    def put(self, char: str) -> None:
        char = char.lower()
        self.root[char] = TrieNode()

    def set_movie_id(self, movie_id: int) -> None:
        self.movie_id.append(movie_id)

    def get_movie_id(self) -> list[int]:
        return self.movie_id

    def get_movie_index(self) -> list[int]:
        return self.movie_index

    def set_movie_index(self, index: int) -> None:
        self.movie_index.append(index)

    def __str__(self) -> str:
        res: str = "{"

        for char, node in self.root.items():
            res += f"{char}: {node.__str__()} "

        res += "}"

        return res


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def __str__(self) -> str:
        return str(self.root)

    def insert(self, word: str, movie_id: int, index: int) -> None:
        curr = self.root

        for char in word:
            if not curr.contains(char):
                curr.put(char)
            curr = curr.get(char)

        curr.set_movie_id(movie_id)
        curr.set_movie_index(index)

    def starts_with(
        self, word: str, n: int = 5, allValues=False
    ) -> tuple[list[int], list[int]]:
        ids: list[int] = []
        indexes: list[int] = []

        def _solve(curr: "TrieNode"):
            nonlocal n
            if len(curr.get_movie_id()) > 0:
                ids.extend(curr.get_movie_id())
                indexes.extend(curr.get_movie_index())
                n -= 1
                if n == 0 and not allValues:
                    return True

            chars = curr.get_root()
            for node in chars.values():
                if _solve(node):
                    return True

        curr = self.root
        for char in word:
            curr = curr.get(char)
            if not curr:
                return (ids, indexes)

        _solve(curr)
        return (ids, indexes)

    def search(self, word: str) -> tuple[list[int], list[int]]:
        curr = self.root

        for char in word:
            curr = curr.get(char)
            if not curr:
                return ([], [])

        return (curr.get_movie_id(), curr.get_movie_index())

if __name__ == "__main__":
    t = Trie()
    t.insert("gaurav", 32, 0)
    t.insert("Gaurav", 350, 1)
    t.insert("Hello", 35, -1)
    t.insert("Hello", 39, -1)
    t.insert("HelloPata", 49, -1)
    t.insert("HelloTata", 69, -1)
    t.insert("HelloBye", 420, -1)
    t.insert("Hellw", 420, 1)
    t.insert("Hellwb", 420, 2)

    print(t.starts_with("hellw", n=3, allValues=True))
