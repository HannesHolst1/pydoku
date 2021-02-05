# pydoku
Solves a Sudoku in Python using OpenCV & Deep Learning

This repository includes the following:
- Image processing
- Sudoku grid recognition
- Grid extraction
- Number prediction using Convolutional Neural Network-model (with 99% accurancy) 
- Recursive Sudoku-solver

The number prediction is based on a CNN-model that was trained with the Chars74K-dataset: http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/

### ToDo
- [x] switch to tflite-model
- [ ] integrate web frontend or expose through API
- [ ] finalize code structure

### Instructions

Clone repository and run `main.py`

### Output

```
testname: test1
using Canny, squares: 81
--- predicting numbers:  
[====================] 100%
--- scanned Sudoku:        
[0, 0, 0, 2, 0, 0, 7, 5, 3]
[6, 0, 0, 8, 0, 5, 0, 4, 0]
[0, 0, 0, 1, 0, 0, 9, 0, 0]
[8, 9, 7, 0, 0, 0, 0, 0, 5]
[0, 5, 0, 9, 1, 3, 0, 8, 0]
[1, 0, 0, 0, 0, 0, 6, 2, 9]
[0, 0, 2, 0, 0, 9, 0, 0, 0]
[0, 6, 0, 4, 0, 7, 0, 0, 2]
[5, 7, 4, 0, 0, 1, 0, 0, 0]
--- solved Sudoku:
[4, 1, 8, 2, 9, 6, 7, 5, 3]
[6, 3, 9, 8, 7, 5, 2, 4, 1]
[7, 2, 5, 1, 3, 4, 9, 6, 8]
[8, 9, 7, 6, 4, 2, 3, 1, 5]
[2, 5, 6, 9, 1, 3, 4, 8, 7]
[1, 4, 3, 7, 5, 8, 6, 2, 9]
[3, 8, 2, 5, 6, 9, 1, 7, 4]
[9, 6, 1, 4, 8, 7, 5, 3, 2]
[5, 7, 4, 3, 2, 1, 8, 9, 6]
---
===
```

### Original file
![original sudoku](https://raw.githubusercontent.com/HannesHolst1/pydoku/master/test_files/test1.jpg)

### Output (solved Sudoku)
![solved sudoku](https://github.com/HannesHolst1/pydoku/blob/master/output/test1_output.png?raw=true)
