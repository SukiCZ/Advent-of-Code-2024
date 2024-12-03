def main():
    input_file = "../input.txt"
    with open(input_file, "r") as file:
        list_1, list_2 = [], []
        result = 0
        # Read file to list variables
        for line in file:
            one, two = line.split()
            list_1.append(int(one))
            list_2.append(int(two))
        # Sort the lists
        list_1.sort()
        list_2.sort()
        # Calculate the result
        for one, two in zip(list_1, list_2):
            result += abs(one - two)
        print(f"The result is: {result}")


if __name__ == "__main__":
    main()
