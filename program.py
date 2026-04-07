num = int(input())
nums = []
nums.append(num)
while num != 0:
    num = int(input())
    if num != 0:
        nums.append(num)
count = 0
for num in nums:
    if num % 14 == 0:
        count += 1
print(count)