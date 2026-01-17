import pygame
import sys
import os
import random
import time
from colorama import Fore, init, Style
init(autoreset=True)

pygame.init() # Initialisation (Get ready for work hehe)

# Varibles
Running = True
screen_x, screen_y = 600, 600
celle_size = 10
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Origin Shift Visualisation")
clock = pygame.time.Clock()
colors_root = {
    "background-color": (27, 26, 23),
    "walls-color": (230, 213, 184),
    "lines-color": (50, 50, 50),
    "Origin-node": (24, 174, 19, 0.8)
}

OriginNode = (0,0)
Origin_CallBack = (0, 0)
NotValid = set(OriginNode)
DeadCells = set()
stack_history = []
Algorithm_status = False
Show_Details = False

start_time = 0

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
    
    
# Welcoming Message
def Welcoming():
    ClearTerminal() # clear the terminal
    print(Fore.BLUE+Style.BRIGHT+f"""
Hey Ther. I am {Fore.MAGENTA}t0m.dev{Fore.BLUE} or {Fore.MAGENTA}TOM{Fore.BLUE}, happy to see you using my project Agin.
          
{Fore.CYAN}[/] Description  :
- {Fore.GREEN} The idea is simple. i used Origin-Shift Algorithme to make a visualisation of Maze Generating.{Fore.BLUE}
          
{Fore.CYAN}[/] Note  :
- {Fore.MAGENTA}[Z] {Fore.BLUE} To Show The details of maze generating press {Fore.MAGENTA}[ Z ]{Fore.BLUE} Before you starting the Algorithm.
- {Fore.MAGENTA}[S] {Fore.BLUE} To Start The algorithme press {Fore.MAGENTA}[S]{Fore.BLUE}. Also use the same key in your keyboard to pause it.
- {Fore.MAGENTA}[M] {Fore.BLUE} To Save The used path in text file inside the same direction use {Fore.MAGENTA}[M]{Fore.BLUE}. (Use it after the maze get finished)
- {Fore.MAGENTA}[O] {Fore.BLUE} Finally To Quit the Visualisation press {Fore.MAGENTA}[Q]{Fore.BLUE}.
          
          
{Fore.CYAN}[/] Also  :
- {Fore.BLUE} The Default Settings are  :
    {Fore.GREEN}-> Show-Details  : {Fore.RED+str(Show_Details)}
    {Fore.GREEN}-> Cell-Size  : {Fore.RED+str(celle_size)}px
    {Fore.GREEN}-> Screen-Size  : [{Fore.RED+str(screen_x)}px | {str(screen_y)}px{Fore.GREEN}]
    
    
{Fore.CYAN}[<3] From < t0m.dev > | < TOM >
          """)
    
    time.sleep(2)
    pass

   
