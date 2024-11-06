from hsv_values import Hsv_values

class ColorReader:
    def __init__(self):
        self.square_values = {
            f'square_{i}_{j}': [None, 0, None] for i in range(1, 10) for j in range(1, 5)
        }

    def verify_color(self, hsv_frame):
        start_coord_y = 115
        start_coord_x = 115
        distance_dots = 34
        
        for square in range(9):
            for dot in range(4):
                y_offset = (dot % 2) * distance_dots
                x_offset = (dot // 2) * distance_dots
                
                pre_color = self.square_values[f'square_{square+1}_{dot+1}'][0]
                current_color = Hsv_values.hsv_to_color(hsv_frame[start_coord_x + x_offset, start_coord_y + y_offset])
                current_counter = self.square_values[f'square_{square+1}_{dot+1}'][1]
                
                if pre_color is None:
                    self.square_values[f'square_{square+1}_{dot+1}'][0] = current_color
                    
                elif current_color == pre_color:      
                    self.square_values[f'square_{square+1}_{dot+1}'][1] += 1
                  
                else:
                    self.square_values[f'square_{square+1}_{dot+1}'][0] = current_color
                    self.square_values[f'square_{square+1}_{dot+1}'][1] = 0   
                
                if current_counter > 30 and pre_color != False:
                    self.square_values[f'square_{square+1}_{dot+1}'][2] = pre_color
                    self.square_values[f'square_{square+1}_{dot+1}'][1] = 0
                            
            start_coord_y += 61     
                        
            if (square+1) % 3 == 0:
                start_coord_x += 61
                start_coord_y = 115

    @staticmethod
    def find_common_value(dictionary, square):
        group_values = [dictionary[f'square_{square}_{col}'][2] for col in range(1, 5)]
        common_value = None
        
        for value in group_values:
            if group_values.count(value) >= 3:
                common_value = value
                break
        if common_value is not None:
            return common_value
        else:
            return "white"
