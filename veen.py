a=[1,3,5]
b=[1,3,4]
c=[5,3,2]
inte = list(set(a) & set(b) -  set(c))
print(inte)