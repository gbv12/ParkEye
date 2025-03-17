#coding:utf-8
lst=['A','B','D','D','D']
#lst=['A','B','D','E','D']
for item in lst:
    if 'D' in lst: # in与索引没有关系，不会关注列表的长度变量
        lst.remove('D')
    # if item=='D':
    #     lst.remove(item)
print(lst)
# lt=['asd','ads','wer']
# #lambda 的作用是将列表中的小写转成大写
# x=map(lambda x: x.upper(), lt)
# print(list(x))






