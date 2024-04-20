from calculator import Calculator

def main():
    unwanted_item = [" ", "+"]
    while True:
        print("\nGauss-Jacopy and Gauss-Seidel calculator!\n")
        equation1 = [
            item for item in [*input("equation1: ")] if item not in unwanted_item
        ]
        equation2 = [
            item for item in [*input("equation2: ")] if item not in unwanted_item
        ]
        equation3 = [
            item for item in [*input("equation3: ")] if item not in unwanted_item
        ]
        try:
            matrix = Calculator(matrix=[equation1, equation2, equation3])
        except Exception:
            print("\n[ERROR] Invalid input.")
            continue
        else:
            matrix.start_calculations()
            response = input("\nwould you like to go again? Y or N: ").upper()
            if response == "Y":
                continue
            elif response == "N":
                break
            else:
                print("\ninvalid input")
                on = False
        print("\nProgram closed\n")


if __name__ == "__main__":
    main()
