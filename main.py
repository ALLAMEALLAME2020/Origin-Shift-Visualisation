import pygame
import sys
import os
import random
import time
from colorama import Fore, init, Style
init(autoreset=True)

pygame.init() # Initialisation (Get ready for work hehe)

# Varibles
screen_x, screen_y = 600, 600
celle_size = 40
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Origin Shift Visualisation")
clock = pygame.time.Clock()
Running = True
colors_root = {
    "background-color": (27, 26, 23),
    "walls-color": (230, 213, 184),
    "lines-color": (50, 50, 50),
    "Origin-node": (24, 174, 19, 0.8)
}

OriginNode = (0,0)
paths = set(OriginNode)
Origin_CallBack = (0, 0)
CallBack_full_list = []
Algorithm_status = False


# Build the Map function
def ClearMap():
    screen.fill((colors_root["background-color"])) # Background color
    # (X, Y) lines drawning
    for x in range(0, screen_x, celle_size): # (X) lines Rows
        pygame.draw.line(screen, colors_root["lines-color"], (x, 0), (x, screen_y))
        
    for y in range(0, screen_y, celle_size): # (Y) lines Columns
        pygame.draw.line(screen, colors_root["lines-color"], (0, y), (screen_x, y))
    
    
def ClearTerminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    
    
