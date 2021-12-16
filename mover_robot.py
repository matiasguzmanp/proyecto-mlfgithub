import sys
import deteccion
import main
import client
import numpy as np

sys.path.append('/home/pi/mlf/core')
from serial_control import SerialControl
from mk2robot import MK2Robot
# from core.serial_control import SerialControl #for pc
# from core.mk2robot import MK2Robot #for pc
import time

robot = MK2Robot(link_lengths=[55, 39, 135, 147, 66.3])
robot_serial = SerialControl(port='/dev/ttyUSB0')
# robot_serial = SerialControl("COM5") #for pc
robot_serial.open_serial()
posicion_encaje=np.array([240,50,10])

for i in range(2):
	posicion_pieza=main.main()
	x,y=posicion_pieza[0],posicion_pieza[1]
	offset_x = 0
	offset_y = 0
	offset_z = 0
	ang=90
	if y < 0 and x > 220:
		offset_y = 10
		offset_x = -22
		offset_z = 5
		ang=90
		posicion_encaje=np.array([220, -50, 10])
		print("cuadrante y>0, x>220")
		
	else:
		offset_y = -55
		offset_x = -20
		offset_z = 10
		ang=45
		print("otro cuadrante")
	posicion_pieza= np.array([int(x) + offset_x,-int(y) + offset_y, offset_z])
	

	robot_serial.write_servo(4,90)
	#va a pieza
	q0, q1, q2 = robot.inverse_kinematics(posicion_pieza[0], posicion_pieza[1], posicion_pieza[2])
	robot_serial.write_servo(1, 45 + int(q0))
	robot_serial.write_servo(2, 90 - int(q1))
	robot_serial.write_servo(3, q2 + int(q1))
	time.sleep(2)

	#prende iman
	robot_serial.write_servo(5,1)
	time.sleep(2)
	robot_serial.write_servo(3,30)
	time.sleep(1)
	robot_serial.write_servo(3,40)
	time.sleep(1)
	robot_serial.write_servo(3,50)
	time.sleep(1)
	robot_serial.write_servo(3,60)
	time.sleep(1)
	robot_serial.write_servo(3,70)
	time.sleep(1)
	#va a home
	robot_serial.write_servo(1, 45)
	robot_serial.write_servo(2, 90)
	robot_serial.write_servo(3, 90)
	robot_serial.write_servo(4,ang)
	time.sleep(2)
	#va a encaje
	q0, q1, q2 = robot.inverse_kinematics(posicion_encaje[0], posicion_encaje[1], posicion_encaje[2])
	robot_serial.write_servo(1, 45 + int(q0))
	robot_serial.write_servo(2, 90 - int(q1))
	robot_serial.write_servo(3, int(q2) + int(q1))
	time.sleep(2)
	#apaga iman
	robot_serial.write_servo(5,0)
	time.sleep(2)
	#va a home
	robot_serial.write_servo(1, 45)
	robot_serial.write_servo(2, 90)
	robot_serial.write_servo(3, 90)

