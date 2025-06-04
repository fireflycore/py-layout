def learList():
    l1 = [1, 2, 3]
    print(l1)
    # 列表尾部添加一项
    l1.append(4)
    print(l1)
    # 列表尾部扩展l2
    l2 = [5, 6, 7]
    l1.extend(l2)
    print(l1)
    # 删除第一个值为1的元素
    l1.remove(1)
    print(l1)
    # 移除列表中给定位置的元素，并返回该元素
    tl = l1.pop(1)
    print(tl)
    print(l1)


learList()
