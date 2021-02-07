from backend import major_grid as mg
from backend import grid_elements as ge
import cv2
from backend import predict
from backend import image_manipulation as im
from backend import solve_puzzle as sp
import tflite_runtime.interpreter as tflite
import numpy as np
import io
import copy

class Sudoku:
    class Major_Grid:
        image = None
        dimensions = None

        def __init__(self) -> None:
            pass

    class Squares:
        '''
        The Squares-class is a representation of all squares which could be extracted from the image.
        Ideally, images should be a list of 9x9.
        '''
        images = None
        coordinates = None
        minimum  = 81

        def __init__(self) -> None:
            pass

        def count(self):
            counter = 0
            for row in self.images:
                counter += len(row)

            return counter

    def __reset(self):
        self.problem = None
        self.output = None
        self.solved = False
        self.status = None
        self.shrink_ratio = 60

        self.major_grid = self.Major_Grid()
        self.squares = self.Squares()

    def __init__(self) -> None:
        self.__reset()

    def __convert_image_to_io(self, image):
        is_success, buffer = cv2.imencode(".jpg", image)
        img_io = io.BytesIO(buffer)
        img_io.seek(0)
        return img_io

    def __shrink(self, image):
        if self.shrink_ratio == 0:
            scale_percent = 60
        else:
            scale_percent = self.shrink_ratio

        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        return resized

    def set_problem(self, in_memory_file):
        self.__reset()
        if type(in_memory_file) == io.BytesIO:
            data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
            color_image_flag = 1
            self.problem = cv2.imdecode(data, color_image_flag)   
        else:
            self.problem = in_memory_file

    def find_sudoku(self, image):
        return mg.extract_major_grid(image)

    def extract_squares_from_sudoku(self, image):
        return ge.extract_grid_elements(image)

    def solve(self):
        self.major_grid.image, self.major_grid.dimensions = self.find_sudoku(self.problem)

        if not self.major_grid.image is None:
            self.squares.images, self.squares.coordinates = self.extract_squares_from_sudoku(self.major_grid.image)

        ## below happens when it wasn't possible to extract the Sudoku-puzzle from the image
        if self.squares.images is None:
            self.status = 'Could not extract complete Sudoku from image.'
            self.solved = False
            self.output = copy.copy(self.problem)

            ## draw area in output-image to show the area recognized
            if len(self.major_grid.dimensions) == 4:
                cv2.rectangle(self.output, 
                            (self.major_grid.dimensions[0], self.major_grid.dimensions[1]), 
                            (self.major_grid.dimensions[0]+self.major_grid.dimensions[2], self.major_grid.dimensions[1]+self.major_grid.dimensions[3]),
                            (0,255,0), 5)
            return

        if self.squares.count() < self.squares.minimum:
            self.status = 'Could not extract all squares from Sudoku.'
            self.solved = False
            self.output = copy.copy(self.major_grid.image)

            ## draw area in output-image to show the squares recognized
            for row in self.squares.coordinates:
                for square_coordinates in row:
                    cv2.rectangle(self.output, 
                                (square_coordinates[0], square_coordinates[1]), 
                                (square_coordinates[0]+square_coordinates[2], square_coordinates[1]+square_coordinates[3]),
                                (0,255,0), 3)
            return

        imported_sudoku = []
        predicted_row = []
        for image_row in self.squares.images:
            for image_square in image_row:
                prep_image = im.prepare_image(image_square)
                prediction = predict.predict_number(prep_image, model)
                predicted_row.append(int(prediction[0]))

            imported_sudoku.append(predicted_row)
            predicted_row = []

        grid_solved = sp.solve(imported_sudoku)

        if imported_sudoku != grid_solved:
            self.status = 'Sudoku solved.'
            self.solved = True
            self.output = im.output_sudoku_solution(self.major_grid.image, self.squares.coordinates, imported_sudoku, grid_solved)
        else:
            self.status = 'It was not possible to solve the Sudoku. Probably it was not possible to predict all numbers.'

        print(self.status)
        
    def get_problem(self):
        image = self.__shrink(self.problem)
        return self.__convert_image_to_io(image)

    def get_output(self):
        image = self.__shrink(self.output)
        return self.__convert_image_to_io(image)

def init_tflite():
    global model    
    model = tflite.Interpreter(model_path='./backend/models/Chars74K_CNN_model.tflite')
    model.allocate_tensors()

init_tflite()