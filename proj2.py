from dataclasses import dataclass, field

@dataclass
class TreeNode:
    char: str
    is_word: bool = False
    children: list["TreeNode"] = field(default_factory=list)

def find_child(node: TreeNode, char: str) -> TreeNode | None:
    if node is None:
        return None
    elif node.children == []:
        return None
    for child in node.children:
        if child.char == char: 
            return child
    return None

    
def binary_search(arr: list[int], target: int, low: int = 0, high: int = None) -> int | None:
    if high is None:
        high = len(arr) - 1
    if low > high:
        return None
    mid = (low + high) // 2
    guess = arr[mid]
    if guess.char == target:
        return mid
    elif guess.char > target:
        return binary_search(arr, target, low, mid - 1)
    else:
        return binary_search(arr, target, mid + 1, high)


def insert_child(node: TreeNode, char: str) -> TreeNode:
    new = TreeNode(char)
    if node is not None:
        if node.children == []:
            node.children.append(new)
            return node 
        else:
            for index, child in enumerate(node.children):
                if child.char >= new.char: 
                    node.children.insert(index, new)
                    return node 
    else:
        return new

          
def insert_word(root: TreeNode, word: str) -> TreeNode:
    
    def insert_helper(root: TreeNode, word: str):
        if root is not None:
            if word == "":
                root.is_word = True
                return root
            char = word[0]
            found = find_child(root, char)
            if found is not None:
                root = found
            else:
                new_root = insert_child(root, char)
                root = find_child(new_root, char)
            return insert_helper(root, word[1:])
    
    leaf = insert_helper(root, word)

    return root


def find_prefix_node(root: TreeNode, prefix: str) -> TreeNode | None:
    if root is None:
        return None
    elif find_child(root, prefix[0]) is not None: 
        for char in prefix:
            root = find_child(root, char)
            if root is None:
                return None 
        return root
    else:
        return None

def collect_words(node: TreeNode, prefix: str) -> list[str]:
    def bfs(node, prefix, collected):
        if node is None:
            return []
        elif len(node.children) == 0:
            collected.append(prefix)
        elif node.is_word:
            collected.append(prefix)
            if len(node.children) > 0:
                for child in node.children:
                    print("test " + child.char)
                    prefix += child.char
                    bfs(child, prefix, collected)
        else:
            for child in node.children:
                prefix = prefix + child.char
                bfs(child, prefix, collected)
        return collected
    
    collected = []
    final = bfs(node, prefix, collected)
    word = []
    for letter in final:
        word.append(letter)
    return final


def preorder_dfs(node: TreeNode | None, prefix) -> list[str]:
    if node is None:
        return[prefix]
    elif len(node.children) > 1:
        for child in node.children:
            return [prefix] + [node.char] + preorder_dfs(child, prefix)
    elif len(node.children) == 1:
        return [prefix] + [node.char] + preorder_dfs(node.children[0], prefix)
    else:
        return [prefix]


def autocomplete(root: TreeNode, prefix: str) -> list[str]:
    starter = find_prefix_node(root, prefix)
    words = collect_words(starter, prefix)
    return words
