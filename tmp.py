class Node:
    def __init__(self, val=float('inf')):
        self.min_value = val
        self.left = None
        self.right = None

def build_segment_tree(arr, start, end, tree):
    # Base case (leaf node)
    if start == end:
        tree.min_value = arr[start]
        return

    # Create new nodes for left and right subtrees
    tree.left = Node()
    tree.right = Node()

    # Find middle index
    mid = (start + end) // 2

    # Recursively build left and right subtrees
    build_segment_tree(arr, start, mid, tree.left)
    build_segment_tree(arr, mid + 1, end, tree.right)

    # Update minimum value for the current node
    tree.min_value = min(tree.left.min_value, tree.right.min_value)

def query_minimum(tree, start, end, query_start, query_end):
    # If query range completely overlaps with the node's segment
    if query_start <= tree.left and query_end >= tree.right:
        return tree.min_value
    # If node segment doesn't overlap with query range
    if query_start > tree.right or query_end < tree.left:
        return float('inf')
    # Partial overlap, recurse on both children
    return min(query_minimum(tree.left, start, end, query_start, query_end),
               query_minimum(tree.right, start, end, query_start, query_end))

# Test cases
def test_segment_tree():
    arr = [1, 3, 2, 7, 5]
    n = len(arr)

    # Build segment tree
    root = Node()
    build_segment_tree(arr, 0, n-1, root)

    # Test cases with assertions
    assert query_minimum(root, 0, n-1, 2, 4) == 2  # Minimum in range [2, 4]
    assert query_minimum(root, 0, n-1, 0, 1) == 1  # Minimum in range [0, 1]
    assert query_minimum(root, 0, n-1, 3, 4) == 5  # Minimum in range [3, 4]
    assert query_minimum(root, 0, n-1, 1, 3) == 2  # Minimum in range [1, 3]

if __name__ == "__main__":
    test_segment_tree()
    print("All test cases passed!")
