# datapool

This repository implements a search engine.

## Requirements
- Python 3.X.X
- pymongo 4.10.1 - can be installed using -> python -m pip install "pymongo[srv]"


## KWIC Overview

This KWIC (Key Word In Context) system implements an abstract data type (ADT) architecture with implicit invocation for real-time text processing. It reads a set of input lines, generates circular shifts of each line, sorts these shifts, and outputs them in lexicographical order. The system processes data incrementally, allowing for continuous updates without reprocessing the entire dataset, simulating a real-time data stream.

### Key Components:
- **LineStorage**: Stores the input lines and the sorted circular shifts.
- **CircularShift**: Generates all circular shifts of a line.
- **Alphabetizer**: Sorts and merges circular shifts incrementally.
- **InputModule**: Reads and stores lines into LineStorage.
- **Output**: Displays the sorted shifts [and/or] it can push the circuarly shifted lines to MongoDB cloud

The driver code simulates real-time data by processing a line from the file `Dataset_KWIC.txt`. The system processes each line independently and updates the KWIC index by merging new shifts with the existing sorted list. This ensures efficient updating without re-sorting the entire dataset.

## Cyberminer Overview

Cyberminer is our search engine that uses the Kwic index system previously generated to process a query and return the websites that best match the query.

### Key Components;
- **Case - Sensitive search**: Performs case-sensitive search of all the query terms.
- **And Search**: The system currently performs the AND search, i.e all the terms in the query must be present in the document.

## Insturctions to use
The KWIC_driver.py file is used to generate circular shifts of each website present in the give dataset and push it to the mongoDB cloud.
The Cyberminer_driver.py file is used to perform search on the websites and retrieve a list of URLs based on the query using the case_sensitive_search() method of searchEngine class.

## Instructions on Committing to the Repository

- You will not be able to commit to the main branch directly. If you wish to do so:
  1. Create a new branch.
  2. Make your changes.
  3. Create a Pull Request (PR).
  4. Get approval and then merge to the main branch.
