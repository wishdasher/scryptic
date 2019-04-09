digits = raw_input("Enter four digits: ")
match = dict((el, False) for el in range(100))
nums = [int(x) for x in list(digits)]
print("Finding solutions for: " + str(nums))


