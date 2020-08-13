largest = None
smallest = None

while True:
    inp = input("Enter a number: ")
    if inp == "done":
        break
    try:
        num = int(inp)
    except:
        print("Invalid input!")
        continue
    if (smallest is None) or (num < smallest):
        smallest = num
    if (largest is None) or (num > largest):
        largest = num

print("Maximum is", largest)
print("Minimum is", smallest)
