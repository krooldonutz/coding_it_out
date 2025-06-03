from typing import Dict, Optional
from heapq import heappush, heappop


class BinaryTree:
    def __init__(self, char: Optional[str] = None, freq: Optional[int] = None):
        self.char:str = char  # Character stored in the node
        self.freq:int = freq  # Frequency of the character
        self.left: Optional['BinaryTree'] = None  # Left child
        self.right: Optional['BinaryTree'] = None  # Right child

    def has_child(self):
        return  self.left and  self.right

    def contains(self, i:str):
        return i in self.char

    def __lt__(self, other: 'BinaryTree'):
        return self.freq < other.freq

class HuffmanEncoding:
    def __init__(self):
        self.frequencies: Dict[str, int] = {}  # Character frequencies
        self.codes: Dict[str, str] = {}  # Huffman codes
        self.tree: Optional[BinaryTree] = None  # Root of the Huffman tree

    def add_frequency(self, char: str, freq: int):
        """Add or update the frequency of a character."""
        if char in self.frequencies:
            self.frequencies[char] += freq
        else:
            self.frequencies[char] = freq

    def build__huffman_tree(self, text: str):
        # Build frequency dictionary
        for char in text:
            self.add_frequency(char, 1)

        # Create a priority queue (min-heap) for the nodes
        heap = []
        for char, freq in self.frequencies.items():
            heappush(heap, (freq, BinaryTree(char=char, freq=freq)))

        # Build the Huffman tree
        while len(heap) > 1:
            # Pop two nodes with the smallest frequencies
            freq1, node1 = heappop(heap)
            freq2, node2 = heappop(heap)

            # Create a new BinaryTree node combining the two
            new_node = BinaryTree(char=node1.char + node2.char, freq=freq1 + freq2)
            new_node.left = node1
            new_node.right = node2

            # Push the new node back into the heap
            heappush(heap, (freq1 + freq2, new_node))

        # The final node is the root of the Huffman tree
        self.tree = heappop(heap)[1]

    def get_huffman_path(self) -> Dict[str, str]:
        for i in self.frequencies.keys():
            curr = self.tree
            while curr.has_child():
                if curr.left.contains(i):
                    self.codes[i] = self.codes.get(i, '') + '0'
                    curr = curr.left
                else:
                    self.codes[i] = self.codes.get(i, ' ') +'1'
                    curr = curr.right

        return self.codes

if __name__ == "__main__":

    encoding = HuffmanEncoding()
    text = "A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED"
    encoding.build__huffman_tree(text)
    print(encoding.get_huffman_path())