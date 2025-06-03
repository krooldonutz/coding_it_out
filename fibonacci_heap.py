from typing import List

class FibNode:
    def __init__(self):
        self.key = None
        self.degree: int = 0
        self.marked: bool = False
        self.parent: FibNode = None
        self.child: FibNode = None
        self.left_sibling: FibNode = None
        self.right_sibling: FibNode = None

class FibonacciHeap:
    def __init__(self):
        self.H_min: FibNode = None

    def insert(self, fib_node: FibNode):
        if self.H_min is None:
            self._initialize_heap(fib_node)
        elif fib_node.key < self.H_min.key:
            self._insert_before_min(fib_node)
        else:
            self._insert_after_min(fib_node)

    def _initialize_heap(self, fib_node: FibNode):
        fib_node.left_sibling = fib_node
        fib_node.right_sibling = fib_node
        self.H_min = fib_node

    def _insert_before_min(self, fib_node: FibNode):
        fib_node.right_sibling = self.H_min
        fib_node.left_sibling = self.H_min.left_sibling
        self.H_min.left_sibling.right_sibling = fib_node
        self.H_min.left_sibling = fib_node
        self.H_min = fib_node

    def _insert_after_min(self, fib_node: FibNode):
        fib_node.right_sibling = self.H_min.right_sibling
        fib_node.left_sibling = self.H_min
        self.H_min.right_sibling.left_sibling = fib_node
        self.H_min.right_sibling = fib_node

    def merge(self, heap: 'FibonacciHeap'):
        if heap is None or heap.H_min is None:
            return  # Nothing to merge if the other heap is empty
        if self.H_min is None:
            # If the current heap is empty, adopt the other heap's H_min
            self.H_min = heap.H_min
            return

        # Merge the root lists by connecting the circular doubly linked lists
        self_last = self.H_min.left_sibling
        heap_last = heap.H_min.left_sibling

        self_last.right_sibling = heap.H_min
        heap.H_min.left_sibling = self_last

        heap_last.right_sibling = self.H_min
        self.H_min.left_sibling = heap_last

        # Update H_min to the smallest key
        if heap.H_min.key < self.H_min.key:
            self.H_min = heap.H_min

    def consolidate(self, current: FibNode):
        aux_list = {}
        terminal = current

        while True:
            degree = current.degree
            while degree in aux_list:
                other = aux_list.pop(degree)
                if current.key > other.key:
                    current, other = other, current
                self._link_nodes(current, other)
                degree += 1
            aux_list[degree] = current
            current = current.right_sibling
            if current == terminal:
                break

        # Update H_min to the smallest key in the root list
        self.H_min = None
        for node in aux_list.values():
            if self.H_min is None or node.key < self.H_min.key:
                self.H_min = node

    def extract_min(self) -> FibNode:
        if self.H_min is None:
            return None

        min_node = self.H_min

        # Add all children of min_node to the root list
        if min_node.child is not None:
            child = min_node.child
            end = child

            # Remove parent pointers for all children
            while True:
                next_child = child.right_sibling
                child.parent = None
                child.marked = False

                # Add to root list
                child.right_sibling = self.H_min.right_sibling
                child.left_sibling = self.H_min
                self.H_min.right_sibling.left_sibling = child
                self.H_min.right_sibling = child

                child = next_child
                if child == end:
                    break

        # Remove min_node from the root list
        if min_node.right_sibling == min_node:  # min_node is the only node
            self.H_min = None
        else:
            min_node.left_sibling.right_sibling = min_node.right_sibling
            min_node.right_sibling.left_sibling = min_node.left_sibling
            self.H_min = min_node.right_sibling

            # Consolidate the root list
            self.consolidate(self.H_min)

        return min_node

    def _link_nodes(self, parent: FibNode, child: FibNode):
        # Remove child from the root list
        child.left_sibling.right_sibling = child.right_sibling
        child.right_sibling.left_sibling = child.left_sibling

        # Make child a child of parent
        child.parent = parent
        child.left_sibling = child
        child.right_sibling = child
        if parent.child is None:
            parent.child = child
        else:
            child.right_sibling = parent.child.right_sibling
            child.left_sibling = parent.child
            parent.child.right_sibling.left_sibling = child
            parent.child.right_sibling = child

        # Update parent's degree and mark child as unmarked
        parent.degree += 1
        child.marked = False

    def decrease_key(self, node: FibNode, new_key: int):
        if new_key > node.key:
            raise ValueError("New key must be smaller than the current key.")

        node.key = new_key
        parent = node.parent

        if parent and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)

        if node.key < self.H_min.key:
            self.H_min = node

    def _cut(self, node: FibNode, parent: FibNode):
        # Remove node from the parent's child list
        if parent.child == node:
            if node.right_sibling == node:  # Node is the only child
                parent.child = None
            else:
                parent.child = node.right_sibling
        node.left_sibling.right_sibling = node.right_sibling
        node.right_sibling.left_sibling = node.left_sibling

        # Decrease parent's degree
        parent.degree -= 1

        # Add node to the root list
        node.parent = None
        node.left_sibling = self.H_min.left_sibling
        node.right_sibling = self.H_min
        self.H_min.left_sibling.right_sibling = node
        self.H_min.left_sibling = node
        node.marked = False

    def _cascading_cut(self, node: FibNode):
        parent = node.parent
        if parent:
            if not node.marked:
                node.marked = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)


