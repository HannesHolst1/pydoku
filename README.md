# pydoku
Solves a Sudoku in Python using OpenCV & Deep Learning. 

---> Live Demo: https://pydoku.azurewebsites.net/

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
- [x] recognize major grid based on area ratio of whole picture (e.g. when area of contour is at least 60% of whole picture and has at least 4 edges it is most likely the major grid)
- [x] consider session-based image processing
- [x] integrate demo-files in frontend
- [x] finalize code structure
- [x] clean unused boilerplate files

### If endless time would be available
- [ ] re-train CNN with more data
- [ ] test with more different Sudoku-puzzles
- [ ] consider handwritten numbers
- [ ] detect other puzzle sizes than 9x9 

### Instructions
#### Run as local webserver
- Download Python 3.8.x (TensorFlow requires Python 3.8.x)
- Clone repository to a local directory
- create a new virtual environment `py -3.8 -m venv name_of_your_virtualenv_here`
- run `pip install -r requirements.txt`
- in `run.py` enable `app.run(debug=True)` and execute
- open your webbrowser and go to `http://127.0.0.1:5000`

#### Create Docker image
- Open CLI (Command Line Interface)
- Change into directory of repository
- run `docker build --tag pydoku_app .`
- run `docker run --detach -p 80:80 pydoku_app`
- open your webbrowser and go to `localhost`

## FAQ
#### What are the minimum requirements?
The Sudoku should be a 9x9 Sudoku. Other types of Sudokus are not supported at the moment. The photo should have at least 8MP. The photo should clearly show a Sudoku with all borders. 

#### Why can my Sudoku not be solved?
This can have several reasons. It could be that it wasn't possible to detect the Sudoku itself in the photo. This can happen due to bad image quality.

#### What happens to the file I have uploaded?
This service is designed to process the image file on the fly. Files uploaded are not stored on the server.

#### I've tried to solve the Sudoku. What about the numbers I have written into the boxes?
Hand written numbers are not recognized properly. The app can be extended by integrating a second AI-model which could recognize hand-written numbers. 

#### Why does this exists at all?
Actually, to find a solution for a Sudoku is the fun a Sudoku has to offer. Therefor, offering a service that eliminates the fun by offering an automatic solution doesn't make much sense. But, this app is a pet project of mine that did teach me several technologies a long the way. So, the whole purpose of this app was to provide me obstacles I had to overcome. 

## Output

![webapp](https://github.com/HannesHolst1/pydoku/blob/master/app/static/assets/img/app.png?raw=true)
