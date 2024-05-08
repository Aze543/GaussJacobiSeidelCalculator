import pandas as pd
import tabulate as tbl
import time
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
        self.__gj_approx = ""
        self.__gs_approx = ""
        self.__rs_approx = ""
        self.__gjdata = [[], [], [], []]
        self.__gsdata = [[], [], [], []]
        self.__rsdata = [[], [], [], [], [],[], [], []]
        for array in matrix:
            arr = []
            n, sign = "", ""
            for item in array:
                try:
                    float(item)
                except Exception:
                    if item == ".":
                        n += item
                    elif item == "-":
                        sign += item
                    elif item == "=":
                        for i in range(array.index(item)+ 1, len(array)):
                            n += str(array[i])
                        arr.append(float(sign+n))
                        break
                    else:
                        if n == "":
                            n += "1"
                        arr.append(float(sign+n))
                        n, sign = "", ""
                else:
                    n += item
            if len(arr[:-1]) != 3:
                float("x")
            self.__matrix.append(arr)

    def view_matrix(self) -> None:
        """
        views the equation in matrix form
        """
        print("\nyour equation convert into matrix:\n")
        n = 0
        letters = ["x", "y", "z"]
        for arr in self.__matrix:
            print(f"{arr[:-1]} [{letters[n]}] = {[arr[3]]}")
            n += 1
            
    def test_diagonal_dominance(self) -> bool:
        """
        Tests whether the matrix is diagonally dominant in any sequence
        """
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
                    if arr.index(item) == diagonal_item:
                        continue
                    sum += abs(item)
                if arr[diagonal_item] > sum:
                    counter += 1
                diagonal_item += 1
            if counter == 3:
                self.__matrix = matrix
                return True
            elif p_counter == 6:
                self.__matrix= [matrix[2], matrix[1], matrix[0]]
                return False
            else:
                counter = 0
                p_counter += 1
                diagonal_item = 0
    
    def gauss_seidel(self) -> list:
        """
        performs Gauss-Seidel method
        """
        start = time.time()
        x, y, z = 0, 0, 0
        arr_x = self.__matrix[0]
        arr_y = self.__matrix[1]
        arr_z = self.__matrix[2]
        sx, sy, sz = 0, 0, 0
        self.__gs_approx += f"\ninitial values: x = {x}, y = {y}, z = {z}\n"
        self.__gjs_to_table(data=self.__gsdata, index=self.__seidel_counter, values=[sx,sy, sz])
        self.__seidel_counter += 1
        while True:
            self.__gs_approx += f"\n>> approximation #{self.__seidel_counter}\n"
            x = round((arr_x[3] - (arr_x[1] * y) - (arr_x[2] * z)) / arr_x[0], 3)
            self.__gs_approx += f"\nx = ({arr_x[3]} - ({arr_x[1]} * {y}) - ({arr_x[2]} * {z}))/{arr_x[0]} = {x}\n"
            
            y = round((arr_y[3] - (arr_y[0] * x) - (arr_y[2] * z)) / arr_y[1], 3)
            self.__gs_approx += f"y = ({arr_x[3]} - ({arr_x[0]} * {y}) - ({arr_x[2]} * {z}))/{arr_x[1]} = {y}\n"
            
            z = round((arr_z[3] - (arr_z[0] * x) - (arr_z[1] * y)) / arr_z[2], 3)
            self.__gs_approx += f"z = ({arr_x[3]} - ({arr_x[0]} * {y}) - ({arr_x[1]} * {z}))/{arr_x[2]} = {z}\n"
            
            self.__gjs_to_table(data=self.__gsdata, index=self.__seidel_counter, values=[x,y,z])
            if (sx, sy, sz) == (x, y, z):
                elapsed_time = f"{round((time.time() - start) * 10**3, 3)} ms"
                break
            elif self.__seidel_counter > 100:
                return "the matrix is diverginng."
            else:
                self.__seidel_counter += 1
                sx, sy, sz = x, y, z     
        return [self.__seidel_counter, self.__jacopy_seidel_table(data=self.__gsdata), x, y, z, self.__gs_approx, elapsed_time]

    def gauss_jacopy(self) -> list:
        """
        Performs Gauss-Jacopy method
        """
        start = time.time()
        x, y, z = 0, 0, 0
        arr_x = self.__matrix[0]
        arr_y = self.__matrix[1]
        arr_z = self.__matrix[2]
        self.__gj_approx += f"\ninitial values: x = {x}, y = {y}, z = {z}\n"
        while True:
            self.__gjs_to_table(data=self.__gjdata, index=self.__jacopy_counter, values=[x, y, z])
            new_x = round((arr_x[3] - (arr_x[1] * y) - (arr_x[2] * z)) / arr_x[0], 3)
            new_y = round((arr_y[3] - (arr_y[0] * x) - (arr_y[2] * z)) / arr_y[1], 3)
            new_z = round((arr_z[3] - (arr_z[0] * x) - (arr_z[1] * y)) / arr_z[2], 3)
            if (new_x, new_y, new_z) == (x, y, z):
                elapsed_time = f"{round((time.time() - start) * 10**3, 3)} ms"
                break
            else:
                self.__jacopy_counter += 1
                self.__gj_approx += f"\n>> approximation #{self.__jacopy_counter}\n"
                self.__gj_approx += f"\nx = ({arr_x[3]} - ({arr_x[1]} * {y}) - ({arr_x[2]} * {z}) / {arr_x[0]} = {new_x}\n"
                self.__gj_approx += f"y = ({arr_y[3]} - ({arr_y[0]} * {x}) - ({arr_y[2]} * {z}) / {arr_y[1]} = {new_y}\n"
                self.__gj_approx += f"z = ({arr_z[3]} - ({arr_z[0]} * {x}) - ({arr_z[1]} * {y}) / {arr_z[2]} = {new_z}\n"
                x, y, z = new_x, new_y, new_z
                
        return [self.__jacopy_counter, self.__jacopy_seidel_table(data=self.__gjdata), x, y, z, self.__gj_approx, elapsed_time]

    def relaxation(self) -> list:
        """
        Performs Gauss-Jacopy method
        """
        start = time.time()
        x,y,z = 0,0,0
        dx,dy,dz = 0,0,0
        tol = 1e-3
        arr_x = self.__matrix[0].copy()
        arr_y = self.__matrix[1].copy()
        arr_z = self.__matrix[2].copy()
        ri_x = max([abs(n) for n in arr_x[:-1]])
        ri_y = max([abs(n) for n in arr_y[:-1]])
        ri_z = max([abs(n) for n in arr_z[:-1]])
        arr = {"Residual Increments": ["dx", "dy", "dz"], "R1": [n*-1 for n in arr_x[:-1]], "R2": [n*-1 for n in arr_y[:-1]], "R3": [n*-1 for n in arr_z[:-1]]}
        df = pd.DataFrame(arr)
        rst = tbl.tabulate(df, headers="keys", tablefmt="grid", showindex=False)
        self.__rs_approx += f"\n{rst}\n"
        f_x, f_y, f_z = 0,0,0
        letters = ["x", "y", "z"]
        while True:
            r1 = arr_x[3] - (arr_x[0]*x) - (arr_x[1]*y) - (arr_x[2]*z)
            r2 = arr_y[3] - (arr_y[0]*x) - (arr_y[1]*y) - (arr_y[2]*z)
            r3 = arr_z[3] - (arr_z[0]*x) - (arr_z[1]*y) - (arr_z[2]*z)
            r1 = round(r1, 4)
            r2 = round(r2, 4)
            r3 = round(r3, 4)
            operation = 0
            for n in enumerate([x,y,z]):
                if abs(n[1]) != 0:
                    operation = f"d{letters[n[0]]} = {round(n[1], 4)}"
            self.__rs_to_table(data=self.__rsdata, index=self.__relaxation_counter,operation=operation, dx=x, dy=y, dz=z, r1=r1, r2=r2, r3=r3)
            self.__relaxation_counter += 1
            self.__rs_approx += f"\n>> approximation #{self.__relaxation_counter}\n"
            self.__rs_approx += f"\nR1 = {arr_x[3]} - ({arr_x[0]} * {x}) - ({arr_x[1]} * {y}) - ({arr_x[2]} * {z}) = {r1}\n"
            self.__rs_approx += f"R2 = {arr_y[3]} - ({arr_y[0]} * {x}) - ({arr_y[1]} * {y}) - ({arr_y[2]} * {z}) = {r2}\n"
            self.__rs_approx += f"R3 = {arr_z[3]} - ({arr_z[0]} * {x}) - ({arr_z[1]} * {y}) - ({arr_z[2]} * {z}) = {r3}\n"
            if [abs(n) < tol for n in [r1-dx, r2-dy, r3-dz]] == [True, True, True]:
                elapsed_time = f"{round((time.time() - start) * 10**3, 3)} ms"
                break
            else:
                arr_x[3], arr_y[3], arr_z[3] = r1, r2, r3
                if abs(r1) == max([abs(n) for n in [r1, r2, r3]]):
                    dx = round(r1/ri_x, 4)
                    self.__rs_approx += f"\nmaximum: R1 = {r1}\ndx = {r1}/{ri_x} = {dx}\n"
                    f_x += dx
                    x, y, z = dx,0,0
                elif abs(r2) == max([abs(n) for n in [r1, r2, r3]]):
                    dy = round(r2/ri_y, 4)
                    self.__rs_approx += f"\nmaximum: R2 = {r2}\ndy = {r2}/{ri_y} = {dy}\n"
                    f_y += dy
                    x, y, z = 0,dy,0
                elif abs(r3) == max([abs(n) for n in [r1, r2, r3]]):
                    dz = round(r3/ri_z, 4)
                    self.__rs_approx += f"\nmaximum: R3 = {r3}\ndx = {r3}/{ri_z} = {dz}\n"
                    f_z += dz
                    x, y, z = 0,0,dz
                
            
        return [self.__relaxation_counter, self.__relaxation_table(data=self.__rsdata), round(f_x, 3),round(f_y, 3),round(f_z, 3), self.__rs_approx, elapsed_time]

    def cramers_rule(self) -> list:
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
        try: 
            x = round(numerator_x / denominator, 3)
            y = round(numerator_y / denominator, 3)
            z = round(numerator_z / denominator, 3)
        except Exception as e:
            print(f"\nCramer's Rule\n[ERROR: {e}] the operation cannot continue.")
            return False
        return [x, y, z]

    def __determinant(self, matrix) -> float:
        """
        finds the determinant of a matrix.
        """
        result = (
            (matrix[0][0] * ((matrix[1][1] * matrix[2][2]) - (matrix[2][1] * matrix[1][2])))
            - (matrix[0][1] * ((matrix[1][0] * matrix[2][2]) - (matrix[2][0] * matrix[1][2])))
            + (matrix[0][2] * ((matrix[1][0] * matrix[2][1]) - (matrix[2][0] * matrix[1][1])))
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
        """
        writes the values for Relaxation table.
        """
        data[0].append(index+1)
        data[1].append(operation)
        data[2].append(dx)
        data[3].append(dy)
        data[4].append(dz)
        data[5].append(r1)
        data[6].append(r2)
        data[7].append(r3)

    def view_ranking(self) -> None:
        rank = {"Gauss-Jacopy Method": self.__jacopy_counter, "Gauss-Seidel Method": self.__seidel_counter, "Relaxation Method": self.__relaxation_counter}
        name, counter = list(rank.keys()), list(rank.values())
        sorted_rank = argsort(counter)
        print("\nbest method:")
        [print(f"{i[0]+1}. {name[i[1]]} -> {counter[i[1]]} iterations") for i in enumerate(sorted_rank)]
        
    def __relaxation_table(self, data) -> str:
        """
        shows the iteration table of relaxation.
        """
        arr = {"iteration": data[0], "operation": data[1], "dx": data[2], "dy": data[3], "dz": data[4], "R1": data[5], "R2": data[6], "R3": data[7]}
        df = pd.DataFrame(arr)
        table = tbl.tabulate(df, headers="keys", tablefmt="grid", showindex=False)
        return table
    
    def __jacopy_seidel_table(self, data) -> str:
        """
        shows the iteration table of Jacopy/Seidel.
        """
        arr = {"iteration": data[0], "x": data[1], "y": data[2], "z": data[3]}
        df = pd.DataFrame(arr)
        table = tbl.tabulate(df, headers="keys", tablefmt="grid", showindex=False)
        return table
   