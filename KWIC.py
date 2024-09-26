class master:
    """
        This class is responsible for the overall orchestration of the KWIC system.
        It manages the line storage, input handling, circular shift generation, 
        alphabetization, and output.
    
        Attributes:
        lineStorage : LineStorage - Object to store lines and shifts.
        inputModule : InputModule - Object for reading lines.
        circularShift : CircularShift - Object for generating circular shifts.
        alphabetizer : Alphabetizer - Object for sorting shifts alphabetically.
        output : Output - Object for printing results.
    """

    def __init__(self):
        """
            Initializes the Master control class by creating instances of the components.
        """

        self.lineStorage = LineStorage()
        self.inputModule = InputModule()
        self.circularShift = CircularShift()
        self.alphabetizer = Alphabetizer()
        self.output = Output()

    def process_line(self, line):
        """
            Processes a single line of input through the KWIC system.
            
            Parameters:
            line : str - The input line to be processed.
            
            Returns: None
        """

        self.inputModule.read(line, self.lineStorage)
        self.circularShift.setup(self.lineStorage)
        self.alphabetizer.alpha(self.lineStorage)
        self.output.print_all_KWIC(self.lineStorage)
        


class InputModule:
    """
        This class handles reading the input line and storing it in the LineStorage.
    """

    def read(self, line, lineStorage):
        """
            Reads a line of input and stores it in the 'lines' array of LineStorage.
            
            Parameters:-
            line : str - The input line to be read.
            lineStorage : LineStorage - The storage object to hold the input line.
            
            Returns: None
        """

        self.line = line
        lineStorage.setline(self.line, 'lines')


class LineStorage:
    """
        This class is responsible for storing lines and shifts, 
        as well as managing various arrays (lines, sorted shifts, temporary shifts).
    """

    def __init__(self):
        """
            Initializes the arrays for storing lines, sorted shifts, and temporary shifts.
        """

        self.lines = []
        self.sorted_shifts = []
        self.temp_shifts = []

    def setline(self, line, array_name):
        """
            Adds a line to the specified array in LineStorage.
            
            Parameters:-
            line : str - The line to be added.
            array_name : str - Specifies which array ('lines', 'sorted_shifts', or 'temp_shifts') the line should be added to.
            
            Returns: None
        """

        if array_name == 'lines':
            array = self.lines            
        elif array_name == 'sorted_shifts':
            array = self.sorted_shifts            
        else:
            array = self.temp_shifts   
        array.append(line)

    def getline(self, indx, array_name):
        """
            Retrieves a line from the specified array.
            
            Parameters:-
            indx : int - The index of the line to retrieve.
            array_name : str - Specifies which array ('lines', 'sorted_shifts', or 'temp_shifts') to retrieve from.
            
            Returns:
            list or str - The line from the specified array.
        """
        
        if array_name == 'lines':
            array = self.lines            
        elif array_name == 'sorted_shifts':
            array = self.sorted_shifts            
        else:
            array = self.temp_shifts
        return array[indx]
    
    def getArray(self, array_name):
        """
            Retrieves the entire array from LineStorage.
            
            Parameters:-
            array_name : str - Specifies which array ('lines', 'sorted_shifts', or 'temp_shifts') to retrieve.
            
            Returns:
            list - The specified array.
        """
        
        if array_name == 'lines':
            array = self.lines            
        elif array_name == 'sorted_shifts':
            array = self.sorted_shifts            
        elif array_name == 'temp_shifts':
            array = self.temp_shifts
        else:
            print("Invalid array name...")
            return            
        return array
    
    def update_array(self, new_array, array_name):
        """
            Updates the specified array with a new array.
            
            Parameters:-
            new_array : list - The new array to replace the existing one.
            array_name : str - Specifies which array ('lines', 'sorted_shifts', or 'temp_shifts') to update.
            
            Returns: None
        """
        
        if array_name == 'lines':
            self.lines = new_array
        elif array_name == 'sorted_shifts':
            self.sorted_shifts = new_array
        elif array_name == 'temp_shifts':
            self.temp_shifts = new_array
        else:
            print("Invalid array name...")
            return
    

    def word(self, indx, array_name):
        """
            Returns the number of words in the line at the specified index.
            
            Parameters:-
            indx : int - The index of the line.
            array_name : str - Specifies which array ('lines', 'sorted_shifts', or 'temp_shifts') to count words from.
            
            Returns:
            int - The number of words in the line.
        """
        
        if array_name == 'lines':
            array = self.lines            
        elif array_name == 'sorted_shifts':
            array = self.sorted_shifts            
        else:
            array = self.temp_shifts            
        return len(array[indx].split())


