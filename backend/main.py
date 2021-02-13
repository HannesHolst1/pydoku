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
    '''
    Sudoku-class which holds all attributes and functions that represent a Sudoku.
    Usage:
        Sudoku.set_problem(image)
        Sudoku.solve()
        Sudoku.get_output()
    '''
    class Major_Grid:
        '''
        The Major_Grid-class is a representation of the outer border of the Sudoku which could be extracted from the image.
        '''
        image = None
        dimensions = None
        area = None
        minium_area = 0.15

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
            '''
            Counts all elements of self.images.
            '''
            counter = 0
            for row in self.images:
                counter += len(row)

            return counter

    def reset(self):
        self.problem = None
        self.output = None
        self.solved = False
        self.status = None
        self.contentarea = None
        self.shrink_to_ratio = 35
        self.imported_sudoku = []
        self.solved_sudoku = []
        self.model = None

        self.major_grid = self.Major_Grid()
        self.squares = self.Squares()

        self.init_tflite()

    def init_tflite(self):
        self.model = tflite.Interpreter(model_path='./backend/models/Chars74K_CNN_model.tflite')
        self.model.allocate_tensors()

    def __init__(self) -> None:
        self.reset()

    def __convert_image_to_io(self, image):
        buffer = cv2.imencode(".jpg", image)[1]
        img_io = io.BytesIO(buffer)
        img_io.seek(0)
        return img_io

    def __shrink(self, image):
        if self.shrink_to_ratio == 0:
            scale_percent = 50
        else:
            scale_percent = self.shrink_to_ratio

        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        return resized

    def set_problem(self, filename=None, in_memory_file=None):
        self.reset()
        if not in_memory_file is None:
            data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
            color_image_flag = 1
            self.problem = cv2.imdecode(data, color_image_flag)
        elif not filename is None:
            self.problem = cv2.imread(filename)
        else:
            self.problem = in_memory_file

        self.contentarea = self.problem.shape[0] * self.problem.shape[1]

    def find_sudoku(self, image):
        '''
        Tries to find a Sudoku in a given image.
        '''
        self.major_grid.image, self.major_grid.dimensions = mg.find_grid_by_edges(image)
        self.major_grid.area = self.major_grid.image.shape[0] * self.major_grid.image.shape[1]

        if self.major_grid.area / self.contentarea < self.major_grid.minium_area:
            self.major_grid.image, self.major_grid.dimensions = mg.find_grid_by_contentarea(image, self.major_grid.minium_area)
            self.major_grid.area = self.major_grid.image.shape[0] * self.major_grid.image.shape[1]

        return self.major_grid.image, self.major_grid.dimensions

    def extract_squares_from_sudoku(self, major_grid):
        '''
        Tries to extract squares from a Major Grid.
        '''
        return ge.extract_grid_elements(major_grid)

    def solve(self):
        self.major_grid.image, self.major_grid.dimensions = self.find_sudoku(self.problem)

        if not self.major_grid.image is None:
            self.squares.images, self.squares.coordinates = self.extract_squares_from_sudoku(self.major_grid.image)

        ## below happens when it wasn't possible to extract the Sudoku-puzzle from the image
        if self.squares.images is None:
            self.status = 'Could not extract complete Sudoku from image. Please try with another image!'
            self.solved = False
            self.output = copy.copy(self.problem)

            ## draw area in output-image to show the area recognized
            if not self.major_grid.dimensions is None:
                if len(self.major_grid.dimensions) == 4:
                    cv2.rectangle(self.output, 
                                (self.major_grid.dimensions[0], self.major_grid.dimensions[1]), 
                                (self.major_grid.dimensions[0]+self.major_grid.dimensions[2], self.major_grid.dimensions[1]+self.major_grid.dimensions[3]),
                                (0,255,0), 5)
            return

        ## In case the amount of extracted squares is less than the minium of squares that should have been extracted.
        ## For a standard 9x9 Sudoku, that should be 81.
        ## It can be less than the minium, when the image quality is not good enough. 
        if self.squares.count() < self.squares.minimum:
            self.status = 'Could not extract all squares from Sudoku. Please try with another image!'
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

        predicted_row = []
        for image_row in self.squares.images:
            for image_square in image_row:
                prep_image = im.prepare_image(image_square)
                prediction = predict.predict_number(prep_image, self.model)
                predicted_row.append(int(prediction[0]))

            self.imported_sudoku.append(predicted_row)
            predicted_row = []

        self.solved_sudoku = sp.solve(self.imported_sudoku)

        self.output = im.output_sudoku_solution(copy.copy(self.major_grid.image), self.squares.coordinates, self.imported_sudoku, self.solved_sudoku)

        if self.imported_sudoku != self.solved_sudoku:
            self.status = 'Sudoku solved.'
            self.solved = True
        else:
            self.status = 'It was not possible to solve the Sudoku. It was not possible to predict all numbers.'
        
    def get_problem(self):
        image = self.__shrink(self.problem)
        return self.__convert_image_to_io(image)

    def get_output(self):
        image = self.__shrink(self.output)
        return self.__convert_image_to_io(image)