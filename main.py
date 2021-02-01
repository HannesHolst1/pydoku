import major_grid as mg
import grid_elements as ge
import cv2
import predict_CNN
import image_manipulation as im
import solve_puzzle as sp
import sys
from keras.models import load_model

def solve(name, filename, model, result):
    print("testname: {}".format(name))
    image = cv2.imread(filename)
    major_grid = mg.extract_major_grid(image)
    squares_images, square_coordinates = ge.extract_grid_elements(major_grid, name)

    if squares_images is None:
        result[name] = 'Could not extract Sudoku grid from image.'
        print('===')
        return

    print('--- predicting numbers:')
    imported_sudoku = []
    predicted_row = []
    progress = 0
    total = len(squares_images)*len(squares_images)
    for image_row in squares_images:
        for image_square in image_row:
            progress += 1
            j = progress / total
            sys.stdout.write('\r')
            sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
            sys.stdout.flush()

            prep_image = im.prepare_image(image_square)
            prediction = predict_CNN.predict_number(prep_image, model)
            predicted_row.append(int(prediction[0]))

        imported_sudoku.append(predicted_row)
        predicted_row = []

    print("")
    print('--- scanned Sudoku:')
    for line in imported_sudoku:
        print(line)

    print('--- solved Sudoku:')
    grid_solved = sp.solve(imported_sudoku)
    for line in grid_solved:
        print(line)

    print('---')
    result[name] = '{}-Sudoku succesful solved: {}'.format(name, imported_sudoku != grid_solved)
    print(result[name])
    if imported_sudoku != grid_solved:
        output = im.output_sudoku_solution(major_grid, square_coordinates, imported_sudoku, grid_solved)
        cv2.imwrite('./output/'+name+'_output.png', output)
    print('===')
    

#knn = joblib.load('./models/Char74K_knn_model.pkl')
model = load_model('./models/Char74K_CNN_model.h5')

results = {}

solve('test1', './test_files/test1.jpg', model, results)
solve('test2', './test_files/test2.jpg', model, results)
solve('test3', './test_files/test3.jpg', model, results)
solve('test4', './test_files/test4.jpg', model, results)
solve('test5', './test_files/test5.jpg', model, results)
solve('test6', './test_files/test6.jpg', model, results)
solve('test7', './test_files/test7.jpg', model, results)
solve('test8', './test_files/test8.jpg', model, results)
solve('test9', './test_files/test9.jpg', model, results)
solve('test10', './test_files/test10.jpg', model, results)
solve('test11', './test_files/test11.jpg', model, results)
solve('test12', './test_files/test12.jpg', model, results)
solve('test13', './test_files/test13.jpg', model, results)
solve('test14', './test_files/test14.jpg', model, results)
solve('test15', './test_files/test15.jpg', model, results)
solve('test16', './test_files/test16.jpg', model, results)
solve('test17', './test_files/test17.png', model, results)

for key, item in results.items():
    print('{} -- {}'.format(key, item))