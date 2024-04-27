from calculator import Calculator

def main():
    unwanted_item = [" ", "+"]
    while True:
        print("\nGauss-Jacopy, Gauss-Seidel, and Relaxation calculator!\n")
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
            print("\ntesting if the matrix is diagonally dominant.")
            result = matrix.test_diagonal_dominance()
            if result:
                matrix.view_matrix()
                jacopy = matrix.gauss_jacopy()
                seidel = matrix.gauss_seidel()
                relaxation = matrix.relaxation()
                print("\nthe matrix is diagonally dominant, what method would you like to use?")
                while True:
                    print("\n(GJ) for Gauss-Jacopy Method\n(GS) for Gauss-Seidel Method\n(RS) for Relaxation Method\n(C) for comparison\n(E) to go back")
                    response = input("\ninput: ").upper()
                    if response == "GJ":
                        print(f"\nGauss-Jacopy Method\nnumber of iterations: {jacopy[0]}\n{jacopy[1]}\nResult: x = {jacopy[2]}, y = {jacopy[3]}, z = {jacopy[4]}\n")
                    elif response == "GS":
                        print(f"\nGauss-Seidel Method\nnumber of iterations: {seidel[0]}\n{seidel[1]}\nResult: x = {seidel[2]}, y = {seidel[3]}, z = {seidel[4]}\n")
                    elif response == "RS":
                        print(f"\nRelaxation Method\nnumber of iterations: {relaxation[0]}\n{relaxation[1]}\nTOTAL: x = {relaxation[2]}, y = {relaxation[3]}, z = {relaxation[4]}\n")
                    elif response == "C":
                        matrix.view_ranking()
                    elif response == "E":
                        break
                    else:
                        print("[ERROR] invalid input.")  
            else:
                matrix.view_matrix()
                print(
                    "\nthe matrix is not diagonally dominant, the program will use Cramers-Rule."
                )
                cr = matrix.cramers_rule()
                if type(cr) != bool:
                    print(f"\nCramers-Rule\nResult: x = {cr[0]}, y = {cr[1]}, z = {cr[2]}\n")
            
            response = input("\nwould you like to go again? Y or N: ").upper()
            if response == "Y":
                continue
            elif response == "N":
                break
            else:
                print("\n[ERROR] invalid input")
        print("\nProgram closed\n")


if __name__ == "__main__":
    main()
