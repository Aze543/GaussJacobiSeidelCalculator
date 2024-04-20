import pandas as pd
import tabulate as tbl
from numpy import argsort


class Calculator:
    def __init__(self, matrix) -> None:
        """
        constructs the matrix.
        """
        self.__matrix = []
        self.__jacopy_counter = 0
        self.__seidel_counter = 0
        self.__relaxation_counter = 0
        self.__gjdata = [[], [], [], []]
        self.__gsdata = [[], [], [], []]
        self.__rsdata = [[], [], [], [], [],[], [], []]
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
                    for n in range(arr_i + 1, len(array)):
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

    def __view(self) -> None:
        """
        views the equation in matrix form
        """
        print("\nyour equation convert into matrix:\n")
        n = 0
        letters = ["x", "y", "z"]
        for arr in self.__matrix:
            print(f"{arr[:-1]} [{letters[n]}] = {[arr[3]]}")
            n += 1
            
    def __test_diagonal(self) -> bool:
        sequence = [[0,1,2], [0,2,1], [1,0,2], [1,2,0], [2,0,1], [2,1,0]]
        diagonal_item = 0
        counter = 0
        p_counter = 1
        for s in sequence:
            matrix = [self.__matrix[s[0]], self.__matrix[s[1]], self.__matrix[s[2]]]
            for arr in matrix:
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
                self.__matrix= matrix
                return True
            elif p_counter == 6:
                return False
            else:
                counter = 0
                p_counter += 1
                diagonal_item = 0

    def start_calculations(self) -> None:
        """
        starts the calcultaions.
        """
        print("\ntesting if the matrix is diagonally dominant.")
        result = self.__test_diagonal()
        if result:
            self.__view()
            jacopy = self.__gauss_jacopy()
            seidel = self.__gauss_seidel()
            relaxation = self.__relaxation()
            print("\nthe matrix is diagonally dominant, what method would you like to use?")
            while True:
                print("\n(GJ) for Gauss-Jacopy Method\n(GS) for Gauss-Seidel Method\n(RS) for Relaxation Method\n(C) for comparison\n(E) to go back")
                response = input("\ninput: ").upper()
                if response == "GJ":
                    print(f"\nGauss-Jacopy Method\nResult: x = {jacopy[0]}, y = {jacopy[1]}, z = {jacopy[2]}\nnumber of iterations: {self.__jacopy_counter}\n{self.__jacopy_seidel_table(data=self.__gjdata)}\n")
                elif response == "GS":
                    print(f"\nGauss-Seidel Method\nResult: x = {seidel[0]}, y = {seidel[1]}, z = {seidel[2]}\nnumber of iterations: {self.__seidel_counter}\n{self.__jacopy_seidel_table(data=self.__gsdata)}\n")
                elif response == "RS":
                    print(f"\nRelaxation Method\n iterations: {self.__relaxation_counter}\n{self.__relaxation_table(self.__rsdata)}\nTOTAL: x = {round(relaxation[0], 3)}, y = {round(relaxation[1], 3)}, z = {round(relaxation[2], 3)}\n")
                elif response == "C":
                    rank = {"Gauss-Jacopy Method": self.__jacopy_counter, "Gauss-Seidel Method": self.__seidel_counter, "Relaxation Method": self.__relaxation_counter}
                    name, counter = list(rank.keys()), list(rank.values())
                    sorted_rank = argsort(counter)
                    print("\nbest method:")
                    [print(f"{i[0]+1}. {name[i[1]]} -> {counter[i[1]]} iterations") for i in enumerate(sorted_rank)]
                elif response == "E":
                    break
                else:
                    print("invalid input.")  
        else:
            print(
                "\nthe matrix is not diagonally dominant, the program will use Cramers-Rule."
            )
            cr = self.__cramers_rule()
            print(f"\nCramers-Rule\nResult: x = {cr[0]}, y = {cr[1]}, z = {cr[2]}\n")

    def __gauss_seidel(self) -> list:
        """
        performs Gauss-Seidel method
        """
        x, y, z = 0, 0, 0
        arr_x = self.__matrix[0]
        arr_y = self.__matrix[1]
        arr_z = self.__matrix[2]
        sx, sy, sz = 0, 0, 0
        while True:
            new_x = round((arr_x[3] - (arr_x[1] * y) - (arr_x[2] * z)) / arr_x[0], 3)
            x = new_x
            new_y = round((arr_y[3] - (arr_y[0] * x) - (arr_y[2] * z)) / arr_y[1], 3)
            y = new_y
            new_z = round((arr_z[3] - (arr_z[0] * x) - (arr_z[1] * y)) / arr_z[2], 3)
            z = new_z
            self.__gjs_to_table(
                data=self.__gsdata, index=self.__seidel_counter, values=[sx,sy, sz]
            )
            if (sx, sy, sz) == (x, y, z):
                break
            else:
                self.__seidel_counter += 1
                sx, sy, sz = x, y, z
                
        return [x, y, z]

    def __gauss_jacopy(self) -> list:
        """
        Performs Gauss-Jacopy method
        """
        x, y, z = 0, 0, 0
        arr_x = self.__matrix[0]
        arr_y = self.__matrix[1]
        arr_z = self.__matrix[2]
        while True:
            self.__gjs_to_table(
                data=self.__gjdata, index=self.__jacopy_counter, values=[x, y, z]
            )
            new_x = round((arr_x[3] - (arr_x[1] * y) - (arr_x[2] * z)) / arr_x[0], 3)
            new_y = round((arr_y[3] - (arr_y[0] * x) - (arr_y[2] * z)) / arr_y[1], 3)
            new_z = round((arr_z[3] - (arr_z[0] * x) - (arr_z[1] * y)) / arr_z[2], 3)
            if self.__jacopy_counter > 100:
                return f"\nthis system of linear equation doesn't or takes time to converge, the program will use Cramer's Rule instead.\n{self.__cramers_rule()}"
            if (new_x, new_y, new_z) == (x, y, z):
                break
            else:
                self.__jacopy_counter += 1
                x, y, z = new_x, new_y, new_z
                
        return [x, y, z]

    def __relaxation(self) -> list:
        x,y,z = 0,0,0
        dx,dy,dz = 0,0,0
        arr_x = self.__matrix[0]
        arr_y = self.__matrix[1]
        arr_z = self.__matrix[2]
        ri_x = max([abs(n) for n in arr_x[:-1]])
        ri_y = max([abs(n) for n in arr_y[:-1]])
        ri_z = max([abs(n) for n in arr_z[:-1]])
        f_x, f_y, f_z = 0,0,0
        letters = ["x", "y", "z"]
        while True:
            r1 = arr_x[3] - (arr_x[0]*x) - (arr_x[1]*y) - (arr_x[2]*z)
            r2 = arr_y[3] - (arr_y[0]*x) - (arr_y[1]*y) - (arr_y[2]*z)
            r3 = arr_z[3] - (arr_z[0]*x) - (arr_z[1]*y) - (arr_z[2]*z)
            arr_x[3] = r1 = round(r1, 4)
            arr_y[3] = r2 = round(r2, 4)
            arr_z[3] = r3 = round(r3, 4)
            if ([round(abs(n), 2) for n in [r1, r2, r3]]) == ([round(abs(n), 2) for n in [dx, dy, dz]]):
                break
            else:
                operation = 0
                for n in enumerate([x,y,z]):
                    if abs(n[1]) != 0:
                        operation = f"d{letters[n[0]]} = {round(n[1], 4)}"
                self.__rs_to_table(data=self.__rsdata, index=self.__relaxation_counter,operation=operation, dx=x, dy=y, dz=z, r1=r1, r2=r2, r3=r3)
                if abs(r1) == max([abs(n) for n in [r1, r2, r3]]):
                    dx = round(r1/ri_x, 4)
                    f_x += dx
                    x, y, z = dx,0,0
                elif abs(r2) == max([abs(n) for n in [r1, r2, r3]]):
                    dy = round(r2/ri_y, 4)
                    f_y += dy
                    x, y, z = 0,dy,0
                elif abs(r3) == max([abs(n) for n in [r1, r2, r3]]):
                    dz = round(r3/ri_z, 4)
                    f_z += dz
                    x, y, z = 0,0,dz
                self.__relaxation_counter += 1
            
        return [f_x,f_y,f_z]

    def __cramers_rule(self) -> list:
        """
        performs Cramer's Rule
        """
        denominator = self.__determinant(self.__matrix)

        numerator_x = self.__determinant(
            [
                [self.__matrix[0][3], self.__matrix[0][1], self.__matrix[0][2]],
                [self.__matrix[1][3], self.__matrix[1][1], self.__matrix[1][2]],
                [self.__matrix[2][3], self.__matrix[2][1], self.__matrix[2][2]],
            ]
        )

        numerator_y = self.__determinant(
            [
                [self.__matrix[0][0], self.__matrix[0][3], self.__matrix[0][2]],
                [self.__matrix[1][0], self.__matrix[1][3], self.__matrix[1][2]],
                [self.__matrix[2][0], self.__matrix[2][3], self.__matrix[2][2]],
            ]
        )

        numerator_z = self.__determinant(
            [
                [self.__matrix[0][0], self.__matrix[0][1], self.__matrix[0][3]],
                [self.__matrix[1][0], self.__matrix[1][1], self.__matrix[1][3]],
                [self.__matrix[2][0], self.__matrix[2][1], self.__matrix[2][3]],
            ]
        )

        x = round(numerator_x / denominator, 3)
        y = round(numerator_y / denominator, 3)
        z = round(numerator_z / denominator, 3)

        return [x, y, z]

    def __determinant(self, matrix) -> int:
        """
        finds the determinant of a matrix.
        """
        result = (
            (
                matrix[0][0]
                * ((matrix[1][1] * matrix[2][2]) - (matrix[2][1] * matrix[1][2]))
            )
            - (
                matrix[0][1]
                * ((matrix[1][0] * matrix[2][2]) - (matrix[2][0] * matrix[1][2]))
            )
            + (
                matrix[0][2]
                * ((matrix[1][0] * matrix[2][1]) - (matrix[2][0] * matrix[1][1]))
            )
        )
        return result

    def __gjs_to_table(self, data, index, values) -> None:
        """
        writes the values for Jacopy/Seidel table.
        """
        data[0].append(index)
        data[1].append(values[0])
        data[2].append(values[1])
        data[3].append(values[2])
        
    def __rs_to_table(self, data, index, operation, dx, dy, dz, r1, r2, r3) -> None:
        data[0].append(index+1)
        data[1].append(operation)
        data[2].append(dx)
        data[3].append(dy)
        data[4].append(dz)
        data[5].append(r1)
        data[6].append(r2)
        data[7].append(r3)

    def __relaxation_table(self, data) -> str:
        arr = {"iteration": data[0], "operation": data[1], "dx": data[2], "dy": data[3], "dz": data[4], "R1": data[5], "R2": data[6], "R3": data[7]}
        df = pd.DataFrame(arr)
        table = tbl.tabulate(df, headers="keys", tablefmt="grid", showindex=False)
        return table
    
    def __jacopy_seidel_table(self, data) -> str:
        """
        shows the iteration table.
        """
        arr = {"iteration": data[0], "x": data[1], "y": data[2], "z": data[3]}
        df = pd.DataFrame(arr)
        table = tbl.tabulate(df, headers="keys", tablefmt="grid", showindex=False)
        return table
   