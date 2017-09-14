import pygame
from pygame.locals import *
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pyglet
import pywavefront
base_middle={"vert":[[-10,-1,0],[10,-1,0],[10,-1,-20],[-10,-1,-20]],
      "tex":[[0,0],[4,0],[4,4],[0,4]]
      }

base_left={"vert":[[-100,-1,0],[-10,-1,0],[-10,-1,-20],[-100,-1,-20]],
      "tex":[[0,0],[18,0],[18,4],[0,4]]
      }

base_right={"vert":[[10,-1,0],[100,-1,0],[100,-1,-20],[10,-1,-20]],
      "tex":[[0,0],[18,0],[18,4],[0,4]]
      }
back={"vert":[[-500,-20,-400],[500,-20,-400],[500,200,-400],[-500,200,-400]],
      "tex":[[0,0],[1,0],[1,1],[0,1]]
      }
cube_vertices = [
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    ]
cube_vertices1 = [
    (1, -1, -1),
    (1, 2, -1),
    (-1, 2, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 2, 1),
    (-1, -1, 1),
    (-1, 2, 1)
    ]
cube_edges = (
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

cube_surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

pyramid_vertices = [
    (0, 1, 0),
    (1, -1, 1),
    (1, -1, -1),
    (-1, -1, -1),
    (-1, -1, 1)
    ]
pyramid_vertices1 = [
    (0, 2, 0),
    (1, -1, 1),
    (1, -1, -1),
    (-1, -1, -1),
    (-1, -1, 1)
    ]
pyramid_edges = (
    (0,1),
    (0,2),
    (0,3),
    (0,4),
    (1,2),
    (2,3),
    (3,4),
    (4,1)
    )

pyramid_surfaces = (
    (1,2,3,4),
    (0,1,2),
    (0,2,3),
    (0,3,4),
    (0,4,1)
    )

textures=[(1,0),(1,1),(0,1),(0,0)]
textures3=[(0.5,1),(0,0),(1,0)]



stem = pywavefront.Wavefront('stem.obj')
leaf = pywavefront.Wavefront('leaf.obj')
z_base=[30,10,-10,-30,-50,-70,-90,-110,-130,-150]
z_tree=[20,-60,-140,-220,-300]
tag=True
lane=[]
z_inc=[]
ch=[]
global texture_id,game
u=1
a=0.00001
rot=0

def quadrilateral(arr,z):
    vert=arr["vert"]
    tex=arr["tex"]
    glBegin(GL_QUADS)
    for i in range (4):
        glTexCoord2fv(tex[i])
        glVertex3f(vert[i][0],vert[i][1],vert[i][2]+z)
    glEnd()

def Cube(ind):
    glBegin(GL_QUADS)
    for surface in cube_surfaces:
        x = 0

        for vertex in surface:
            glTexCoord2f(textures[x][0],textures[x][1])
            if(ch[ind]==0):
                glVertex3f(cube_vertices[vertex][0]+lane[ind],cube_vertices[vertex][1],cube_vertices[vertex][2]+z_inc[ind])
            else:
                glVertex3f(cube_vertices1[vertex][0]+lane[ind],cube_vertices1[vertex][1],cube_vertices1[vertex][2]+z_inc[ind])
            x+=1    
    glEnd()
    glColor4f(0.0,0.0,0.0,1.0)
    glBegin(GL_LINES)
    for edge in cube_edges:
        for vertex in edge:
            if(ch[ind]==0):
                glVertex3f(cube_vertices[vertex][0]+lane[ind],cube_vertices[vertex][1],cube_vertices[vertex][2]+z_inc[ind])
            else:
                glVertex3f(cube_vertices1[vertex][0]+lane[ind],cube_vertices1[vertex][1],cube_vertices1[vertex][2]+z_inc[ind])
    glEnd()
    glColor4f(1.0,1.0,1.0,1.0)

def Pyramid(ind):
    glBegin(GL_QUADS)
    x=0
    for vertex in pyramid_surfaces[0]:
        glTexCoord2f(textures[x][0],textures[x][1])
        if(ch[ind]==2):
            glVertex3f(pyramid_vertices[vertex][0]+lane[ind],pyramid_vertices[vertex][1],pyramid_vertices[vertex][2]+z_inc[ind])
        else:
            glVertex3f(pyramid_vertices1[vertex][0]+lane[ind],pyramid_vertices1[vertex][1],pyramid_vertices1[vertex][2]+z_inc[ind])
        x+=1
    glEnd()
    glBegin(GL_TRIANGLES)
    for i in range (1,5):
        x = 0
        for vertex in pyramid_surfaces[i]:
            glTexCoord2f(textures3[x][0],textures3[x][1])
            if(ch[ind]==2):
                glVertex3f(pyramid_vertices[vertex][0]+lane[ind],pyramid_vertices[vertex][1],pyramid_vertices[vertex][2]+z_inc[ind])
            else:
                glVertex3f(pyramid_vertices1[vertex][0]+lane[ind],pyramid_vertices1[vertex][1],pyramid_vertices1[vertex][2]+z_inc[ind])
        
            x+=1
        
    glEnd()
    glColor4f(0.0,0.0,0.0,1.0)
    glBegin(GL_LINES)
    for edge in pyramid_edges:
        for vertex in edge:
            if(ch[ind]==2):
                glVertex3f(pyramid_vertices[vertex][0]+lane[ind],pyramid_vertices[vertex][1],pyramid_vertices[vertex][2]+z_inc[ind])
            else:
                glVertex3f(pyramid_vertices1[vertex][0]+lane[ind],pyramid_vertices1[vertex][1],pyramid_vertices1[vertex][2]+z_inc[ind])
        
    glEnd()
    glColor4f(1.0,1.0,1.0,1.0)

def sphere():
    quadric=gluNewQuadric()
    gluQuadricTexture(quadric,GLU_TRUE)
    gluSphere(quadric,1.2,64,64)


def texture(case):
    global texture_id
    # Load the textures
    if(case==1):
        texture_surface = pygame.image.load("ground.jpg")
    elif(case==2):
        texture_surface = pygame.image.load("woodenbox1.jpg")
    elif(case==3):
        texture_surface = pygame.image.load("sphere5.jpg")
    elif(case==4):
        texture_surface = pygame.image.load("background1.jpg")
    elif(case==5):
        texture_surface = pygame.image.load("grass.jpg")
    elif(case==6):
        texture_surface = pygame.image.load("pyramid1.jpg")
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

def update(dt):
    global u,a,rot
    increment=u
    u+=a*dt
    r_increment=increment*150/3.14
    rot += r_increment
    if rot > 720:
        rot = 0
    for i in range(10):
        z_base[i]+=increment
    if(z_base[0]>30):
        z_base.pop(0)
        z_base.append(z_base[-1]-20)
    for i in range(5):
        z_tree[i]+=2*increment
    if(z_tree[0]>30):
        z_tree.pop(0)
        z_tree.append(z_tree[-1]-80)
    for i in range(12):
        z_inc[i]+=increment
    if(z_inc[0]>0):
        z_inc.pop(0)
        ch.pop(0)
        lane.pop(0)
        t=random.randint(-8,8)
        lane.append(t)
        ch.append(random.randint(0,3))
        z_inc.append(z_inc[-1]-10)
def score_display():
    label=pyglet.text.Label("SCORE:",
                            font_name="Times New Roman",
                            font_size=200,
                            x=100,y=100,
                            anchor_x="center",anchor_y="center")

    label.draw()

def main():
    global texture_id,ch,tag,rot,a,game
    
    
    over=True
    dist=10
    count=0
    dt=0
    pygame.init()
    pygame.mixer.music.load("sound.wav")
    pygame.mixer.music.play(-1)
    t_prev=pygame.time.get_ticks()
    display = (1000,920)
    game=pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor (1.0, 1.0, 1.0, 1.0)
    gluPerspective(65, (display[0]/display[1]), 0.1, 470.0)
    glTranslatef(0,-5, 0)
    glRotatef(10, 1, 0, 0)
    x_move = 0
    x_mov = 0
    for i in range (12):
        t=random.randint(-8,8)
        lane.append(t)
        ch.append(random.randint(0,3))
        z_inc.append(-(dist)*10)
        dist+=1
    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = 0.5+a*dt
                    
                if event.key == pygame.K_RIGHT:
                    x_move = -0.5-a*dt
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_move = 0

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        texture(4)
        quadrilateral(back,0)
        glDisable(GL_TEXTURE_2D)
        glDeleteTextures(texture_id)
        glPopMatrix()

        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        texture(1)
        for z in z_base:
            quadrilateral(base_middle,z)
        glDisable(GL_TEXTURE_2D)
        glDeleteTextures(texture_id)
        glPopMatrix()

        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        texture(5)
        for z in z_base:
            quadrilateral(base_left,z)
        glDisable(GL_TEXTURE_2D)
        glDeleteTextures(texture_id)
        glPopMatrix()

        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        texture(5)
        for z in z_base:
            quadrilateral(base_right,z)
        glDisable(GL_TEXTURE_2D)
        glDeleteTextures(texture_id)
        glPopMatrix()

        
        glPushMatrix()
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        texture(2)
        for i in range (12):
            if(ch[i]==0 or ch[i]==1):
                Cube(i)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_CULL_FACE)
        glDisable(GL_DEPTH_TEST)
        glDeleteTextures(texture_id)
        glPopMatrix()


        glPushMatrix()
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        texture(6)
        for i in range (12):
            if(ch[i]==2 or ch[i]==3):
                Pyramid(i)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_CULL_FACE)
        glDisable(GL_DEPTH_TEST)
        glDeleteTextures(texture_id)
        glPopMatrix()

        glPushMatrix()
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        texture(3)
        
        
        if(tag==True):
            x_mov+=x_move
            glTranslatef(-x_mov,0, -15)
            if(x_move>0):
                glRotatef(15, 0, 0, 1)
            elif(x_move<0):
                glRotatef(-15, 0, 0, 1)
            glRotatef(rot, 1, 0, 0)
            sphere()
        else:
            if(count<3):
                glTranslate(-x_mov,count,-15)
                sphere()
            elif(count<6):
                glTranslate(-x_mov,(6-count),-15)
                sphere()
            elif(count==20):
                over=False
            count+=1
        
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_CULL_FACE)
        glDisable(GL_DEPTH_TEST)
        glDeleteTextures(texture_id)
        glPopMatrix()

        
        for z in z_tree:
            glPushMatrix()
            glEnable(GL_CULL_FACE)
            glCullFace(GL_BACK)
            glFrontFace(GL_CW)
            glEnable(GL_DEPTH_TEST)
            glScale(0.8,0.8,0.8)
            glTranslatef(-30+x_mov,-5,z-30)
            glColor4f(0.5,0,0,1)
            stem.draw()
            glColor4f(0,1,0,1)
            leaf.draw()
            glDisable(GL_CULL_FACE)
            glDisable(GL_DEPTH_TEST)
            glColor4f(1,1,1,1)
            glPopMatrix()

            glPushMatrix()
            glEnable(GL_CULL_FACE)
            glCullFace(GL_BACK)
            glFrontFace(GL_CW)
            glEnable(GL_DEPTH_TEST)
            glScale(0.8,0.8,0.8)
            glTranslatef(30+x_mov,-5,z-30)
            glColor4f(0.5,0,0,1)
            stem.draw()
            glColor4f(0,1,0,1)
            leaf.draw()
            glDisable(GL_CULL_FACE)
            glDisable(GL_DEPTH_TEST)
            glColor4f(1,1,1,1)
            glPopMatrix()
        glTranslatef(x_move,0,0)
        t_new=pygame.time.get_ticks()
        dt=t_new-t_prev
        if(tag==True):
            update(dt)
        t_prev=t_new
        pygame.display.flip()
        if(abs(z_inc[1]+15)<=2.3):
            if(abs(lane[1]+x_mov)<2.18):
                tag=False
        if(abs(z_inc[0]+15)<=2.3):
            if(abs(lane[0]+x_mov)<2.18):
                tag=False
        if(x_mov<-9.5 or x_mov>9.5):
            tag=False
        score_display()

        

main()
print("SCORE:",int(pygame.time.get_ticks())//1000)
pygame.quit()

