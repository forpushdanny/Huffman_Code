# coding=utf-8

import collections
import heapq

'''
    109 資訊學分班作業
    1. 測試資料檔test3.txt輸入字串
    2. 字串代表每一個字元出現的頻率
    3. 字元不一定依序排列，大小寫視為相同字元
        範例： adgbbcddadddeeeeeffggggaghhhhiii
        其中a出現3次，b出現2次，... 
    4. 輸出：
        A.每一字元對應的頻率(出現次數)
        B.編碼
        C.與編碼長度  
'''

def read_data():
    try:
        read_file = open('test3.txt', 'r')
    except:
        print("讀取 test3.txt 錯誤")
    read_data = read_file.read()
    #全部轉成小寫字母 lower()
    mydata = read_data.lower()
    return mydata
    
class Tree_node:
    def __init__(self, value=None, count=1, left=None, right=None, code =''):
        self.value = value
        self.count = count
        self.left = left
        self.right = right
        self.code= code
    def is_leaf(self):
        #測試是否有左右子節點，沒有的話就是葉子
        return not(self.left or self.right)
    def __lt__(self, other):
        # 擴充 '<' 符號的功能
        return self.count < other.count
    def __add__(self, other):
        #擴充 '+' 符號的功能
        self.code = 0
        other.code = 1
        return Tree_node(None, self.count + other.count, self, other )

def convert_huffman_tree_to_code(node, prefix=[]):
    """將樹轉成編碼."""
    code = {}
    if node:
        prefix = prefix + [node.code]
        if node.is_leaf():
            code[node.value] = prefix
        else:
            code.update(convert_huffman_tree_to_code(node.left, prefix))
            code.update(convert_huffman_tree_to_code(node.right, prefix))
    return code

def huffman_code(mydata):
    #計算每個字母出現的次數 
    char_counts = collections.Counter(mydata)
    #建立節點
    tree_nodes = [Tree_node(item, count) for item, count in char_counts.items()]
    #將節點tree_nodes轉成堆積 heap
    heapq.heapify(tree_nodes)

    while len(tree_nodes)>=2:
        heapq.heappush(tree_nodes, heapq.heappop(tree_nodes)+heapq.heappop(tree_nodes))
        
    huffman_tree = tree_nodes[0]
    code= convert_huffman_tree_to_code(huffman_tree)
    return char_counts, code

def huffman_encrypt(mydata, code):
    #將傳入字串編碼
    encrypted=[]
    for char in mydata:
        encrypted.extend(code[char])
    encrypted_text = "".join(str(ch) for ch in encrypted)
    return encrypted_text

def huffman_test():
    mydata=read_data()
    char_counts, code = huffman_code(mydata)
    #將字串編碼
    encrypted_text = huffman_encrypt(mydata, code)
    output(mydata, char_counts, code, encrypted_text)
    
def output(mydata, char_counts, code, encrypted_text):
    
    myitem = {}
    for item,count in char_counts.items():
        myitem[item]=count
    keysorted = sorted(myitem.keys())
    print('每一字元對應的頻率(出現次數):')
    for key in keysorted:
        print("  {} : {}".format(key, myitem[key]))

    print()
    print('編碼表:')
    #code 是 tuple格式，例如：'g':['',0,0]
    for co in code:
        print('  {} : {}'.format(co,code[co][1:]))

    print()
    print('原文:{}'.format(mydata))
    print('編碼後:{}'.format(encrypted_text))
    print('編碼長度:{}'.format(str(len(encrypted_text))))
    
        
        
        
    
    




if __name__ == "__main__":
    huffman_test()