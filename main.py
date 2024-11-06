from hsv_values import Hsv_values
from color_reader import ColorReader
import cv2
import subprocess
import sys

class Main:
    def __init__(self):
        self.image = cv2.imread('assets/squares.png', cv2.IMREAD_UNCHANGED)
        self.cap = cv2.VideoCapture(0)
        self.color_to_letter = {'blue': 'F',
                                'yellow': 'U',
                                'white': 'D',
                                'red': 'R',
                                'green': 'B',
                                'orange': 'L'}
        self.sides = {'yellow': 0,
                      'red': 1,
                      'blue': 2,
                      'white': 3,
                      'orange': 4,
                      'green': 5}
        self.faces = ['', '', '', '', '', '']
        self.color_reader = ColorReader()

    def colors_to_letters(self):
        result = ''
        
        for index in range(1, 10):
            color = self.color_reader.find_common_value(self.color_reader.square_values, index)
            result += self.color_to_letter[color]
        middle_color = self.color_reader.find_common_value(self.color_reader.square_values, 5)
        
        if self.faces[self.sides[middle_color]] == '':
            self.faces[self.sides[middle_color]] = result
            print(f'{middle_color} side has been registered.')

    def cube_letters(self):
        f_result = ''
        for item in self.faces:
            f_result += item
        return f_result

    def process_webcam(self):
        while True:
            
            _, frame = self.cap.read()
            
            overlay = self.image[:, :, :3]
            alpha = self.image[:, :, 3] / 255.0
            
            height, width = overlay.shape[:2]
            x1, y1 = 100, 100
            x2, y2 = x1 + width, y1 + height
            
            cv2.rectangle(frame, (107, 107), (157, 157), Hsv_values.color_to_rgb(self.color_reader.find_common_value(self.color_reader.square_values, 1)), thickness=5)
            cv2.rectangle(frame, (168, 107), (218, 157), Hsv_values.color_to_rgb(self.color_reader.find_common_value(self.color_reader.square_values, 2)), thickness=5)
            cv2.rectangle(frame, (229, 107), (279, 157), Hsv_values.color_to_rgb(self.color_reader.find_common_value(self.color_reader.square_values, 3)), thickness=5)
            cv2.rectangle(frame, (107, 168), (157, 218), Hsv_values.color_to_rgb(self.color_reader.find_common_value(self.color_reader.square_values, 4)), thickness=5) 
            cv2.rectangle(frame, (168, 168), (218, 218), Hsv_values.color_to_rgb(self.color_reader.find_common_value(self.color_reader.square_values, 5)), thickness=5)
            cv2.rectangle(frame, (229, 168), (279, 218), Hsv_values.color_to_rgb(self.color_reader.find_common_value(self.color_reader.square_values, 6)), thickness=5)
            cv2.rectangle(frame, (107, 229), (157, 279), Hsv_values.color_to_rgb(self.color_reader.find_common_value(self.color_reader.square_values, 7)), thickness=5)
            cv2.rectangle(frame, (168, 229), (218, 279), Hsv_values.color_to_rgb(self.color_reader.find_common_value(self.color_reader.square_values, 8)), thickness=5)
            cv2.rectangle(frame, (229, 229), (279, 279), Hsv_values.color_to_rgb(self.color_reader.find_common_value(self.color_reader.square_values, 9)), thickness=5)
            
            for c in range(0, 3):
                frame[y1:y2, x1:x2, c] = (1 - alpha) * frame[y1:y2, x1:x2, c] + alpha * overlay[:, :, c]

            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            cv2.imshow('Webcam', frame)
            
            self.color_reader.verify_color(hsv_frame)
            
            key_pressed = cv2.waitKey(1)
            
            if key_pressed == ord('\r'):  
                self.colors_to_letters()
                
            elif key_pressed == ord('r'):  
                cube_letters = self.cube_letters() 
                with open('rubiks_cube.txt', 'w') as file:
                    file.write(cube_letters)
                subprocess.Popen(['python', '3d_cube.py'])
                sys.exit()
                
            elif key_pressed & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

main = Main()
main.process_webcam()
