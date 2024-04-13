from jacopyseidel import JacopySeidel as js
        
def main():
    on = True
    unwanted_item = [" ", "+"]
    while on:
        print("\nGauss-Jacopy and Gauss-Seidel calculator!\n")
        equation1 = [item for item in [*input("equation1(x): ")] if item not in unwanted_item]
        equation2 = [item for item in [*input("equation2(y): ")] if item not in unwanted_item]
        equation3 = [item for item in [*input("equation3(z): ")] if item not in unwanted_item]
        matrix = js([equation1, equation2, equation3])
        matrix.view()
        result = matrix.test_diagonally_dominant()
        print(result)
        if matrix.compare:
            matrix.method_comparison()
        response = input("\nwould you like to go again? Y or N: ").upper()
        if response == "Y":
            continue
        elif response == "N":
            on = False
        else:
            print("invalid input")
            on = False
    print("Program closed")
           
            
if __name__ == "__main__":
    main()




