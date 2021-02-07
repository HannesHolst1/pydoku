# pydoku
Solves a Sudoku in Python using OpenCV & Deep Learning.

This repository includes the following:
- Image processing
- Sudoku grid recognition
- Grid extraction
- Number prediction using Convolutional Neural Network-model (with 99% accurancy) 
- Recursive Sudoku-solver
- Flask web frontend (based on the Pixel-Lite boilerplate: https://demo.themesberg.com/pixel-lite/)

The number prediction is based on a CNN-model that was trained with the Chars74K-dataset: http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/

### ToDo
- [x] switch to tflite-model
- [x] integrate web frontend
- [ ] recognize major grid based on area ratio of whole picture (e.g. when area of contour is at least 60% of whole picture and has at least 4 edges it is most likely the major grid) 
- [ ] consider session-based image processing
- [ ] integrate demo-files in frontend
- [ ] make frontend vertical screen-friendly
- [ ] finalize code structure
- [ ] clean unused boilerplate files

### Instructions

- Download Python 3.8.x (TensorFlow requires Python 3.8.x)
- Clone repository to a local directory
- create a new virtual environment `py -3.8 -m venv name_of_your_virtualenv_here`
- run `pip install -r requirements.txt`
- execute `run.py`
- open your webbrowser and go to `http://127.0.0.1:5000`

## Output

### Original file
![original sudoku](https://github.com/HannesHolst1/pydoku/blob/master/backend/test_files/test9.jpg?raw=true)

### Solved Sudoku
![solved sudoku](https://github.com/HannesHolst1/pydoku/blob/master/backend/output/test9_output.png?raw=true)
