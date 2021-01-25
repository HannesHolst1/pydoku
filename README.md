# pydoku
Solves a Sudoku in Python using OpenCV & Deep Learning

This repository includes the following:
- Image processing
- Sudoku grid recognition
- Grid extraction
- Number prediction using Convolutional Neural Network-model (with 99% accurancy) 
- Recursive Sudoku-solver

The number prediction is based on a CNN-model that was trained with the Chars74K-dataset: http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/

Download the dataset and extract into `./datasets/Char74K/`

Then, run `create_Char74K_CNN_model.py`
(It took appr. 30 minutes to complete on my laptop.)

This will create a dump of the trained model: `./models/Char74K_CNN_model.h5`

The CNN has the following benefits:
- The file in which the model is saved is much smaller (the kNN model-file was 650MB, the CNN model-file is 42MB)
- The prediction runs faster compared to kNN 

Current test output ----------------------->>>>

```
test1 -- test1-Sudoku succesful solved: True
test2 -- test2-Sudoku succesful solved: True
test3 -- test3-Sudoku succesful solved: True
test4 -- Could not extract Sudoku grid from image.
test5 -- test5-Sudoku succesful solved: False
test6 -- Could not extract Sudoku grid from image.
test7 -- Could not extract Sudoku grid from image.
test8 -- test8-Sudoku succesful solved: True
test9 -- test9-Sudoku succesful solved: True
test10 -- Could not extract Sudoku grid from image.
test11 -- Could not extract Sudoku grid from image.
test12 -- test12-Sudoku succesful solved: True
test13 -- test13-Sudoku succesful solved: True
test14 -- Could not extract Sudoku grid from image.
test15 -- Could not extract Sudoku grid from image.
test16 -- test16-Sudoku succesful solved: True
test17 -- Could not extract Sudoku grid from image.
```

## Original file
![original sudoku](https://raw.githubusercontent.com/HannesHolst1/pydoku/master/test_files/test1.jpg)

## Output (solved Sudoku)
![solved sudoku](https://github.com/HannesHolst1/pydoku/blob/master/output/test1_output.png?raw=true)
