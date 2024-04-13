import pandas as pd
import tabulate as tbl

class JacopySeidel:
    def __init__(self, matrix) -> None:
        """
        constructs the matrix.
        """
        self.__matrix = []
        self.__jacopy_counter = 0
        self.__seidel_counter = 0
        self.__use_jacopy = False
        self.__use_seidel = False
        self.compare = False
        self.__gjdata = [[], [], [], []]
        self.__gsdata = [[], [], [], []]
        for array in matrix:
            right_side = ""
            sign_collector = ""
            n_before_variable = ""
            arr = []
            for n in array:
                if n == "-":
                    sign_collector = n
                    continue
                elif n == "=":
                    arr_i = array.index(n)
                    for n in range(arr_i+1, len(array)):
                        right_side += str(array[n])
                    break
                try: 
                    int(n)
                except Exception:
                    if n_before_variable == "":
                        arr.append(int(f"{sign_collector}{1}"))
                        sign_collector = ""
                    else:
                        n_before_variable = ""
                else:
                    arr.append(int(f"{sign_collector}{n}"))
                    sign_collector = ""
                    n_before_variable = f"{n}"
            arr.append(int(right_side))
            self.__matrix.append(arr)
            
            
    def view(self) -> None:
        """
        views the equation in matrix form
        """
        print("\nyour equation convert into matrix:")
        n = 0
        letters = ["x", "y", "z"]
        for arr in self.__matrix:
            print(f"{arr[:-1]} [{letters[n]}] = {[arr[3]]}")
            n +=1
    def test_diagonally_dominant(self) -> None:
        """
        tests whether the matrix is diagonally dominant.
        """
        print("\ntesting if the matrix is diagonally dominant.")
        diagonal_item = 0
        counter = 0
        for arr in self.__matrix:
            arr = arr[:-1]
            sum = 0
            for item in arr:
                if arr[diagonal_item] == item:
                    continue
                sum += abs(item)
            if arr[diagonal_item] > sum:
                counter += 1
            diagonal_item += 1
        if counter == 3:
            on = True
            while on:
                response = input("\nthe matrix is diagonally dominant, what method would you like to __use?\ntype (GJ) for gauss-jacopy and (GS) for gauss-seidel\n").upper()
                if response == "GJ":
                    on = False
                    self.compare = True
                    self.__use_seidel = True
                    return self.__gauss_jacopy()
                elif response == "GS":
                    on = False
                    self.compare = True
                    self.__use_jacopy = True
                    return self.__gauss_seidel()
                else:
                    print("invalid input.")
        else:
            print("\nthe matrix is not diagonally dominant, the program will __use Gauss-Seidel.")
            return self.__gauss_seidel()
             
             
    def __gauss_seidel(self) -> str:
        """
        performs Gauss-Seidel method
        """
        if not self.__use_seidel:
            print("\nusing Gauss-Seidel...")
        x, y, z = 0, 0, 0
        arr_x  = self.__matrix[0]
        arr_y = self.__matrix[1]
        arr_z = self.__matrix[2]
        sx, sy, sz = 0, 0, 0
        while True:
            self.__write_to_table(data=self.__gsdata, index=self.__seidel_counter, values=[x, y, z])
            new_x = round((arr_x[3] - (arr_x[1] * y) - (arr_x[2] * z))/arr_x[0], 3)
            x = new_x
            new_y = round((arr_y[3] - (arr_y[0] * x) - (arr_y[2] * z))/arr_y[1], 3)
            y = new_y
            new_z = round((arr_z[3] - (arr_z[0] * x) - (arr_z[1] * y))/arr_z[2], 3)
            z = new_z
            if self.__seidel_counter > 100:
                return f"\nthis system of linear equation doesn't or takes time to converge, the program will use Cramer's Rule instead.\n{self.__cramers_rule()}"
            if (sx, sy, sz) == (x, y, z):
                break
            else:
                self.__seidel_counter += 1
                sx, sy, sz = x, y, z
        if self.__use_jacopy:
            self.__gauss_jacopy()
        return f"\nResult: x = {x}, y = {y}, z = {z}\nnumber of iterations: {self.__seidel_counter+1}\n{self.__show_iteration_table(data=self.__gsdata)}"
            

    def __gauss_jacopy(self) -> str:
        """
        Performs Gauss-Jacopy method
        """
        if not self.__use_jacopy:
            print("\nusing Gauss-Jacopy...")
        x, y, z = 0, 0, 0
        arr_x  = self.__matrix[0]
        arr_y = self.__matrix[1]
        arr_z = self.__matrix[2]
        while True:
            self.__write_to_table(data=self.__gjdata, index=self.__jacopy_counter, values=[x, y, z])
            new_x = round((arr_x[3] - (arr_x[1] * y) - (arr_x[2] * z))/arr_x[0], 3)
            new_y = round((arr_y[3] - (arr_y[0] * x) - (arr_y[2] * z))/arr_y[1], 3)
            new_z = round((arr_z[3] - (arr_z[0] * x) - (arr_z[1] * y))/arr_z[2], 3)
            if self.__jacopy_counter > 100:
                return f"\nthis system of linear equation doesn't or takes time to converge, the program will use Cramer's Rule instead.\n{self.__cramers_rule()}"
            if (new_x, new_y, new_z) == (x, y, z):
                break
            else:
                self.__jacopy_counter += 1
                x, y, z = new_x, new_y, new_z
        
        if self.__use_seidel:
            self.__gauss_seidel()
        return f"\nResult: x = {x}, y = {y}, z = {z}\nnumber of iterations: {self.__jacopy_counter+1}\n{self.__show_iteration_table(data=self.__gjdata)}"
    
    def __cramers_rule(self):
        """
        performs Cramer's Rule
        """
        denominator = self.__determinant(self.__matrix)

        numerator_x = self.__determinant([
            [self.__matrix[0][3], self.__matrix[0][1], self.__matrix[0][2]],
            [self.__matrix[1][3], self.__matrix[1][1], self.__matrix[1][2]],
            [self.__matrix[2][3], self.__matrix[2][1], self.__matrix[2][2]]
            ])
        
        numerator_y = self.__determinant([
            [self.__matrix[0][0], self.__matrix[0][3], self.__matrix[0][2]],
            [self.__matrix[1][0], self.__matrix[1][3], self.__matrix[1][2]],
            [self.__matrix[2][0], self.__matrix[2][3], self.__matrix[2][2]]
            ])

        numerator_z = self.__determinant([
            [self.__matrix[0][0], self.__matrix[0][1], self.__matrix[0][3]],
            [self.__matrix[1][0], self.__matrix[1][1], self.__matrix[1][3]],
            [self.__matrix[2][0], self.__matrix[2][1], self.__matrix[2][3]]
            ])
        
        x = round(numerator_x/denominator, 3)
        y = round(numerator_y/denominator, 3)
        z = round(numerator_z/denominator, 3)
    
        return f"\nx = {x}, y = {y}, z = {z}"
    
    def __determinant(self, matrix):
        """
        finds the determinant of a matrix.
        """
        result = (
            (matrix[0][0]*((matrix[1][1]*matrix[2][2])-(matrix[2][1]*matrix[1][2]))) 
            - (matrix[0][1]*((matrix[1][0]*matrix[2][2])-(matrix[2][0]*matrix[1][2]))) 
            + (matrix[0][2]*((matrix[1][0]*matrix[2][1])-(matrix[2][0]*matrix[1][1])))
            )
        return result
    
    
    def method_comparison(self):
        """
        compares the two methods.
        """
        if self.__jacopy_counter < self.__seidel_counter:
            print("comparison: The Gauss-Jacopy method is more efficient than the Gauss-Seidel method.")
            response = input("Would you like to see the other table? Y or N: ").upper()
            if response == "Y":
                if self.__use_jacopy == True:
                    print(f"\niterations: {self.__jacopy_counter+1}")
                    print(self.__show_iteration_table(self.__gjdata))
                elif self.__use_seidel == True:
                    print(f"\niterations: {self.__seidel_counter+1}")
                    print(self.__show_iteration_table(self.__gsdata))
                    
        elif self.__seidel_counter < self.__jacopy_counter:
            print("comparison: The Gauss-Seidel method is more efficient than the Gauss-Jacopy method.")
            response = input("Would you like to see the other table? Y or N: ").upper()
            if response == "Y":
                if self.__use_jacopy == True:
                    print(f"\niterations: {self.__jacopy_counter+1}")
                    print(self.__show_iteration_table(self.__gjdata))
                elif self.__use_seidel == True:
                    print(f"\niterations: {self.__seidel_counter+1}")
                    print(self.__show_iteration_table(self.__gsdata))
                    
        else:
            print("comparison: Both of the methods are efficient for this system of linear equations.")
            

    def __write_to_table(self, data, index, values):
        """
        writes the values for the iteration table.
        """
        data[0].append(index)
        data[1].append(values[0])
        data[2].append(values[1])
        data[3].append(values[2])
    
    def __show_iteration_table(self, data):
        """
        shows the iteration table.
        """
        arr = {"iteration": data[0], "x": data[1], "y": data[2], "z": data[3]}
        df = pd.DataFrame(arr)
        table = tbl.tabulate(df, headers='keys', tablefmt="grid", showindex=False)
        return table
            
