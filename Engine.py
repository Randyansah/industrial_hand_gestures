import pyfirmata
import time

comm_port='COM4'

board=pyfirmata.Arduino(comm_port)

off_state=board.get_pin('d:13:o')
ind_motor=board.get_pin('d:12:o')
on_state=board.get_pin('d:11:o')


def gesture_count(total):
    if total==0:
        off_state.write(0)
        ind_motor.write(1)
        on_state.write(1)
        time.sleep(1.0)   
       
    elif total==5:
        off_state.write(1)
        ind_motor.write(0)
        on_state.write(0)
        