ClearMap()
Welcoming() 

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Closing window Event
            Running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q: # Closing window Event Using (Q Button)
                Running = False
                
                
            # Saving the map cells in file to use lmra jaya      (M)  : Keyboard
            if event.key == pygame.K_m:
                try:
                    with open('PathData.txt','w') as file: # Write data on the file (Anl9ah fsame path kola mra hehe)
                        file.write(str(NotValid))
                        print(Fore.GREEN+Style.BRIGHT+f"Map got saved in the file Succsusfully")
                    pass
                except Exception as e: # Detect Errors
                    print(Fore.RED+Style.BRIGHT+f"Error Detected  : {e}")
                
                
            # Clearing the Board (Map).   (C)  : Keyboard     
            if event.key == pygame.K_c: 
                print(Fore.GREEN+Style.BRIGHT+f"Map hase been cleard !!")
                OriginNode = (0,0)
                Origin_CallBack = (0, 0)
                stack_history = []
                NotValid = set() # Clear the list of NotValid
                DeadCells = set()
                
                Algorithm_status = False
                ClearMap()
                print(DeadCells)
                
            
            # Start and stop using the Same button   (S)  : Keyboard
            if event.key == pygame.K_s:
                if Algorithm_status:
                    Algorithm_status = False
                    start_time = time.time() - start_time
                    ClearTerminal()
                    print(Fore.YELLOW+Style.BRIGHT+f"[START]  : Algorithm get stopped For a bit")
                elif not Algorithm_status:
                    Algorithm_status = True
                    ClearTerminal()
                    print(Fore.GREEN+Style.BRIGHT+f"[START]  : Algorithm Going to start RN.")
                    
                    # Continue the counting
                    if not start_time:
                        start_time = time.time()
                    else:
                        start_time = time.time() - start_time
                
                

            if event.key == pygame.K_z:
                if not Show_Details:
                    Show_Details = True
                else:
                    Show_Details = False
    


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
        global NotValid
        
        cell_x, cell_y = OriginNode[0], OriginNode[1]
        
        neighbors = [ # Searching for authers dotes bach ytconectaw wkda rak fahm
                [cell_x - 1, cell_y], # Left
                [cell_x + 1, cell_y], # Right
                [cell_x, cell_y + 1], # Down
                [cell_x, cell_y - 1] # Top
            ]
    
        Valid_choices = [ # Valid Nodes to choose randomlly
            
        ]
    
    
    
        # Yaa jedk l7rira katbda mn hna bla ma tsawlni ana katb hadchi o ma3rftoch kifach 5dm hahaha
        # (RIR DAHK :D )

        

        for Neighber in neighbors:
            if tuple(Neighber) in NotValid:
                pass
            status = Filtring_Function(Neighber)
            # print(status)
            if not status:
                pass
            if status:
                Valid_choices.append(Neighber)


        try:
            if not Valid_choices: # If the cell have no Neighbors (mskiins hahaha)
                if stack_history:
                    NewOrigin = stack_history.pop() # Get the new OriginNode from the History
                    OriginNode = NewOrigin # Use the new OriginNode
                    Origin_CallBack = stack_history[-1] # Use the New Call Back node
                    
                    NotValid.add(tuple(OriginNode))
                    DrawingFunc(OriginNode[0], OriginNode[1])
                    pass
                else:
                    ClearTerminal()
                    End_Time = int(time.time() - start_time)
                    print(Fore.GREEN+Style.BRIGHT+f"---> Maze got generated Successfully !!",end="")
                    Algorithm_status = False
                    
                    print(Fore.BLUE+Style.BRIGHT+f"""
{Fore.CYAN}[/] -  Origin Cell     : {Fore.MAGENTA}{OriginNode}{Fore.BLUE}
{Fore.CYAN}[/] -  CallBack Cell   : {Fore.MAGENTA}{Origin_CallBack}{Fore.BLUE}
{Fore.CYAN}[/] -  Taken time (s)  : {Fore.MAGENTA}{End_Time}s{Fore.BLUE} | {Fore.MAGENTA}{float(time.time() - start_time)*1000}ms {Fore.BLUE}
{Fore.CYAN}[/] -  Detected Cells  : {Fore.MAGENTA}{len(NotValid)}{Fore.BLUE}
    
                          """)
                    pass
                    
                    
                    
                    
                    
                    
            if Valid_choices:
                stack_history.append(tuple(OriginNode)) # Get The OLD Origin
                RandomChoice = random.choice(Valid_choices)
                Origin_CallBack = OriginNode
                OriginNode = RandomChoice
                
                NotValid.add(tuple(RandomChoice))
                stack_history.append(RandomChoice) # Get The new Origin
                DrawingFunc(OriginNode[0], OriginNode[1])
                
            
        except Exception as error:
            ClearTerminal()
            print(Fore.RED+Style.BRIGHT+f"Error Detected. {error}")
            pass
        





    # just for filltring the neighbors (jiran wkda rak fahm hoohoo)
    def Filtring_Function(cordinates):
        x, y = cordinates

        if x < 0 or y < 0: # Small Than the screen
            # print(f"[{tuple(cordinates)}] {x} > 0, {y} > 0   | X-Y")
            return False
        
        if x >= screen_x/celle_size or y >= screen_y/celle_size: # Biiger than the screen
            # print(f"[{tuple(cordinates)}] {x * celle_size} >= {screen_x}, {y * celle_size} >= {screen_y}   | Border-Screen")
            return False
        
        if tuple(cordinates) in NotValid : # NotValid Cell
            # print(f"[{tuple(cordinates)}], In NotValid {tuple(cordinates) in NotValid}  - In DeadList {tuple(cordinates) in DeadCell}   | Lists")
            return False

        if tuple(cordinates) in DeadCells: # Dead Cell
            print(f" ---- >Dead Cell {cordinates}")
            if Show_Details:
                Pos_x, Pos_y = cordinates[0], cordinates[1]
                pygame.draw.circle(screen, "RED", ((Pos_x * celle_size) + celle_size//2, (Pos_y * celle_size) + celle_size//2), 15)            
                return False


        if cordinates == OriginNode or cordinates == Origin_CallBack: # The Same cell
            return False
        return True


    
    
    
    
    def DrawingFunc(Pos_x, Pos_y): # Drawing funciton.
        # print(Pos_x, Pos_y)
        
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
    
    
    
        # Show The Details Lines And Dead Cells Styles
    
        if Show_Details: 
            
            # Show The Origin Cell
            pygame.draw.circle(screen, colors_root["Origin-node"], ((OriginNode[0] * celle_size) + celle_size / 2 , (OriginNode[1] * celle_size) + celle_size / 2), 2)
            
            # Change Old origin color
            pygame.draw.circle(screen, colors_root["walls-color"], ((Origin_CallBack[0] * celle_size) + celle_size / 2, (Origin_CallBack[1] * celle_size) + celle_size / 2), 2)
            
            # Draw New Origin Node
            pygame.draw.circle(screen, colors_root["Origin-node"], ((Pos_x * celle_size) + celle_size / 2, (Pos_y * celle_size) + celle_size / 2), 2)
        
            # Connect them by a line ( Rawabit 2ossariya rak fahm 3liya hhhhhh. ana 7amd 3arf 3arf)
            pygame.draw.line(screen, "BLUE",
                            ((OriginNode[0] * celle_size) + celle_size/2, (OriginNode[1] * celle_size) + celle_size/2), # First Point Pos (Line start)
                            ((Origin_CallBack[0] * celle_size) + celle_size/2, (Origin_CallBack[1] * celle_size) + celle_size/2)  # Second Point Pos (Line End)
                            )
    pygame.display.update()
    clock.tick(60)
    pass





