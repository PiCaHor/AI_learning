# print("hello world!")
#
# '''
# This is a annotation
# '''
#
# message = 'Hello world'
# print(message)
#
# # message = input("input test text\n")
# # print(message)
#
# print(5+3)
# print(10-2)
# print(2*4)
# print(16/2)
# print(2**3)
#
# message = 'A said,"Python is good."'
# print(message)
#
# s = 0
# for i in range(2, 100, 2):
#     s += i
# print(s)
#
# a = sum(range(1, 100))
# print(a)
#
# ma1 = [[1, 1, 1], [2, 2, 2]]
# ma2 = [[3, 3, 3], [4, 4, 4], [5, 5, 5]]
# ma4 = []
# for i in range(2):
#     ma3 = []
#     for j in range(3):
#         tmp = 0
#         for k in range(3):
#             tmp += ma1[i][k] * ma2[k][j]
#         ma3.append(tmp)
#     ma4.append(ma3)
# print(ma4)
#
# cities = {
#     'a': {
#         'country': 'C',
#         'population': 100,
#         'fact': 1,
#     },
#     'b': {
#         'country': 'A',
#         'population':200,
#         'fact': 2,
#     },
#     'c': {
#         'country': 'E',
#         'population': 300,
#         'fact': 3,
#     },
# }
# print(cities)
a = 1
print(id(a), type(a))
a = 2
print(id(a), type(a))
a = "aaa"
print(id(a), type(a))
a = 'bbb'
print(id(a), type(a))
b = [1, 2, 3]
a = (1, 2, b)
print(id(a), type(a))
b[1] = 'aaa'
print(id(a), type(a))
a = [1, 2, 3]
print(id(a), type(a))
a.append(4)
print(id(a), type(a))
a = {1:2}
print(id(a), type(a))
a[3] = 4
print(id(a), type(a))
