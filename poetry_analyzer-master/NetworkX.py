import networkx as nx
import numpy as np
import pylab
f=open('./static/link_txt_pre')
link_txt_pre=f.readlines()
f=open('./static/link_txt_next')
link_txt_next=f.readlines()
f=open('./static/data_txt')
data_txt=f.readlines()
for i in range(1,np.size(link_txt_next)-1):
    for j in range(1,np.size(data_txt)-1):
        if(link_txt_next[i]==data_txt[j]):
            link_txt_next[i]=j
for i in range(1,np.size(link_txt_pre)-1):
    for j in range(1,np.size(data_txt)-1):
        if(link_txt_pre[i]==data_txt[j]):
            link_txt_pre[i]=j
link_txt_next=np.array(link_txt_next)
link_txt_pre=np.array(link_txt_pre)
# print(link_txt_pre)
# print(link_txt_next)
G=nx.Graph()
for i in range(1,np.size(data_txt)-2):
    G.add_node(i)
for j in range(1,np.size(link_txt_pre)-2):
    G.add_edge(link_txt_pre[j],link_txt_next[j])

density=nx.degree(G)
print(density)
