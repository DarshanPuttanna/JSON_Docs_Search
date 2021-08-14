class TrieNode:

    def __init__(self,val):
        self.val = val

        self.children = {}
        self.documents = []
        return self

class Trie(TrieNode):
    def __init__(self,key=""):
        self.root = super().__init__(key)

    def insert(self, word):
        node = self.root
        doc_id = word[0]
        val = word[1]
        #print("node is ", node.val)
        #print("value in insert is ", val)
        if type(val) == dict:
            for k,v in val.items():
                if k not in node.children:
                    obj = Trie(k)
                    node.children[k] = obj
                obj = node.children[k]
                obj.insert((doc_id,v))
        elif type(val) == str:
            #Loop through each character in the word
            #Check if there is no child containing the character
            for char in val:
                if char in node.children:
                    node = node.children[char]
                else:
                    #if char is not found , create a new node in the trie
                    new_node  = Trie(char)
                    node.children[char] = new_node
                    node = new_node
            node.documents.append(doc_id)
        else:
            if val in node.children:
                node = node.children[val]
            else:
                new_node = Trie(val)
                node.children[val] = new_node
                node = new_node
            node.documents.append(doc_id)
        #print("printing node value", node.val)
        #print("printing documents: ", node.documents)

    def search(self,val,current=""):
        if current == "":
            current = self.root

        if type(val) == dict:
            for k,v in val.items():
                if k in current.children:
                    current = current.children[k]
                    return self.search(v,current)
                else:
                    return []

        elif type(val) == str:
            for v in val:
                if v in current.children:
                    current = current.children[v]
                else:
                    return []
            return current.documents
        
        else:
            if val in current.children:
                current = current.children[val]
                return current.documents
            else:
                return []
        




