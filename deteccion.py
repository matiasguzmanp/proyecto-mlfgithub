import cv2
import numpy as np
import matplotlib.pyplot as plt
import datetime

#Clase que contiene las funciones necesarias para realizar la deteccion y procesamiento de la imagen
class BoardDetector:
    #Se inician las variables que contendrán las imagenes, contornos y posiciones
    def __init__(self, img, img_original):
        self.img = img
        self.img_original = img_original
        self.centros = []
        self.mask = np.zeros(img.shape)
        self.img_boundingboxes = np.zeros(img.shape)
        self.contours=[]
        self.center_cuadrado= None
        self.center_img= None

    #Crea una mascara de la imagen con los colores de entre los lower y upper color
    def mask_image(self, lower_color, upper_color):
        img = np.copy(self.img)
        self.mask = cv2.inRange(img, lower_color, upper_color)

    #Busca los contornos de la mascara de la imagen obtenida.
    def buscar_contornos(self):
        self.img_boundingboxes=np.copy(self.img_original)
        contours, hierarchy = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = contours
        buenos_contornos = []
        for contorno in self.contours:
            if cv2.contourArea(contorno) >= 100:
                buenos_contornos.append(contorno)
        self.contours = buenos_contornos

        for contorno in self.contours:
            x, y, w, h = cv2.boundingRect(contorno)

            self.center_cuadrado=np.array([int((2*x+w)/2),int((2*y+h)/2)])
            self.center_img=np.array([160,120])
            self.centros.append(self.center_cuadrado)
            cv2.rectangle(self.img_boundingboxes, (x, y), (x+w, y+h), color=(255,0,0), thickness=1)
            cv2.circle(self.img_boundingboxes,self.center_cuadrado, radius=1, color=(0, 0, 255), thickness=3)
            cv2.circle(self.img_boundingboxes, self.center_img, radius=1, color=(255, 100, 100), thickness=3)
        print("Se ha(n) detectado ", len(self.contours), " contorno(s)")
        
        #cv2.imshow('test', self.img_boundingboxes)
