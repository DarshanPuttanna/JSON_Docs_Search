import json
import uuid
import time
import sys


def getCommonDocuments(result):
    finallist = []
    x = result[0]
    for item in x:
        failed = False
        for i in range(1, len(result)):
            if item not in result[i]:
                failed = True
                break
            else:
                continue
        if failed == False:
            finallist.append(item)
    return finallist


class TrieNode:

    def __init__(self, val):
        self.val = val
        self.children = {}
        self.documents = []
        return self


class Trie(TrieNode):
    def __init__(self, key=""):
        self.root = super().__init__(key)

    def insert(self, word):
        node = self.root
        doc_id = word[0]
        val = word[1]

        if type(val) == list:
            for item in val:

                if item in node.children:
                    node.children[item].documents.append(doc_id)
                else:
                    new_node = Trie(item)
                    node.children[item] = new_node
                    node.children[item].documents.append(doc_id)

        elif type(val) == dict:
            for k, v in val.items():
                if k not in node.children:
                    obj = Trie(k)
                    node.children[k] = obj
                obj = node.children[k]
                obj.insert((doc_id, v))

        elif type(val) == str:
            for char in val:
                if char in node.children:
                    node = node.children[char]
                else:
                    new_node = Trie(char)
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

    def search(self, val, current=""):
        if current == "":
            current = self.root

        if type(val) == list:
            res = []
            for v in val:
                if v in current.children:
                    res.append(current.children[v].documents)
                else:
                    res.append([])
            return getCommonDocuments(res)

        elif type(val) == dict:
            for k, v in val.items():
                if k in current.children:
                    current = current.children[k]
                    return self.search(v, current)
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


class DocStore:
    def __init__(self):
        self.mainStore = {}
        self.lookupStore = {}

    def add(self, request):
        docid = str(uuid.uuid4())
        self.mainStore[docid] = request

        data = json.loads(request)
        for key, value in data.items():
            if (key == "type" and value == "list"):
                continue

            val = (docid, value)
            if key not in self.lookupStore.keys():
                self.lookupStore[key] = Trie(key)
            trieobj = self.lookupStore[key]
            trieobj.insert(val)
        return

    def get(self, request):
        res = []
        data = json.loads(request)

        if (len(data) == 0):
            for k, v in self.mainStore.items():
                print(v)

        for k, v in data.items():

            if (k == "type" and v == "list"):
                continue

            if k in self.lookupStore.keys():
                trieobj = self.lookupStore[k]
                temp = trieobj.search(v)
                res.append(temp)

        if len(res) == 0:
            return
        finallist = getCommonDocuments(res)
        for item in finallist:
            if item in self.mainStore:
                print(self.mainStore[item])
        return

    def getCommonDocuments(result):
        finallist = []
        x = res[0]
        for item in x:
            failed = False
            for i in range(1, len(res)):
                if item not in res[i]:
                    failed = True
                    break
                else:
                    continue
            if failed == False:
                finallist.append(item)
        return finallist

    def delete(self, request):
        res = []
        finallist = []
        data = json.loads(request)

        for k, v in data.items():
            if (k == "type" and v == "list"):
                continue

            if k in self.lookupStore.keys():
                trieobj = self.lookupStore[k]
                temp = trieobj.search(v)
                res.append(temp)
        if len(res) == 0:
            return
        x = res[0]
        for item in x:
            failed = False
            for i in range(1, len(res)):
                if item not in res[i]:
                    failed = True
                    break
                else:
                    continue
            if failed == False:
                finallist.append(item)
        for item in finallist:
            if item in self.mainStore:
                self.mainStore.pop(item)
        return


if __name__ == '__main__':
    docstore = DocStore()
    for line in sys.stdin:
        x = line.index(' ')
        op = line[:x]
        payload = line[x:].strip()
        if op == 'add':
            docstore.add(payload)
        elif op == 'get':
            docstore.get(payload)
        elif op == 'delete':
            docstore.delete(payload)
        else:
            print('invalid input')