class CircularShift:
    """
        This class is responsible for generating circular shifts of the input lines.
    """

    def setup(self, lineStorage):
        """
            Sets up the circular shift for the latest line stored in LineStorage.
            
            Parameters:-
            lineStorage : LineStorage - The storage object containing the lines.
            
            Returns: None
        """
        
        line = lineStorage.getline(-1, 'lines')

        n = lineStorage.word(-1, 'lines')
        shifts = lineStorage.temp_shifts
        words = line.split()

        lineStorage.setline(words, 'temp_shifts')

        self.shiftWords(n, shifts)
        

    def shiftWords(self, n, shifts):
        """
            Generates circular shifts for a given line.
            
            Parameters:-
            n : int - The number of words in the line.
            shifts : list - The temporary shifts array where new shifts are stored.
            
            Returns: None
        """

        for i in range(n-1):
            line_to_be_shifted = shifts[-1]
            shifted_line = [line_to_be_shifted[-1]] + line_to_be_shifted[:-1]

            shifts.append(shifted_line)

    def CSLine(self, indx, lineStorage):
        """
            Retrieves a circular shift line by index.
            
            Parameters:-
            indx : int - The index of the circular shift.
            lineStorage : LineStorage - The storage object containing the shifts.
            
            Returns:
            list - The circular shift at the specified index.
        """

        return lineStorage.getline(indx, 'temp_shifts')


class Alphabetizer:
    """
        This class is responsible for sorting the circular shifts alphabetically.
    """

    def alpha(self, lineStorage):
        """
            Sorts the circular shifts alphabetically and merges them with the existing sorted shifts.
            
            Parameters:-
            lineStorage : LineStorage - The storage object containing the shifts.
            
            Returns: None
        """

        shifts = lineStorage.getArray('temp_shifts')
        shifts.sort()
        sorted_shifts = lineStorage.getArray('sorted_shifts')
        n = len(shifts)
        m = len(lineStorage.sorted_shifts)

        if m == 0:
            sorted_shifts += shifts
            sorted_shifts.sort()
            shifts.clear()
            return

        i, j = 0, 0
        new_sorted_shift = []

        while i < n and j < m:
            if shifts[i] < sorted_shifts[j]:
                new_sorted_shift.append(shifts[i])
                i += 1
            else:
                new_sorted_shift.append(sorted_shifts[j])
                j += 1

        new_sorted_shift.extend(shifts[i:])
        new_sorted_shift.extend(sorted_shifts[j:])

        lineStorage.update_array(new_sorted_shift, 'sorted_shifts')
        shifts.clear()


    def ith(self,lineStorage, indx):
        """
            Retrieves the sorted circular shift at the specified index.
            
            Parameters:-
            lineStorage : LineStorage - The storage object containing the sorted shifts.
            indx : int - The index of the sorted shift.
            
            Returns:
            list - The sorted circular shift at the specified index.
        """
        
        return lineStorage.getline(indx, 'sorted_shifts')


class Output:
    """
        This class is responsible for printing the KWIC results.
    """

    def print_all_KWIC(self, lineStorage):
        """
            Prints all sorted circular shifts stored in LineStorage.
            
            Parameters:-
            lineStorage : LineStorage - The storage object containing the sorted shifts.
            
            Returns: None
        """
       
        sorted_shifts = lineStorage.sorted_shifts
        for line in sorted_shifts:
            print(" ".join(line))


    def print_KWIC(self, indx, lineStorage, alphabetizer):
        """
            Prints a specific KWIC result by index.
           
            Parameters:-
            indx : int - The index of the sorted shift to print.
            lineStorage : LineStorage - The storage object containing the sorted shifts.
            alphabetizer : Alphabetizer - The alphabetizer to retrieve the sorted shifts.
           
            Returns:
            None
        """
        
        line = alphabetizer.ith(lineStorage, indx)
        print(" ".join(line))