ClearMap()
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Closing window Event
            Running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q: # Closing window Event Using (Q Button)
                Running = False
                
            if event.key == pygame.K_m: # Saving the map cells in file to use lmra jaya
                try:
                    with open('PathData.txt','w') as file: # Write data on the file (Anl9ah fsame path kola mra hehe)
                        file.write(str(paths))
                        print(Fore.GREEN+Style.BRIGHT+f"Map god saved in the file Succsusfully")
                    pass
                except Exception as e: # Detect Errors
                    print(Fore.RED+Style.BRIGHT+f"Error Detected  : {e}")
                    
                    
            if event.key == pygame.K_c: # Clear the MAP (msa7 msa7)
                print(Fore.GREEN+Style.BRIGHT+f"Map hase been cleard !!")
                OriginNode = (0,0)
                Origin_CallBack = (0, 0)
                CallBack_full_list = []
                paths = set() # Clear the list of paths
                
                Algorithm_status = False
                ClearMap()
                
            
            if event.key == pygame.K_s:
                ClearTerminal()
                print(Fore.GREEN+Style.BRIGHT+f"[START]  : Algorithm Going to start RN.")
                Algorithm_status = True

            if event.key == pygame.K_o:
                ClearTerminal()
                print(Fore.RED+Style.BRIGHT+f"[SYS] : Algorithm God stopped for while.")
                Algorithm_status = False
    


    mouse = pygame.mouse.get_pressed() # Mouse Events hoohoo !!
    mouse_pose = pygame.mouse.get_pos() # Mouse [X, Y] cordinateS
    if mouse:
        if mouse_pose[0] > screen_x or mouse_pose[0] < 0 or mouse_pose[1] > screen_y or mouse_pose[1] < 0:
            pass
        else:
            if mouse[0]:
                blockPos_X = int(mouse_pose[0] / celle_size) # X cell Cordinates
                blockPos_Y = int(mouse_pose[1] / celle_size) # Y cell Cordinates
                
                print(Fore.BLUE+Style.BRIGHT+f"Left Mouse got pressed --> [ X: {Fore.GREEN+str(blockPos_X)+Fore.BLUE}, Y: {Fore.GREEN+str(blockPos_Y)+Fore.BLUE} ]")
            elif mouse[2]:
                blockPos_X = int(mouse_pose[0] / celle_size) # X cell Cordinates
                blockPos_Y = int(mouse_pose[1] / celle_size) # Y cell Cordinates
                
                pass
    
    
    
    if Algorithm_status:
        StartAlgorithm()
    
    
    def StartAlgorithm(): # Start Searching Algorithm
        global Origin_CallBack
        global OriginNode
        global Algorithm_status
        
        cell_x, cell_y = OriginNode[0], OriginNode[1]
        pygame.draw.circle(screen, colors_root["Origin-node"], ((OriginNode[0] * celle_size) + celle_size / 2 , (OriginNode[1] * celle_size) + celle_size / 2), 2)
        
        neighbors = [ # Searching for authers dotes bach ytconectaw wkda rak fahm
                [cell_x - 1, cell_y], # Left
                [cell_x + 1, cell_y], # Right
                [cell_x, cell_y + 1], # Down
                [cell_x, cell_y - 1] # Top
            ]
    
        Valid_choices = [ # Valid Nodes to choose randomlly
            
        ]
    
    
        for Neighber in neighbors:
            status = Filtring_Function(Neighber)
            print(status)
            if not status:
                pass
            if status:
                CallBack_full_list.append(Neighber)
                Valid_choices.append(Neighber)

        try:
            if not Valid_choices:
                if not Filtring_Function(CallBack_full_list.pop()):
                    CallBack_full_list.remove(CallBack_full_list[-1])
                else:
                    OriginNode = CallBack_full_list.pop()
                    Origin_CallBack = OriginNode
                    paths.add(tuple(OriginNode))
                    
            else:
                paths.add(tuple(OriginNode))
                Origin_CallBack = tuple(OriginNode)
                OriginNode = random.choice(Valid_choices)
                

            DrawingFunc(OriginNode[0], OriginNode[1])
            Valid_choices = []
            pass
        
        except Exception as e:
            ClearTerminal()
            print(Fore.RED+Style.BRIGHT+f"Error Detected !! {e}")
            Algorithm_status = False
            pass
    



    # just for filltring the neighbors (jiran wkda rak fahm hoohoo)
    def Filtring_Function(cordinates): 
        if cordinates[0] * celle_size < 0 or cordinates[0] * celle_size >= screen_x or cordinates[1] * celle_size < 0 or cordinates[1] * celle_size >= screen_y or tuple(cordinates) in paths:
            return False
        else:
            return True

    
    
    
    
    def DrawingFunc(Pos_x, Pos_y): # Drawing funciton.
           
        # Brock the bariers
        def BordersLogic():
            base, reference = OriginNode, Origin_CallBack
            
            direction_x = base[0] - reference[0]
            direction_y = base[1] - reference[1]

            
            if direction_x > 0:  # Right
                pygame.draw.line(
                    screen, colors_root["background-color"],
                    ((Origin_CallBack[0] * celle_size) + celle_size, (Origin_CallBack[1] * celle_size)),  # left side of right cell
                    ((Origin_CallBack[0] * celle_size) + celle_size, (Origin_CallBack[1] * celle_size) + celle_size)  # right side
                )

            elif direction_x < 0:  # Left
                pygame.draw.line(
                    screen, colors_root["background-color"],
                    (Origin_CallBack[0] * celle_size, Origin_CallBack[1] * celle_size),
                    (Origin_CallBack[0] * celle_size, (Origin_CallBack[1] * celle_size) + celle_size)
                )

            elif direction_y > 0:  # Down
                pygame.draw.line(
                    screen, colors_root["background-color"],
                    (Origin_CallBack[0] * celle_size, (Origin_CallBack[1] * celle_size) + celle_size),
                    ((Origin_CallBack[0] * celle_size) + celle_size, (Origin_CallBack[1] * celle_size) + celle_size)
                )

            elif direction_y < 0:  # Up
                pygame.draw.line(
                    screen, colors_root["background-color"],
                    (Origin_CallBack[0] * celle_size, Origin_CallBack[1] * celle_size),
                    ((Origin_CallBack[0] * celle_size) + celle_size, Origin_CallBack[1] * celle_size)
                )
            
        BordersLogic()
    
    
        # Change Old origin color
        pygame.draw.circle(screen, colors_root["walls-color"], ((Origin_CallBack[0] * celle_size) + celle_size / 2, (Origin_CallBack[1] * celle_size) + celle_size / 2), 2)
        
        # Draw New Origin Node
        pygame.draw.circle(screen, colors_root["Origin-node"], ((Pos_x * celle_size) + celle_size / 2, (Pos_y * celle_size) + celle_size / 2), 2)
    
        # Connect them by a line ( Rawabit 2ossariya rak fahm 3liya hhhhhh. ana 7amd 3arf 3arf)
        pygame.draw.line(screen, "red",
                         ((OriginNode[0] * celle_size) + celle_size/2, (OriginNode[1] * celle_size) + celle_size/2), # First Point Pos (Line start)
                         ((Origin_CallBack[0] * celle_size) + celle_size/2, (Origin_CallBack[1] * celle_size) + celle_size/2)  # Second Point Pos (Line End)
                         )
    pygame.display.update()
    clock.tick(60)
    pass



