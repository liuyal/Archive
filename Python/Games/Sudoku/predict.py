import cv2
import image_processes
from tensorflow.python.keras.models import load_model


def extract_number_image(img_grid):
    tmp_sudoku = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            image = img_grid[i][j]
            image = cv2.resize(image, (28, 28))
            thresh = 128
            gray = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]
            cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            for c in cnts:
                x, y, w, h = cv2.boundingRect(c)
                if (x < 3 or y < 3 or h < 3 or w < 3): continue
                ROI = gray[y:y + h, x:x + w]
                ROI = image_processes.scale_and_centre(ROI, 120)
                tmp_sudoku[i][j] = predict(ROI)
    return tmp_sudoku


def predict(img_grid):
    image = img_grid.copy()
    image = cv2.resize(image, (28, 28))
    image = image.astype('float32')
    image = image.reshape(1, 28, 28, 1)
    image /= 255
    model = load_model('cnn.hdf5')
    pred = model.predict(image.reshape(1, 28, 28, 1), batch_size=1)
    return pred.argmax()
