# 定义函数
def main():
    # 列表（List）
    l = [1, 2, 3]
    # 字典（Dict）
    d = {"name": "张三", "gender": 1, "age": 30}
    # 集合（Set）
    s = {1, 2, 3}

    # 遍历列表
    for idx, item in enumerate(l):
        print(idx, item)

    # 遍历字典
    for k, v in d.items():
        print(k, v)

    # 遍历集合
    for i in s:
        print(i)


main()
