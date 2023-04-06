# 接收两个值（新的差分和差分列表），突然降低返回 true
def find_sudden_drop(diff, diff_list = []):
    # 计算现有列表的平均值
    if len(diff_list) == 0:
        average = diff
    else:
        average = sum(diff_list) / len(diff_list)

    # 如果新加入列表的数字小于特定值，帧间差分突然降低，有可能匹配到了样本
    if diff < average * 0.1:
        return True
    else:
        diff_list.append(diff)
        # Keep track of the last 10 numbers
        if len(diff_list) > 10:
            diff_list = diff_list[-10:]
        return False

#
# numbers = []
#
# while True:
#     # Receive a new number
#     new_number = int(input("Enter a number: "))
#
#     # Add the number to the list
#     numbers.append(new_number)
#
#     # Check for a sudden drop
#     sudden_drop = find_sudden_drop(numbers)
#     if sudden_drop is not None:
#         print("Sudden drop detected at", sudden_drop)
