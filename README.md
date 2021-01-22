# pydoku
Solves a Sudoku in Python using OpenCV

This repository includes the following:
- Image processing
- Sudoku grid recognition
- Grid extraction
- Number prediction using kNN-model (with 97% confidence) 
- Recursive Sudoku-solver

The number prediction is based on kNN-model that was trained with the Char74K-dataset: http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/
Download the dataset and extract into `./datasets/Char74K/`

Then, run `create_Char74K_model.py`

This will create a dump of the trained model: `./models/Char74K_knn_model.pkl`

Current test output ----------------------->>>>

- test1 -- test1-Sudoku succesful solved: True
- test2 --test2-Sudoku succesful solved: True
- test3 -- test3-Sudoku succesful solved: True
- test4 -- Could not extract Sudoku grid from image.
- test5 -- test5-Sudoku succesful solved: False
- test6 -- Could not extract Sudoku grid from image.
- test7 -- Could not extract Sudoku grid from image.
- test8 -- test8-Sudoku succesful solved: True
- test9 -- test9-Sudoku succesful solved: False
- test10 -- Could not extract Sudoku grid from image.
- test11 -- Could not extract Sudoku grid from image.
- test12 -- test12-Sudoku succesful solved: True
- test13 -- test13-Sudoku succesful solved: True
- test14 -- Could not extract Sudoku grid from image.
- test15 -- Could not extract Sudoku grid from image.
- test16 -- test16-Sudoku succesful solved: True
- test17 -- Could not extract Sudoku grid from image.
