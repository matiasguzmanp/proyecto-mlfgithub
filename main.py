import cv2
from deteccion import BoardDetector
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import sys
import time

pos_encaje_cuadrado = np.array([210,50,-5])

def main():

    sys.path.insert(0, os.path.abspath('..'))

    from client import ClientWrapper

    c = ClientWrapper()  # Si no se especifica url, pide al 'localhost' (misma raspi)
    img_frame = c.get_single_frame()
    img_hsv = cv2.cvtColor(img_frame, cv2.COLOR_BGR2HSV)
    det = BoardDetector(img_hsv, img_frame)
    img = det.img


    #fig, ax = plt.subplots(2, 2)

    #ax[0, 0].imshow(img, cmap="gray")

    # Calculamos la mascara y la aplicamos
    # deben encontrar limites adecuados para el color que les interese
    lower_color = np.array([165, 86, 80])
    upper_color = np.array([180, 255, 255])

    det.mask_image(lower_color, upper_color)
    #ax[0, 1].imshow(det.mask, cmap="gray")
    det.buscar_contornos()
    #ax[1, 0].imshow(det.img_boundingboxes)

    print(det.centros)
    '''
    Transformada
    '''
    try:
        pix_a_mm=1.61
        centro_fig= det.center_cuadrado
        centro_img= det.center_img

        pos_fig_pix = centro_fig - centro_img
        pos_fig_mm = pos_fig_pix*pix_a_mm
        x,y = pos_fig_mm
        pos_fig_mm_al_r = np.array([-y,-x])
        pos_fig_mm_r = pos_fig_mm_al_r+np.array([170,0]) #posicion de la figura en el sistema de referencia del robot (mm)
        print(pos_fig_mm_r)
    except Exception as e:
        print('mala foto')


    def close(event):
        if event.key == 'q':
            plt.close(event.canvas.figure)

    plt.gcf().canvas.mpl_connect("key_press_event", close)
    plt.show()
    return pos_fig_mm_r

if __name__ == '__main__':
    main()
