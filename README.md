# datapool

This repository implements a search engine.

## KWIC Overview

This KWIC (Key Word In Context) system implements an abstract data type (ADT) architecture with implicit invocation for real-time text processing. It reads a set of input lines, generates circular shifts of each line, sorts these shifts, and outputs them in lexicographical order. The system processes data incrementally, allowing for continuous updates without reprocessing the entire dataset, simulating a real-time data stream.

### Key Components:
- **LineStorage**: Stores the input lines and the sorted circular shifts.
- **CircularShift**: Generates all circular shifts of a line.
- **Alphabetizer**: Sorts and merges circular shifts incrementally.
- **InputModule**: Reads and stores lines into LineStorage.
- **Output**: Displays the sorted shifts.

The driver code simulates real-time data by processing a line from the file `Dataset_KWIC.txt`. The system processes each line independently and updates the KWIC index by merging new shifts with the existing sorted list. This ensures efficient updating without re-sorting the entire dataset.

## Instructions on Committing to the Repository

- You will not be able to commit to the main branch directly. If you wish to do so:
  1. Create a new branch.
  2. Make your changes.
  3. Create a Pull Request (PR).
  4. Get approval and then merge to the main branch.
