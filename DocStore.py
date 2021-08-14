import json
import uuid
import time
from Trie import Trie
  
class DocStore:
    def __init__(self):
        self.mainStore = {}
        self.lookupStore = {}

    def add(self, request):
        #print(request)
        data = json.loads(request)
        #print(data)
        docid = str(uuid.uuid4())
        self.mainStore[docid] = data
        #print(self.mainStore)
        for key,value in data.items():
            val = (docid, value)
            if key not in self.lookupStore.keys():
                self.lookupStore[key] = Trie(key)
            trieobj = self.lookupStore[key]
            #print("trieobj for key is ", key, trieobj.val)
            #print("Val for insert is ", val)
            trieobj.insert(val)
        #print(self.lookupStore)   #print(trieobj)
        return

    def get(self, request):
        res= []
        finallist = []
        data = json.loads(request)
        #print(data)
        for k,v in data.items():
            if k in self.lookupStore.keys():
                #print("here in get for ", k, v)
                trieobj = self.lookupStore[k]
                temp = trieobj.search(v)
                #print(temp)
                res.append(temp)
        if len(res)== 0:
            return
        x= res[0]
        for item in x:
            #print(item)
            failed = False
            for i in range(1,len(res)):
                if item not in res[i]:
                    failed = True
                    break
                else:
                    continue
            if  failed == False:
                finallist.append(item)
        #print(finallist)
        for item in finallist:
            #print(item)
            if item in self.mainStore:
                print(json.dumps(self.mainStore[item]))
        return

    def delete(self,request):
        res = []
        finallist = []
        data = json.loads(request)
        for k, v in data.items():
            if k in self.lookupStore.keys():
                trieobj = self.lookupStore[k]
                res.append(trieobj.search(v))
                # print(res)
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
            if not failed:
                finallist.append(item)
        #print(finallist)
        for item in finallist:
            if item in self.mainStore:
                self.mainStore.pop(item)
        return


if __name__ == '__main__':

    docstore = DocStore()
    str_inp = ['add {"id":1,"last":"Doe","first":"John","location":{"city":"Oakland","state":"CA","postalCode":"94607"},"active":true}',
'add {"id":2,"last":"Doe","first":"Jane","location":{"city":"SanFransicso","state":"CA","postalCode":"94105"},"active":true}',
'add {"id":3,"last":"Black","first":"Jim","location":{"city":"Spokane","state":"WA","postalCode":"99207"},"active":true}',
'add {"id":4,"last":"Frost","first":"Jack","location":{"city":"Seattle","state":"WA","postalCode":"98204"},"active":false}',
'get {"id":4}']
    for item in str_inp:

        op = item.split(' ')[0]
        payload = item.split(' ')[1]
        if op == 'add':
            docstore.add(payload)
        elif op== 'get':
            print(payload)
            docstore.get(payload)
        elif op== 'delete':
            docstore.delete(payload)
        else:
            print('invalid input')

