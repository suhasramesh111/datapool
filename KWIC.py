class master:
    """
    The Master Control of the KWIC system. Manages the coordination of the entire process
    including input reading, circular shifting, alphabetizing, and output.
    """

    def __init__(self):
        """
        Initializes the Master Control, setting up the LineStorage, InputModule,
        CircularShift, Alphabetizer, and Output components.
        """

        self.lineStorage = LineStorage()
        self.inputModule = InputModule(self.lineStorage)
        self.circularShift = CircularShift()
        self.alphabetizer = Alphabetizer(self.circularShift, self.lineStorage)
        self.output = Output(self.alphabetizer)

    def process_line(self, line):
        """
        Processes a single line by reading, shifting, alphabetizing, and updating the KWIC index.

        Parameters:
        line (str): A line of text to be processed.
        """

        self.inputModule.read(line)
        self.circularShift.setup(self.lineStorage.getline(-1), self.lineStorage.word(-1))
        self.alphabetizer.alpha()


class InputModule:
    """
    Handles the input and storage of lines into LineStorage.
    """

    def __init__(self, lineStorage):
        """
        Initializes the InputModule.

        Parameters:
        lineStorage (LineStorage): An instance of LineStorage where lines will be stored.
        """

        self.lineStorage = lineStorage

    def read(self, line):
        """
        Reads a line and stores it into LineStorage.

        Parameters:
        line (str): A line of text to be read and stored.
        """

        self.line = line
        self.lineStorage.setline(self.line)


class LineStorage:
    """
    Stores lines of text and keeps track of sorted circular shifts.
    """

    def __init__(self):
        """
        Initializes the LineStorage with empty lines and sorted shifts lists.
        """

        self.lines = []
        self.sorted_shifts = []

    def setline(self, line):
        """
        Adds a line to the stored lines.

        Parameters:
        line (str): A line of text to be added to the storage.
        """

        self.lines.append(line)

    def getline(self, indx):
        """
        Retrieves a stored line based on the index.

        Parameters:
        indx (int): The index of the line to retrieve.

        Returns:
        str: The line of text at the specified index.
        """

        return self.lines[indx]

    def word(self, indx):
        """
        Counts the number of words in a specific line.

        Parameters:
        indx (int): The index of the line to count words from.

        Returns:
        int: The number of words in the line.
        """

        return len(self.lines[indx].split())


class CircularShift:
    """
    Handles the creation of circular shifts of lines.
    """

    def __init__(self):
        """
        Initializes the CircularShift with an empty list of shifts.
        """

        self.shifts = []

    def setup(self, line, n):
        """
        Sets up circular shifts for a given line.

        Parameters:
        line (str): The line of text to be circularly shifted.
        n (int): The number of words in the line.
        """

        words = line.split()
        self.shifts.append(words)
        self.shiftWords(n)

    def shiftWords(self, n):
        """
        Generates all circular shifts for the current line.

        Parameters:
        n (int): The number of words in the line.
        """

        for i in range(n-1):
            line_to_be_shifted = self.shifts[-1]
            shifted_line = [line_to_be_shifted[-1]] + line_to_be_shifted[:-1]
            self.shifts.append(shifted_line)

    def CSLine(self, indx):
        """
        Retrieves a circularly shifted line based on the index.

        Parameters:
        indx (int): The index of the circular shift to retrieve.

        Returns:
        list: The circularly shifted line as a list of words.
        """

        return self.shifts[indx]


class Alphabetizer:
    """
    Handles sorting circular shifts in lexicographic order and merging them into
    the sorted list of shifts.
    """

    def __init__(self, circularShift, linestorage):
        """
        Initializes the Alphabetizer.

        Parameters:
        circularShift (CircularShift): An instance of CircularShift to be alphabetized.
        linestorage (LineStorage): An instance of LineStorage to store sorted shifts.
        """

        self.circularShift = circularShift
        self.linestorage = linestorage

    def alpha(self):
        """
        Sorts the circular shifts and merges them with the existing sorted shifts.
        """

        shifts = self.circularShift.shifts
        shifts.sort()

        sorted_shifts = self.linestorage.sorted_shifts
        n = len(shifts)
        m = len(self.linestorage.sorted_shifts)

        if m == 0:
            sorted_shifts += shifts
            sorted_shifts.sort()
            shifts.clear()
            return

        i, j = 0, 0
        new_sorted_shift = []

        while i < n and j < m:
            if shifts[i] < self.linestorage.sorted_shifts[j]:
                new_sorted_shift.append(shifts[i])
                i += 1
            else:
                new_sorted_shift.append(self.linestorage.sorted_shifts[j])
                j += 1

        new_sorted_shift.extend(shifts[i:])
        new_sorted_shift.extend(self.linestorage.sorted_shifts[j:])

        self.linestorage.sorted_shifts = new_sorted_shift
        self.circularShift.shifts.clear()

    def ith(self, indx):
        """
        Retrieves the ith alphabetized circular shift.

        Parameters:
        indx (int): The index of the sorted circular shift to retrieve.

        Returns:
        list: The sorted circular shift at the specified index.
        """

        return self.linestorage.sorted_shifts[indx]


class Output:
    """
    Handles the output of KWIC lines.
    """

    def __init__(self, alphabetizer):
        """
        Initializes the Output class.

        Parameters:
        alphabetizer (Alphabetizer): An instance of Alphabetizer for retrieving sorted KWIC lines.
        """

        self.alphabetizer = alphabetizer

    def print_all_KWIC(self):
        """
        Prints all KWIC lines.
        """

        for line in self.alphabetizer.linestorage.sorted_shifts:
            print(" ".join(line))

    def print_KWIC(self, indx):
        """
        Prints the KWIC line at the specified index.

        Parameters:
        indx (int): The index of the KWIC line to print.
        """
        
        line = self.alphabetizer.ith(indx)
        print(" ".join(line))
