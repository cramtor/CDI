#!/usr/bin/python3


from math import log2, ceil


'''
transform_as_frq transform 'src' in freq mode
'''
def transform_as_frq(src):
    total = 0;
    for x,y in src:
        total += y

    frq_aux = [];
    for x,y in src:
        frq_aux.append((x,y/total))

    return frq_aux
'''
COMPUTATION OF entropy_source
'''
def entropy_source(src):
    ent = 0.0;
    for x,y in src:
        ent += y * log2(1.0/y)

    return ent
'''
CREATION OF SOURCES
'''
def source_fromstring(mystr):
    aux = {}
    for x in mystr:
        if x in aux.keys():
            aux[x] += 1
        else:
            aux[x] = 1

    src = []
    for x in aux:
        src.append((x, aux[x]))
    return src

def source_extension(src, k):
    if k == 1:
        return src

    src_extended = []
    for x,y in src:
        for w,z in src:
            src_extended.append((x+w,round(y*z,10)))
            #print(src_extended)

    return source_extension(src_extended,k-1)

def sumbin1(bit,string):
    aux = list(string)
    bitAux = len(aux)-1-bit
    if aux[bitAux] == '0':
        aux[bitAux] = '1'
        return "".join(aux)
    else:
        aux[bitAux] = '0'
        return sumbin1(bit+1,"".join(aux))

'''
SOURCE CODING
'''

from collections import Counter
def functord(comm,chainaux,src):

    slist = [chainaux]
    for x in range(len(comm)-2,-1,-1):
        charac, length = comm[x]        
        chainaux = sumbin1(0,chainaux)
        diff = length - len(chainaux)
        chainaux += '0'*diff
        slist.append(chainaux)
    return slist
    
def funct2ord(comm,slist,src):
    mnsize = 0
    ult = []
    for x in range(len(src)):
        charac,p=src[x]
        for y in range(len(comm)):
            w,_ = comm[y]
            if charac == w:
                ult.append(slist[y])
                mnsize += p*len(slist[y])
                break
    return ult,round(mnsize,10)

def shannon_code(src):
    if len(src) == 0:
        return [],0
    lengthSrc = []
    frq = Counter()
    for x,y in src:
        #lengthSrc.append((x,ceil(log2(1.0/y))))
        lengthSrc += (x,ceil(log2(1.0/y)))
        frq[x] = ceil(log2(1.0/y))
    comm = frq.most_common()
    firstletter, firstLength = comm[len(comm)-1]
    chainaux = '0'*firstLength
    slist = functord(comm,chainaux,src)
    slist.reverse()
    ult = funct2ord(comm,slist,src)
    return ult



def funct_rec(src):
    if len(src) <= 1:
        return [""]

    count = Counter()
    total = 0.0
    for x,y in src:
        count[x] = y
        total += y
    comm = count.most_common()
    x,y = comm[0]
    chainaux = y
    sub_src_l = [(x,y)]
    sub_src_r = []

    for n in range(1,len(comm)):
        x,y = comm[n]
        last = chainaux
        chainaux += y
        if chainaux < total/2.0:
            sub_src_l.append((x,y))
        elif chainaux > total/2.0 and last < total/2.0:
            if total/2 - last < chainaux - total/2:
                sub_src_r.append((x,y))
            else:
                sub_src_l.append((x,y))
        else:
            sub_src_r.append((x,y))

    left = funct_rec(sub_src_l)
    right = funct_rec(sub_src_r)
    ulty = []
    for x in left:
        ulty.append('0'+x)
    for x in right:
        ulty.append('1'+x)

    return ulty


def shannon_fano_code(src):

    aux = funct_rec(src)

    c = Counter()
    for i,j in src:
        c[i] = j
    comm = c.most_common()
    mnsize = 0

    result = []
    for n in range(len(src)):
        i, j = src[n]
        for m in range(len(comm)):
            k,z = comm[m]
            if i == k:
                result.append(aux[m])
                mnsize += z*len(aux[n])
                break

    return result, round(mnsize,10)


