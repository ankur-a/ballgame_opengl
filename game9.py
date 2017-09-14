import pygame
from pygame.locals import *
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
start=time.time()
tag=True
vertices = [
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    ]
z_inc=[]
lane=[]
edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )
colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )

ground_vertices = (
    (10,-1.1,50),
    (10,-1.1,-160),
    (-10,-1.1,-160),
    (-10,-1.1,50)
    )
back=(
    (500,-10,-400),
    (500,200,-400),
    (-500,200,-400),
    (-500,-10,-400)
    )
leftside=(
    (-11,-1.1,50),
    (-11,-1.1,-160),
    (-300,-1.1,-160),
    (-300,-1.1,50)
    )
rightside=(
    (300,-1.1,50),
    (300,-1.1,-160),
    (11,-1.1,-160),
    (11,-1.1,50)
    )
    
textures=[(1,0),(1,1),(0,1),(0,0)]
textures1=[(4,0),(4,42),(0,42),(0,0)]
textures2=[(29,0),(29,21),(0,21),(0,0)]
def cullface():
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glFrontFace(GL_CW)
    glEnable(GL_DEPTH_TEST)
def Ground():
    
    glBegin(GL_QUADS)

    x = 0
    for vertex in ground_vertices:
        
        #glColor3fv((0,1,1))
        glTexCoord2f(textures1[x][0],textures1[x][1])
        glVertex3fv(vertex)
        x+=1 
    glEnd()

def Background():
    
    glBegin(GL_QUADS)

    x = 0
    for vertex in back:
        
        #glColor3fv((0,1,1))
        glTexCoord2f(textures[x][0],textures[x][1])
        glVertex3fv(vertex)
        x+=1 
    glEnd()

def left():
    
    glBegin(GL_QUADS)

    x = 0
    for vertex in leftside:
        
        
        glTexCoord2f(textures2[x][0],textures2[x][1])
        glVertex3fv(vertex)
        x+=1 
    glEnd()

def right():
    
    glBegin(GL_QUADS)

    x = 0
    for vertex in rightside:
        
        
        glTexCoord2f(textures2[x][0],textures2[x][1])
        glVertex3fv(vertex)
        x+=1 
    glEnd()


def texture(case):
    # Load the textures
    if(case==1):
        texture_surface = pygame.image.load("ground.jpg")
    elif(case==2):
        texture_surface = pygame.image.load("woodenbox.jpg")
    elif(case==3):
        texture_surface = pygame.image.load("sphere.jpg")
    elif(case==4):
        texture_surface = pygame.image.load("background1.jpg")
    elif(case==5):
        texture_surface = pygame.image.load("grass.jpg")
    # Retrieve the texture data
    texture_data = pygame.image.tostring(texture_surface, 'RGB', True)
    # Generate a texture id
    texture_id = glGenTextures(1)
    # Tell OpenGL we will be using this texture id for texture operations
    glBindTexture(GL_TEXTURE_2D, texture_id)
    # Tell OpenGL how to scale images
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
    
    # Tell OpenGL that data is aligned to byte boundries
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    # Get the dimensions of the image
    width, height = texture_surface.get_rect().size
    # Upload the image to OpenGL
    glTexImage2D( GL_TEXTURE_2D,
             0,
             3,
             width,
             height,
             0,
             GL_RGB,
             GL_UNSIGNED_BYTE,
             texture_data)
    
def Cube(i):
    global tag
    glBegin(GL_QUADS)
    if(tag==True):
        z_inc[i]+=1.5
    for surface in surfaces:
        x = 0

        for vertex in surface:
            
            #glColor3fv(colors[x])
            glTexCoord2f(textures[x][0],textures[x][1])
            glVertex3f(vertices[vertex][0]+lane[i],vertices[vertex][1],vertices[vertex][2]+z_inc[i])
            x+=1
        
    glEnd()
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3f(vertices[vertex][0]+lane[i],vertices[vertex][1],vertices[vertex][2]+z_inc[i])
    glEnd()


def sphere():
    quadric=gluNewQuadric()
    gluQuadricTexture(quadric,1)
    glEnable(GL_LIGHTING)
    lightZeroPosition = [0.,4.,100.,1.]
    lightZeroColor = [0.8,1.0,0.8,1.0] #green tinged
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)
    color = [1.0,1.,0.,1.]
##    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
    gluSphere(quadric,1.2,32,32)
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)

def main():
    global tag
    count=0
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor (1.0, 1.0, 1.0, 1.0)
    gluPerspective(65, (display[0]/display[1]), 0.1, 401.0)
    glTranslatef(0,-5, 0)
    glRotatef(10, 1, 0, 0)
    dist=1
    x_move = 0
    y_move = 0
    x_mov = 0
    y_mov = 0
    for i in range (12):
        t=random.randint(-8,8)
        lane.append(t)
        z_inc.append(-(dist)*10)
        dist+=1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = 0.5
                    
                if event.key == pygame.K_RIGHT:
                    x_move = -0.5
                    

                if event.key == pygame.K_UP:
                    y_move = -0.5
                if event.key == pygame.K_DOWN:
                    y_move = 0.5


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_move = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_move = 0
##        x = glGetDoublev(GL_MODELVIEW_MATRIX)
##        camera_x = x[3][0]
##        camera_y = x[3][1]
##        camera_z = x[3][2]
##        print camera_x,camera_y,camera_z
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)


        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        texture(1)
        Ground()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        texture(4)
        Background()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        texture(5)
        left()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        texture(5)
        right()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        
        glPushMatrix()
        cullface()
        glEnable(GL_TEXTURE_2D)
        texture(2)
        glTranslatef(0,0, -50)
        for i in range (12):
            Cube(i)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_CULL_FACE)
        glDisable(GL_DEPTH_TEST)
        glPopMatrix()


        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        texture(3)
        if(tag==True):
            x_mov+=x_move
            glTranslatef(-x_mov,0, -15)
            sphere()
        else:
            if(count<3):
                glTranslate(-x_mov,count,-15)
                count+=1
                sphere()
            elif(count<6):
                glTranslate(-x_mov,(6-count),-15)
                count+=1
                sphere()        
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        

        glTranslatef(x_move,y_move,0)
        

        
        
        
        pygame.display.flip()
        pygame.time.wait(1)
        if(abs(z_inc[1]-35)<=2.2):
            if(abs(lane[1]+x_mov)<2.2):
                glClearColor (1.0, 1.0, 0.0, 0.0)
                tag=False
                print(int(time.time()-start))
        if(abs(z_inc[0]-35)<=2.2):
            if(abs(lane[0]+x_mov)<2.2):
                glClearColor (1.0, 1.0, 0.0, 0.0)
                tag=False
                print(int(time.time()-start))
        
        if(x_mov<-9.5 or x_mov>9.5):
            glClearColor (1.0, 1.0, 0.0, 0.0)
            tag=False
            print(int(time.time()-start))
        if 47<=z_inc[0]:
            z_inc.pop(0)
            lane.pop(0)
            t=random.randint(-8,8)
            lane.append(t)
            z_inc.append(z_inc[-1]-10)
            

main()
