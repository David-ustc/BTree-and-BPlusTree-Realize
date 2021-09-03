import random
import numpy as np
# import BloomFilter as BF
import BF_mmh as bf

k=128
hash_count = 10

def keygen(k):
    '''
    ##### 输入参数k，返回密钥sk
    :param k: 随机矩阵的维度
    :return: sk=(M1,M2,S)
    '''
    M1=np.random.randint(0,2,[k,k])
    M2=np.random.randint(0,2,[k,k])
    S=np.random.randint(0,2,[k])
    sk = [M1,M2,S]

    return sk

def Encode(string):
    substring = []
    substring.append(string+"$")
    substring.append("$"+string) # $[0,len-1]  [0,len-1]$
    for i in range(1, len(string)):  # [0,1),[0,2),[0,3),...,[0,len-1)
        s1 = string[0:i] + "$"
        s2 = "$" + string[i:]
        substring.append(s1)
        substring.append(s2)

    return substring

def BuildIndex(k, sk, Lib):
  
    B = [bf.BloomFilter(k, hash_count) for i in range(len(Lib))]

    for i, val in enumerate(Lib):
        substring = Encode(val)
        for s in substring:
            B[i].add(s)  

    S = sk[2]  #提取私钥中的S
    r = random.randint(1,10) # 生成一个随机数

    b_P=[]
    b_PP=[] 
    I=[]  # 索引
    for i,b in enumerate(B):
        b = list(b)
        for j,vals in enumerate(S):
            if vals==1:
                b_jp=b_jpp=int(b[j])  # b_j'=b_j''=b_j ,v是第i个bloomfilter
                b_P.append(b_jp)
                b_PP.append(b_jpp)
            else:
                b_jp = 0.5*int(b[j])+r
                b_jpp = 0.5*int(b[j])-r
                b_P.append(b_jp)
                b_PP.append(b_jpp)

        I_iP = np.inner(np.transpose([sk[0]]).reshape((k, k)), b_P) # 将M1矩阵转置后与B'点乘
        I_iPP = np.inner(np.transpose([sk[1]]).reshape((k, k)), b_PP) # 将M2矩阵转置后与B''点乘
        I_i = [I_iP,I_iPP]
        I.append(I_i)
        b_PP = []  
        b_P = []

    return I, B

def Trapdoor(k, sk, Q):

    b = bf.BloomFilter(k, hash_count)
    
    substring = ["$"+Q, Q+"$"]
    b.add(substring[0])
    b.add(substring[1])
    S = sk[2]  
    r = random.randint(1, 10)  
    b_P = []
    b_PP = []

    b_t = list(b)
    for j,vals in enumerate(S):
        if vals==0:
            b_jp=b_jpp=int(b_t[j])  
            b_P.append(b_jp)
            b_PP.append(b_jpp)
        else:
            b_jp = 0.5*int(b_t[j])+r
            b_jpp = 0.5*int(b_t[j])-r
            b_P.append(b_jp)
            b_PP.append(b_jpp)

    T_P = np.inner(np.linalg.inv([sk[0]]).reshape((k, k)), b_P) 
    T_PP = np.inner(np.linalg.inv([sk[1]]).reshape((k, k)), b_PP)  
    t=[T_P,T_PP]
    return t

def Search(I, t, Lib):
    for i, I_i in enumerate(I):
        I_iP = I_i[0]  # I_i'
        I_iPP =  I_i[1] # I_i''
        Ri = np.inner(I_iP,t[0])+np.inner(I_iPP,t[1])
        print(Ri, Lib[i])


if __name__ == '__main__':
    query = "qwertyu00"

    sk=keygen(k)
    StringLib = []
    f=open('data/trgm.txt')
    for line in f:
        StringLib.append(line.strip())
    Index, BFilter = BuildIndex(k, sk, StringLib)
    for i, b in enumerate(BFilter):
        if query+"$" in b:
            print(StringLib[i])

    trap = Trapdoor(k, sk, query)
    Search(Index, trap, StringLib)
