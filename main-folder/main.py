#Importing important libraries
from tkinter import Canvas, Label, Tk, Button, StringVar, LEFT
from tkinter import *
#second importing 
from random import choice, randint

#importing pygame for adding some theme music / sound effects
import pygame 

#fourth importing for images wiht PIL
from PIL import Image, ImageTk

#utf4354675456453424635746857867654

pygame.mixer.init()

'''
#main game theme sound 
def play():
    pygame.mixer.music.load("super-mario.mp3")
    pygame.mixer.music.play()
'''
#main music code
main_music = pygame.mixer.music.load("super-mario.mp3")

#sound effects
block_placed = pygame.mixer.Sound("block-sounds.mp3")
complete_line = pygame.mixer.Sound("cheer-up.mp3")
game_over_sound = pygame.mixer.Sound("game-over.mp3")
reaching_score = pygame.mixer.Sound("john-cena.mp3")

complete_line.set_volume(0.1)

#finalize the music / effects
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.1)


'''
#block placed sound (on the surface or on each block)
def blocks_sound():
    pygame.mixer.Sound.load("block-sounds.mp3")
    pygame.mixer.Sound.play()
'''


#Main projects Canvas get helped from youtube on some functions
class MainCanvas(Canvas):
    def background_image():
        ImportWarning
    '''   
    bg = PhotoImage(file= "tetris-background.jpeg")
    my_label = Label(root, image = bg)
    my_label.place(x=0,y=0, relwidth=1, relheight=1)
    '''
    
    def clean_the_line(self, deleted_boxs):
        for box in deleted_boxs:
            self.delete(box)
        self.update()
    
    def reaching_score_functions(self):
        if self.score >= 100 :
            reaching_score.play()
        

    def boxes_dropped(self, need_to_drop):
        for box in need_to_drop:
            self.move(box, 0, main_tetris_game.BOX_SIZE)
        self.update()



    
    #full copied from internet but i understand what happened so no worry
    def main_game_page(self):
        board = [[0] * ((main_tetris_game.GAME_WIDTH - 20) // main_tetris_game.BOX_SIZE)\
                 for _ in range(main_tetris_game.GAME_HEIGHT // main_tetris_game.BOX_SIZE)]
        for box in self.find_withtag('game'):
            x, y, _, _ = self.coords(box)
            board[int(y // main_tetris_game.BOX_SIZE)][int(x // main_tetris_game.BOX_SIZE)] = 1
        return board
    def boxes(self):
        return self.find_withtag('game') == self.find_withtag(fill="blue")


#utf345678564634253413524635764879506

    def completed_lines_blocks(self, setting_y_coordinates):
        lines_got_cleaned = 0
        setting_y_coordinates = sorted(setting_y_coordinates)
        for y in setting_y_coordinates:
            if sum(1 for box in self.find_withtag('game') if self.coords(box)[3] == y) == \
               ((main_tetris_game.GAME_WIDTH - 20) // main_tetris_game.BOX_SIZE):
                self.clean_the_line([box
                                for box in self.find_withtag('game')
                                if self.coords(box)[3] == y])

                self.boxes_dropped([box
                                 for box in self.find_withtag('game')
                                 if self.coords(box)[3] < y])
                lines_got_cleaned += 1
        return lines_got_cleaned
    
#creating class of shape (main project) with events [copied the events from stackoverflow]
    
class Shape():
    def __init__(self, coords = None):
        if not coords:
            self.__coords = choice(main_tetris_game.SHAPES)
        else:
            self.__coords = coords

    

    @property
    def matrix(self):
        return [[1 if (j, i) in self.__coords else 0 \
                 for j in range(max(self.__coords, key=lambda x: x[0])[0] + 1)] \
                 for i in range(max(self.__coords, key=lambda x: x[1])[1] + 1)]

    def drop(self, board, offset):
        off_x, off_y = offset
        last_level = len(board) - len(self.matrix) + 1
        for level in range(off_y, last_level):
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    if board[level+i][off_x+j] == 1 and self.matrix[i][j] == 1:
                        return level - 1
        return last_level - 1  

#utf98678574635241354265376487598678575645

    @property
    def coords(self):
        return self.__coords

    def rotate(self):  
        self.__coords = self.rotating()

    def rotate_directions(self):
        rotated = self.rotating()
        directions = [(rotated[i][0] - self.__coords[i][0],
                       rotated[i][1] - self.__coords[i][1]) for i in range(len(self.__coords))]

        return directions
    
    def rotating(self):
        max_x = max(self.__coords, key=lambda x:x[0])[0]
        new_original = (max_x, 0)

        rotated = [(new_original[0] - coord[1],
                    new_original[1] + coord[0]) for coord in self.__coords]

        min_x = min(rotated, key=lambda x:x[0])[0]
        minimum_y_level = min(rotated, key=lambda x:x[1])[1]
        return [(coord[0] - min_x, coord[1] - minimum_y_level) for coord in rotated]

class Piece():
    def __init__(self, canvas, start_point, shape = None):
        self.__shape = shape
        if not shape:
            self.__shape = Shape()
        self.canvas = canvas
        self.boxes = self.creating_the_boxes(start_point)

    
#utf567895634524125657656978574635241
    
    def rotate(self):
        directions = self.__shape.rotate_directions()
        if all(self.__can_move(self.canvas.coords(self.boxes[i]), directions[i]) for i in range(len(self.boxes))):
            self.__shape.rotate()
            for i in range(len(self.boxes)):
                x, y = directions[i]
                self.canvas.move(self.boxes[i],
                                 x * main_tetris_game.BOX_SIZE,
                                 y * main_tetris_game.BOX_SIZE)

    @property
    def offset(self):
        return (min(int(self.canvas.coords(box)[0]) // main_tetris_game.BOX_SIZE for box in self.boxes),
                min(int(self.canvas.coords(box)[1]) // main_tetris_game.BOX_SIZE for box in self.boxes))

    def predicting_the_movments_of_the_blocks(self, board):
        level = self.__shape.drop(board, self.offset)
        minimum_y_level = min([self.canvas.coords(box)[1] for box in self.boxes])
        return (0, level - (minimum_y_level // main_tetris_game.BOX_SIZE))

    def predicting_the_dropped_blocks(self, board):
        level = self.__shape.drop(board, self.offset)
        self.removing_the_predicts()
        
        

    @property
    def shape(self):
        return self.__shape


    def move(self, direction):
        if all(self.__can_move(self.canvas.coords(box), direction) for box in self.boxes):
            x, y = direction
            for box in self.boxes:
                self.canvas.move(box,
                                 x * main_tetris_game.BOX_SIZE,
                                 y * main_tetris_game.BOX_SIZE)
            return True
        return False


        minimum_y_level = min([self.canvas.coords(box)[1] for box in self.boxes])
        for box in self.boxes:
            x1, y1, x2, y2 = self.canvas.coords(box)
            box = self.canvas.create_rectangle(x1,
                                               level * main_tetris_game.BOX_SIZE + (y1 - minimum_y_level),
                                               x2,
                                               (level + 1) * main_tetris_game.BOX_SIZE + (y1 - minimum_y_level),
                                               fill="red",
                                               tags = "predict")

    def removing_the_predicts(self):
        for i in self.canvas.find_withtag('predict'):
            self.canvas.delete(i) 
        self.canvas.update()

    

    def __can_move(self, box_coords, new_pos):
        x, y = new_pos
        x = x * main_tetris_game.BOX_SIZE
        y = y * main_tetris_game.BOX_SIZE
        x_left, y_up, x_right, y_down = box_coords

        overlap = set(self.canvas.find_overlapping((x_left + x_right) / 2 + x, 
                                                   (y_up + y_down) / 2 + y, 
                                                   (x_left + x_right) / 2 + x,
                                                   (y_up + y_down) / 2 + y))
        etc_items = set(self.canvas.find_withtag('game')) - set(self.boxes)

        if y_down + y > main_tetris_game.GAME_HEIGHT or \
           x_left + x < 0 or \
           x_right + x > main_tetris_game.GAME_WIDTH or \
           overlap & etc_items:
            return False
        return True        

#blocks color 10910 with main tag !

    def creating_the_boxes(self, start_point):
        boxes = []
        off_x, off_y = start_point
        for coord in self.__shape.coords:
            x, y = coord
            box = self.canvas.create_rectangle(x * main_tetris_game.BOX_SIZE + off_x,
                                               y * main_tetris_game.BOX_SIZE + off_y,
                                               x * main_tetris_game.BOX_SIZE + main_tetris_game.BOX_SIZE + off_x,
                                               y * main_tetris_game.BOX_SIZE + main_tetris_game.BOX_SIZE + off_y,
                                               fill="cyan",
                                               tags="game")
            boxes += [box]

        return boxes
    
    
#the main game logic using some classes and some functions
class main_tetris_game():
    SHAPES = ([(0, 0), (1, 0), (0, 1), (1, 1)],     
              [(0, 0), (1, 0), (2, 0), (3, 0)],     
              [(2, 0), (0, 1), (1, 1), (2, 1)],     
              [(0, 0), (0, 1), (1, 1), (2, 1)],     
              [(0, 1), (1, 1), (1, 0), (2, 0)],    
              [(0, 0), (1, 0), (1, 1), (2, 1)],     
              [(1, 0), (0, 1), (1, 1), (2, 1)])     

    BOX_SIZE = 19

    
    GAME_WIDTH = 300
    GAME_HEIGHT = 500
    GAME_START_POINT = GAME_WIDTH / 2 / BOX_SIZE * BOX_SIZE - BOX_SIZE

    #the standard thing when you use classes __init__.
    #some of the codes are from internet and github
    def __init__(self, predictable = False):
        self._level = 1
        self._score = 0
        self._blockcount = 0
        self.speed = 500
        self.predictable = predictable

        self.root = Tk()
        self.root.geometry("700x700") 
        self.root.title("Farbod Foroutani's self made Tetris")
        self.root.bind("<Key>", self.game_control)
        self.main_canvas_of_the_game()
        self.score_level_label_109()
        self.toward_piece_of_block()


#keybinds section

    def game_control(self, event):
        if event.char in ["a","A", "\uf702"]:
            self.current_piece.move((-1, 0))
            self.updating_the_predicts()
        elif event.char in ["d", "D", "\uf703"]:  #this \uf703 is direction codes
            self.current_piece.move((1, 0))
            self.updating_the_predicts()
        elif event.char in ["s", "S", "\uf701"]:
            self.__s_drop_straight()
        elif event.char in ["w", "W", "\uf700"]:
            self.current_piece.rotate()
            self.updating_the_predicts()

    
    def updating_each_piece(self):
        if not self.next_piece:
            self.next_piece = Piece(self.next_canvas, (20,20))

        self.current_piece = Piece(self.canvas, (main_tetris_game.GAME_START_POINT, 0), self.next_piece.shape)
        self.next_canvas.delete("all")
        self.drawing_the_next_canva_frame()
        self.next_piece = Piece(self.next_canvas, (20,20))
        self.updating_the_predicts()

    def start_the_new_game(self):
        self.level = 1
        self.score = 0
        self.blockcount = 0
        self.speed = 500

        self.canvas.delete("all")
        self.next_canvas.delete("all")

        self.draw_the_next_canva()
        self.drawing_the_next_canva_frame()

        self.current_piece = None
        self.next_piece = None        

        self.main_game_page = [[0] * ((main_tetris_game.GAME_WIDTH - 20) // main_tetris_game.BOX_SIZE)\
                           for _ in range(main_tetris_game.GAME_HEIGHT // main_tetris_game.BOX_SIZE)]

        self.updating_each_piece()

    
    def start(self):
        self.start_the_new_game()
        self.root.after(self.speed, None)
        self.drop()
        self.root.mainloop()


    #drop function similar to the main game.
    #but need an improvement
    def drop(self):
        if not self.current_piece.move((0,1)):
            self.current_piece.removing_the_predicts()
            self.completed_lines_blocks()
            self.main_game_page = self.canvas.main_game_page()
            self.updating_each_piece()

            if self.end_of_the_game_game_over():
                return
            else:
                self._blockcount += 1
                self.score += 1
                block_placed.play()
                
                
                



        self.root.after(self.speed, self.drop)

    
    
    #final getting statuses and setting the logic of last line
    #using F string too!
    def update_status(self):
        self.status_var.set(f"Score : {self.score}")
        self.status.update()

    def end_of_the_game_game_over(self):
        if not self.current_piece.move((0,1)):

            self.play_the_main_again_btn = Button(self.root, text="You Can Play Again :D", command=self.play_the_main_again)
            self.rage_quiting_btn = Button(self.root, text="What a loser (Imagine Losing)", command=self.rage_quiting) 
            self.play_the_main_again_btn.place(x = main_tetris_game.GAME_WIDTH + 80, y = 200, width=250, height=50)
            self.rage_quiting_btn.place(x = main_tetris_game.GAME_WIDTH + 80, y = 300, width=250, height=50)
            game_over_sound.play()
            return True
        return False

    def __s_drop_straight(self):
        self.current_piece.move(self.current_piece.predicting_the_movments_of_the_blocks(self.main_game_page))

    def updating_the_predicts(self):
        if self.predictable:
            self.current_piece.predicting_the_dropped_blocks(self.main_game_page)


    def play_the_main_again(self):
        self.play_the_main_again_btn.destroy()
        self.rage_quiting_btn.destroy()
        self.start()

    def rage_quiting(self):
        exit()
        self.root.rage_quiting()     

    def completed_lines_blocks(self):
        setting_y_coordinates = [self.canvas.coords(box)[3] for box in self.current_piece.boxes]
        completed_line = self.canvas.completed_lines_blocks(setting_y_coordinates)
        if completed_line == 1:
            self.score += 400
            complete_line.play()
        elif completed_line == 2:
            self.score += 1000
            complete_line.play()
        elif completed_line == 3:
            self.score += 3000
            complete_line.play()
        elif completed_line >= 4:
            self.score += 12000
            complete_line.play()
            
    def main_canvas_of_the_game(self):
        self.canvas = MainCanvas(self.root, 
                             width = main_tetris_game.GAME_WIDTH, 
                             height = main_tetris_game.GAME_HEIGHT)
        self.canvas.pack(padx=5 , pady=10, side=LEFT)



    def score_level_label_109(self):
        self.status_var = StringVar()        
        self.status = Label(self.root, 
                            textvariable=self.status_var, 
                            font=("Courier", 15, "bold"),
                            width = 100,
                            padx= 5 ,
                            pady= 68)
        
        self.status.pack(padx=5,pady=100)

    
    def toward_piece_of_block(self):
        self.next_canvas = Canvas(self.root,
                                 width = 100,
                                 height = 100)
        self.next_canvas.pack(padx=5 , pady=10)

#main game lines 

    def draw_the_next_canva(self):
        self.canvas.create_line(10, 0, 10, self.GAME_HEIGHT, fill = "#5D5D5D", tags = "line" ,width=10)
        self.canvas.create_line(self.GAME_WIDTH-10, 0, self.GAME_WIDTH-10, self.GAME_HEIGHT, fill = "#5D5D5D", tags = "line" ,width=10)
        self.canvas.create_line(5, 500, 295, self.GAME_HEIGHT, fill = "#5D5D5D", tags = "line" ,width=10)
        self.canvas.create_line(10, 3, 290, 3, fill ="#5D5D5D",width=10, tags="line")
        
        #column lines 
        
        self.canvas.create_line(self.GAME_WIDTH-36, 0, self.GAME_WIDTH-36, self.GAME_HEIGHT, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(self.GAME_WIDTH-56, 0, self.GAME_WIDTH-56, self.GAME_HEIGHT, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(self.GAME_WIDTH-74, 0, self.GAME_WIDTH-74, self.GAME_HEIGHT, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(self.GAME_WIDTH-94, 0, self.GAME_WIDTH-94, self.GAME_HEIGHT, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(self.GAME_WIDTH-112, 0, self.GAME_WIDTH-112, self.GAME_HEIGHT, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(self.GAME_WIDTH-132, 0, self.GAME_WIDTH-132, self.GAME_HEIGHT, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(self.GAME_WIDTH-150, 0, self.GAME_WIDTH-150, self.GAME_HEIGHT, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(self.GAME_WIDTH-170, 0, self.GAME_WIDTH-170, self.GAME_HEIGHT, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(self.GAME_WIDTH-188, 0, self.GAME_WIDTH-188, self.GAME_HEIGHT, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(self.GAME_WIDTH-208, 0, self.GAME_WIDTH-208, self.GAME_HEIGHT, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(self.GAME_WIDTH-226, 0, self.GAME_WIDTH-226, self.GAME_HEIGHT, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(self.GAME_WIDTH-246, 0, self.GAME_WIDTH-246, self.GAME_HEIGHT, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(self.GAME_WIDTH-264, 0, self.GAME_WIDTH-264, self.GAME_HEIGHT, fill = "#5D5D5D", tags = "line" ,width=1)
        
        # straight lines
        
        self.canvas.create_line(5, 475, 295, 475, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 456, 295, 456, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 436, 295, 436, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 417, 295, 417, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 398, 295, 398, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 379, 295, 379, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 360, 295, 360, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 341, 295, 341, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 322, 295, 322, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 303, 295, 303, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 285, 295, 285, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 266, 295, 266, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 247, 295, 247, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 228, 295, 228, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 209, 295, 209, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 190, 295, 190, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 171, 295, 171, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 152, 295, 152, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 133, 295, 133, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 114, 295, 114, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 95, 295, 95, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 76, 295, 76, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 57, 295, 57, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 38, 295, 38, fill = "#5D5D5D", tags = "line" ,width=1)
        self.canvas.create_line(5, 19, 295, 19, fill = "#5D5D5D", tags = "line" ,width=1)
        
        
        
    def drawing_the_next_canva_frame(self):
        self.next_canvas.create_rectangle(10, 10, 90, 90, tags="frame")

    def getting_the_level_count(self):
        return self._level

    def setting_next_level(self, level):
        self.speed = 500 - (level - 1) * 25
        self._level = level
        self.update_status()

    def getting_the_next_level__blocks(self):
        return self._score

    def blockcount_setting_tetrisv1(self, blockcount):
        self.level = blockcount // 5 + 1
        self._blockcount = blockcount
        
    def __set_score(self, score):
        self._score = score
        self.update_status()

    def blockcount_getting_tetris(self):
        return self._blockcount

    
    #LAST VALUABLES to finalize the result
    level = property(getting_the_level_count, setting_next_level)
    score = property(getting_the_next_level__blocks, __set_score)
    blockcount = property(blockcount_getting_tetris, blockcount_setting_tetrisv1)

#last thing to do
if __name__ == '__main__':
    game = main_tetris_game(predictable = True)
    game.start()