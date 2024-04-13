class JacopySeidel:
    def __init__(self, matrix) -> None:
        """
        constructs the matrix.
        """
        self._matrix = []
        self.jacopy_counter = 0
        self.seidel_counter = 0
        self.compare = False
        self.use_jacopy = False
        self.use_seidel = False
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
            self._matrix.append(arr)
            
            
    def view(self) -> None:
        """
        views the equation in matrix form
        """
        print("\nyour equation convert into matrix:")
        n = 0
        letters = ["x", "y", "z"]
        for arr in self._matrix:
            print(f"{arr[:-1]} [{letters[n]}] = {[arr[3]]}")
            n +=1
    def test_diagonally_dominant(self) -> None:
        """
        tests whether the matrix is diagonally dominant.
        """
        print("\ntesting if the matrix is diagonally dominant.")
        diagonal_item = 0
        counter = 0
        for arr in self._matrix:
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
                response = input("\nthe matrix is diagonally dominant, what method would you like to use?\ntype (GJ) for gauss-jacopy and (GS) for gauss-seidel\n").upper()
                if response == "GJ":
                    on = False
                    self.compare = True
                    self.use_seidel = True
                    return self._gauss_jacopy()
                elif response == "GS":
                    on = False
                    self.compare = True
                    self.use_jacopy = True
                    return self._gauss_seidel()
                else:
                    print("invalid input.")
        else:
            print("\nthe matrix is not diagonally dominant, the program will use Gauss-Seidel.")
            return self._gauss_seidel()
             
             
    def _gauss_seidel(self) -> str:
        """
        performs gauss-seidel method
        """
        if not self.use_seidel:
            print("\nusing Gauss-Seidel...")
        x, y, z = 0, 0, 0
        arr_x  = self._matrix[0]
        arr_y = self._matrix[1]
        arr_z = self._matrix[2]
        sx, sy, sz = 0, 0, 0
        while True:
            new_x = round((arr_x[3] - (arr_x[1] * y) - (arr_x[2] * z))/arr_x[0], 3)
            x = new_x
            new_y = round((arr_y[3] - (arr_y[0] * x) - (arr_y[2] * z))/arr_y[1], 3)
            y = new_y
            new_z = round((arr_z[3] - (arr_z[0] * x) - (arr_z[1] * y))/arr_z[2], 3)
            z = new_z
            self.seidel_counter += 1
            if self.seidel_counter > 100:
                return "\nerror: this system of linear equation doesn't converge."
            if (sx, sy, sz) == (x, y, z):
                break
            else:
                sx, sy, sz = x, y, z
        if self.use_jacopy:
            self._gauss_jacopy()
        return f"\nResult: x = {x}, y = {y}, z = {z}\nnumber of iterations: {self.seidel_counter}"
            

    def _gauss_jacopy(self) -> str:
        """
        performs gauss-jacopy method
        """
        if not self.use_jacopy:
            print("\nusing Gauss-Jacopy...")
        x, y, z = 0, 0, 0
        arr_x  = self._matrix[0]
        arr_y = self._matrix[1]
        arr_z = self._matrix[2]
        while True:
            new_x = round((arr_x[3] - (arr_x[1] * y) - (arr_x[2] * z))/arr_x[0], 3)
            new_y = round((arr_y[3] - (arr_y[0] * x) - (arr_y[2] * z))/arr_y[1], 3)
            new_z = round((arr_z[3] - (arr_z[0] * x) - (arr_z[1] * y))/arr_z[2], 3)
            self.jacopy_counter += 1
            if self.jacopy_counter > 100:
                return "\nerror: this system of linear equation doesn't converge."
            if (new_x, new_y, new_z) == (x, y, z):
                break
            else:
                x, y, z = new_x, new_y, new_z
        
        if self.use_seidel:
            self._gauss_seidel()
        return f"\nResult: x = {x}, y = {y}, z = {z}\nnumber of iterations: {self.jacopy_counter}"
    
    def method_comparison(self):
        """
        compares the two methods.
        """
        if self.jacopy_counter < self.seidel_counter:
            print("comparison: The Gauss-Jacopy method is more efficient than the Gauss-Seidel method.")
        elif self.seidel_counter < self.jacopy_counter:
            print("comparison: The Gauss-Seidel method is more efficient than the Gauss-Jacopy method.")
        else:
            print("comparison: Both of the methods are efficient for this system of linear equations.")
        
            
