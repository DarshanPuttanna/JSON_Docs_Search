import json
import uuid
import time


class DocStore:
    def __init__(self):
        self.__mainstore__ = {}
        self.__lookupstore__ = {}

    def request(self, request_string):
        op = request_string[:request_string.index(' ')].strip()
        request = json.loads(request_string[request_string.index(' '):].strip())
        if op == 'add':
            self.add(request)
        elif op == 'get':
            self.get(request)
        elif op == 'delete':
            self.delete(request)
        else:
            print("ERROR: Invalid operation")

    def add(self, request):
        rid = str(uuid.uuid4())
        self.__mainstore__[rid] = (request, float(time.time() * 1000))
        for key, value in request.items():
            hashkeys = self.__getHashCode__(key, value)
            for hashkey in hashkeys:
                if hashkey not in docstore.__lookupstore__.keys():
                    docstore.__lookupstore__[hashkey] = []
                docstore.__lookupstore__[hashkey].append(rid)
        return

    def get(self, request):
        resultant_list = []
        final_list = []
        for key, value in request.items():
            hashkeys = self.__getHashCode__(key, value)
            for hashkey in hashkeys:
                resultant_list.append(docstore.__lookupstore__.get(hashkey, []))
        minidx, minlist = min(enumerate(resultant_list))
        for elt in minlist:
            failed = False
            for at_idx, at_list in enumerate(resultant_list):
                if minidx != at_idx and elt not in at_list:
                    failed = True
            if not failed:
                final_list.append(docstore.__mainstore__[elt])
        final_list = sorted(final_list, key=lambda x: x[1])
        result = [elt[0] for elt in final_list]
        print(result)
        return

    def delete(self, request):
        resultant_list = []
        final_list = []
        all_hashkeys = []
        for key, value in request:
            hashkeys = self.__getHashCode__(key, value)
            all_hashkeys.extend(hashkeys)
            for hashkey in hashkeys:
                resultant_list.append(docstore.__lookupstore__.get(hashkey, []))
        minidx, minlist = min(enumerate(resultant_list))
        for elt in minlist:
            failed = False
            for at_idx, at_list in enumerate(resultant_list):
                if minidx != at_idx and elt not in at_list:
                    failed = True
            if not failed:
                final_list.append(elt)
        for elt in final_list:
            docstore.__mainstore__.pop(elt)
        for hashkey in all_hashkeys:
            for elt in final_list:
                docstore.__lookupstore__[hashkey].remove(elt)
                if len(docstore.__lookupstore__[hashkey]) == 0:
                    docstore.__lookupstore__.pop(hashkey)
        return

    def __getHashCode__(self, key, value):
        if type(value) != dict:
            return [key + '_' + str(value)]
        hashcode = []
        if type(value) == dict:
            for k, v in value.items():
                hashcode.extend([key + '_' + x for x in self.__getHashCode__(k, v)])
        return hashcode


if __name__ == '__main__':
    docstore = DocStore()
    str1 = ['add {"id":1,"last":"Doe","first":"John","location":{"city":"Oakland","state":"CA","postalCode":"94607"},"active":true}', 'add {"id":2,"last":"Doe","first":"Jane","location":{"city":"San Fransicso","state":"CA","postalCode":"94105"},"active":true}', 'add {"id":3,"last":"Black","first":"Jim","location":{"city":"Spokane","state":"WA","postalCode":"99207"},"active":true}', 'add {"id":4,"last":"Frost","first":"Jack","location":{"city":"Seattle","state":"WA","postalCode":"98204"},"active":false}', 'get {"location":{"state":"WA"},"active":true}', 'get {"id":1}']
    for req in str1:
        docstore.request(req)