import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class FibonacciHeapVisualizer:
    def __init__(self, heap: FibonacciHeap):
        self.heap = heap
        self.graph = nx.DiGraph()

    def visualize(self):
        self.graph.clear()
        if self.heap.H_min is None:
            plt.figure(figsize=(8, 6))
            plt.title("Empty Fibonacci Heap")
            plt.text(0.5, 0.5, "Empty Heap", ha='center', va='center', fontsize=14)
            plt.axis('off')
            plt.show()
            return

        # Add all nodes from root list and their children
        self._add_nodes_from_root_list()

        # Create a better layout
        pos = nx.kamada_kawai_layout(self.graph)

        # Draw the graph with different node colors based on properties
        plt.figure(figsize=(12, 10))

        # Draw nodes
        root_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('is_root', False)]
        marked_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('marked', False)]
        normal_nodes = [n for n in self.graph.nodes() if n not in root_nodes and n not in marked_nodes]
        min_node = self.heap.H_min.key if self.heap.H_min else None

        # Draw edges with different styles
        sibling_edges = [(u, v) for u, v, d in self.graph.edges(data=True) if d.get('type') == 'sibling']
        child_edges = [(u, v) for u, v, d in self.graph.edges(data=True) if d.get('type') == 'child']

        # Draw edges
        nx.draw_networkx_edges(self.graph, pos, edgelist=child_edges, arrows=True,
                               arrowstyle='->', arrowsize=15, edge_color='black')
        nx.draw_networkx_edges(self.graph, pos, edgelist=sibling_edges, arrows=True,
                               style='dashed', arrowstyle='->', arrowsize=10, edge_color='blue')

        # Draw nodes with different colors
        nx.draw_networkx_nodes(self.graph, pos, nodelist=normal_nodes, node_size=700,
                               node_color='lightblue', edgecolors='black')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=marked_nodes, node_size=700,
                               node_color='lightgrey', edgecolors='black')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=root_nodes, node_size=700,
                               node_color='lightgreen', edgecolors='black')
        if min_node is not None:
            nx.draw_networkx_nodes(self.graph, pos, nodelist=[min_node], node_size=800,
                                   node_color='yellow', edgecolors='red', linewidths=3)

        # Draw node labels
        node_labels = {n: f"{n}\nd:{d.get('degree', 0)}" +
                          (f"\n(M)" if d.get('marked', False) else "") for n, d in self.graph.nodes(data=True)}
        nx.draw_networkx_labels(self.graph, pos, labels=node_labels)

        # Add legend
        legend_elements = [
            mpatches.Patch(color='lightblue', label='Regular Node'),
            mpatches.Patch(color='lightgreen', label='Root Node'),
            mpatches.Patch(color='lightgrey', label='Marked Node'),
            mpatches.Patch(color='yellow', label='Minimum Node'),
        ]
        plt.legend(handles=legend_elements, loc='upper right')

        plt.title("Fibonacci Heap Visualization")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def _add_nodes_from_root_list(self):
        if not self.heap.H_min:
            return

        start = self.heap.H_min
        current = start

        # Process all nodes in the root list
        while True:
            self._add_node_and_children(current, is_root=True)
            current = current.right_sibling
            if current == start:
                break

        # Add sibling connections
        current = start
        while True:
            next_node = current.right_sibling
            if current != next_node:  # Skip self-loops
                self.graph.add_edge(current.key, next_node.key, type='sibling')
            current = next_node
            if current == start:
                break

    def _add_node_and_children(self, node, is_root=False, parent=None):
        if node is None:
            return

        # Add the node with its attributes
        self.graph.add_node(node.key,
                            is_root=is_root,
                            degree=node.degree,
                            marked=node.marked)

        # Connect with parent if exists
        if parent:
            self.graph.add_edge(parent.key, node.key, type='child')

        # Process children if any
        if node.child:
            child = node.child
            start_child = child

            # Add all children
            while True:
                self._add_node_and_children(child, is_root=False, parent=node)
                child = child.right_sibling
                if child == start_child:
                    break

            # Connect siblings
            child = start_child
            while True:
                next_child = child.right_sibling
                if child != next_child:  # Skip self-loops
                    self.graph.add_edge(child.key, next_child.key, type='sibling')
                child = next_child
                if child == start_child:
                    break

# Example usage
if __name__ == "__main__":
    # Create a Fibonacci Heap
    fib_heap = FibonacciHeap()

    # Insert nodes
    node1 = FibNode()
    node1.key = 10
    fib_heap.insert(node1)

    node2 = FibNode()
    node2.key = 5
    fib_heap.insert(node2)

    node3 = FibNode()
    node3.key = 20
    fib_heap.insert(node3)

    print(fib_heap.extract_min())

    # Visualize the heap
    visualizer = FibonacciHeapVisualizer(fib_heap)
    visualizer.visualize()



