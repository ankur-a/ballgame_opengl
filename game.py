from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys, os, random, time

window = 0
width, height = 300, 300
verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

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
def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluLookAt(0,1,0,
              0,1,-1,
              0,2,0)
    gluPerspective(170, 1, 0.1, 50.0)
    glTranslatef(0.0,0.0, -1)
    
    
def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	# Draw something
	refresh2d(width, height)
	glColor3f(0.0, 0.4, 0.7)
	
	Cube()
	glutSwapBuffers()
	
	
glutInit()

glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0,0)
window = glutCreateWindow("Hello")

glutDisplayFunc(draw)
glutIdleFunc(draw)
glutMainLoop()
