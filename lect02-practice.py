# # P1、循环打印输出1-100的所有奇数
# for i in range(1, 101):
#     if i % 2 == 1:
#         print(i)

# # P2、字符串替换
# input_str = '你好$$$我正在学 Python@#@#现在需要&*&*&修改字符串'
# input_replace = input_str.replace('$$$', ' ').replace('@#@#', ' ').replace('&*&*&', ' ')
# print(input_replace)

# P3、输出9*9乘法口诀
# # i代表的是行的值
# # for i in range(1, 10):
# #     for j in range(1, i+1):
# #         print('{}*{}={}\t'.format(j, i, i*j), end='')
# #         if i == j:
# #             print()

# P4、奖金发放
# input_interest = int(input('请输入奖金金额：'))
#
# input_interest = input_interest/100000
#
# if input_interest <= 1:
#     input_bonus = input_interest * 0.1
# elif 1 < input_interest <= 2:
#     input_bonus = 1 * 0.1 + (input_interest - 1) * 0.075
# elif 2 < input_interest <= 4:
#     input_bonus = 1*0.1 + 1*0.075 + (input_interest - 2)*0.05
# elif 4 < input_interest <= 6:
#     input_bonus = 1 * 0.1 + 1 * 0.075 + 2 * 0.05 + (input_interest - 4) * 0.03
# elif 6 < input_interest <= 10:
#     input_bonus = 1 * 0.1 + 1 * 0.075 + 2 * 0.05 + 2 * 0.03 + (input_interest - 6) * 0.15
# elif input_interest > 10:
#     input_bonus = 1 * 0.1 + 1 * 0.075 + 2 * 0.05 + 2 * 0.03 + 4 * 0.15 + (input_interest - 10) * 0.01
#
# print(input_bonus * 100000)

# # P5、字典值排序
# from operator import itemgetter
#
# dict_a = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
#
# print(dict_a.items())
# # 对字典排序是不可能的，只有把字段转化成另一种方式才能排序。字典本身是无序的，但是如列表元组等其他类型是有序的
# s_dict_a = sorted(dict_a.items(), key=itemgetter(1))
# print(s_dict_a)


class Person:
    name = []


p1 = Person()
p2 = Person()

p1.name.append(1)
print(p1.name)
print(p2.name)
print(Person.name)