class Tree(object):
    def __init__(self, charac, prob):
        self.left = None
        self.right = None
        self.charac = charac
        self.prob = prob
        self.depth = 0

    def __repr__(self):
        return "charac: \""+self.charac+"\" w/ prob: "+str(round(self.prob,10))+(' Left '+self.left.charac if self.left != None else '')+(' Right '+self.right.charac if self.right != None else '')+ '\n'

    def __str__(self):
        return self.charac+' '+str(round(self.prob,10))

def huffman_tree(tree):
    if tree.left == None and tree.right == None:
        return [('',tree.prob, tree.charac)]

    l = []
    if tree.right != None:
        huff_tr_rec = huffman_tree(tree.right)
        for word,prob,charac in huff_tr_rec:
            l.append(('0'+word, prob, charac))
    if tree.left != None:
        huff_tr_rec = huffman_tree(tree.left)
        for word,prob,charac in huff_tr_rec:
            l.append(('1'+word, prob, charac))

    return l

def huffman_code(src):
    count = Counter()
    for x,y in src:
        count[x] = y
    comm = count.most_common()
    treeList = []
    for n in range(len(comm)-1,-1,-1):
        x, y = comm[n]
        t = Tree(x,y)
        treeList.append(t)
    i = 0
    while i+1 < len(treeList):
        p = treeList[i].prob+treeList[i+1].prob
        t = Tree('-'+treeList[i].charac+'+'+treeList[i+1].charac,p)
        if treeList[i].depth >= treeList[i+1].depth:
            t.left = treeList[i]
            t.right = treeList[i+1]
        else:
            t.left = treeList[i+1]
            t.right = treeList[i]
        t.depth = max(t.left.depth,t.right.depth)+1
        if p >= 1:
            treeList.insert(len(treeList),t)
            break
        inserted = False
        for x in range(i,len(treeList)):
            if p < treeList[x].prob:
                treeList.insert(x, t)
                inserted = True
                break
        if not inserted:
            treeList.insert(len(treeList),t)
        i += 2

    ht = huffman_tree(treeList[len(treeList)-1])

    huffman_c = []
    mnsize = 0
    for x,y in src:
        for w,p,l in ht:
            if x == l:
                mnsize += len(w)*p
                huffman_c.append(w)

    return huffman_c, round(mnsize,10)


src_code = [("0",18), ("1",2)]

#src_code = [("a",3), ("1",5), ("2",9), ("3",11), ("4",14), ("5",19), ("6",33), ("7",44), ("8",62)]

#src_code = [("a",0.05), ("d",0.05), ('e',0.2), ('f',0.025), ('h',0.075), ('j',0.1),('m',0.025),('n',0.125),('p',0.025),('s',0.05),('t',0.15),('u',0.1),('z',0.025)]

#src_code = [("a1",0.36),("a2",0.18),("a3",0.18),("a4",0.12),("a5",0.09),("a6",0.07)]

#src_code = [("A",15),("B",7),("C",6),("D",6),("E",5)]  

print("Encoding with Shannon ->         ",shannon_code(source_extension(transform_as_frq(src_code),2)))

print("Encoding with Shannon Fano ->    ",shannon_fano_code(source_extension(transform_as_frq(src_code),2)))

print("Encoding with Huffman ->         ", huffman_code(source_extension(transform_as_frq(src_code),2)))
#print(src_code)
#print(source_extension(transform_as_frq(src_code),2))
#print (transform_as_frq(src_code))

print(huffman_code(transform_as_frq(src_code)))

# print (entropy_source (source_extension(transform_as_frq(([("0",18), ("1",2)])),2)))

print (entropy_source(source_fromstring("00000010000000000100")))

# print ((source_extension(transform_as_frq([("0",0.9), ("1",0.1)]), 2)))