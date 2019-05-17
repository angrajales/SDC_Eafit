import requests
import numpy as np
import cv2
from LineDetection.LineFollowing import *
from SignalDetection.SignalRecollection import *

import time
import threading

deafult_link_actions = ''
default_link_stream = ''
default_link_cali = ''
cap = None
lf = None
sr = None
time_to_wait = None
time_to_wait_cali = None

def display_frame():
    line = LineFollowing()
    while(cap.isOpened()):      
        ret, frame = cap.read()
        if ret==True:       
            [line_edges, p_next_action, last_valid_slope] = line.next_action(frame)    
            cv2.imshow('frame',frame)
            cv2.waitKey(25)
        if 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
        else:
            continue;


def main(ip):
    global cap,deafult_link_actions,default_link_stream,lf,time_to_wait,sr,default_link_cali,time_to_wait_cali
    ip ='192.168.0.'+ip
    deafult_link_actions = 'http://'+ip+':8000/run/'
    default_link_stream =  'http://'+ip+':8080/'
    default_link_cali = 'http://' + ip + ':8000/cali/'
    cap = cv2.VideoCapture( default_link_stream +'?action=stream' )

    lf = LineFollowing()
    sr = SignalRecollection()

    time_to_wait = 0.1
    time_to_wait_cali = 1
    

    '''
    hilo = threading.Thread(name='frame_thread',
            target=display_frame)
    hilo.start()

    '''
    print(deafult_link_actions)
    print(default_link_stream)
    print(default_link_cali)

    recognize_action()


    '''
    0 -> Acciones correctivas
    1 -> no reconoce izq derecha 
    2 -> Derecha
    3 -> Izquierda
    '''


    '''
        fw -> foward
        lf -> left
        rg -> right
        st -> stop
    '''
def recognize_action():
    global_state = -1
    while(True):
        action_p, action_c = get_action_prom()
        state,area = get_state_frequency()
        state = str(state)
        print("AREA ---------------------->", area)
        if (state == '2' or state =='3'):
            if global_state == -1:
                global_state = state;
        print('STATE -> ',state, ' ACTION C -> ',action_c,' ACTION P -> ',action_p, ' GLOBAL STATE -> ', global_state )
        if not(global_state == -1) and area > 4000: 
            request_action(global_state)
            global_state = -1
        else:
            request_action(action_c)
        
'''
        fw -> foward
        lf -> left
        rg -> right
        st -> stop
        long_lf -> long left
        long_rg -> long right
''' 

def get_state_frequency():
    dic_t = {}
    limit = 12

    while limit > 0:
        print(dic_t)
        frame = request_frame()
        returned = sr.get_state(frame)

        if(len(returned) == 2):
            state,area = returned
        else:
            state = returned

        if state in dic_t:
            dic_t[state] = dic_t[state] + 1
        else:
            dic_t[state] = 1
        
        limit = limit - 1

    max_number, max_id = 0,''

    for key in dic_t:
        value = dic_t[key]
        if value > max_number:
            max_number = value
            max_id = key
   
    return max_id,area


def request_action(action):

    #/run/?action=fwstraight

    if action == 'fw':
        send_action('forward')
        time.sleep(time_to_wait)
        send_action('stop')
    if action == 'bw':
        send_action('backward')
        time.sleep(time_to_wait)
        send_action('stop')
    if action == 'lf':
        send_action('fwleft')
        send_action('forward')
        time.sleep(time_to_wait)
        send_action('stop')
        send_action('fwstraight')
    if action == 'rg':
        send_action('fwright')
        send_action('forward')
        time.sleep(time_to_wait)
        send_action('stop')
        send_action('fwstraight')
    if action == '2':
        send_action('80',msg='speed')
        send_action('fwstraight')
        send_action('forward')
        time.sleep(0.2)
        send_action('fwright')
        send_action('forward')
        time.sleep(1.2)
        send_action('fwstraight')
        send_action('fwleft')
        send_action('backward')
        time.sleep(1)
        send_action('40',msg='speed')
        send_action('fwright')
        send_action('forward')
        time.sleep(0.2)
        send_action('fwstraight')
        send_action('stop')
    if action == '3':
        send_action('80',msg='speed')
        send_action('fwstraight')
        send_action('forward')
        time.sleep(0.2)
        send_action('fwleft')
        send_action('forward')
        time.sleep(1.2)
        send_action('fwstraight')
        send_action('fwright')
        send_action('backward')
        time.sleep(1)
        send_action('40',msg='speed')
        send_action('fwleft')
        send_action('forward')
        time.sleep(0.2)
        send_action('fwstraight')
        send_action('stop')
    return




def send_action(action,msg='action'):
    payload = {msg:action}
    r = requests.get(deafult_link_actions, params=payload)
    print(r.status_code)

def send_cali(action):
    payload = {'action':action}
    r = requests.get(default_link_cali, params=payload)
    print(r.status_code)

'''
        lf -> left
        rg -> right
'''
def get_state():
    #TO DO
    return 'long_lf'


def get_action_prom():
    dic_p = {}
    dic_c = {}
    limit = 12

    while limit > 0:
        print(dic_p)
        print(dic_c)
        p_next_action,p_next_action_c = get_action()

        if p_next_action in dic_p:
            dic_p[p_next_action] = dic_p[p_next_action] + 1
        else:
            dic_p[p_next_action] = 1

        if p_next_action_c in dic_c:
            dic_c[p_next_action_c] = dic_c[p_next_action_c] + 1
        else:
            dic_c[p_next_action_c] = 1
        
        limit = limit - 1
    
    max_number, max_id_c = 0,''
    for key in dic_p:
        value = dic_p[key]
        if value > max_number:
            max_number = value
            max_id_c = key

    max_number, max_id_p = 0,''
    for key in dic_c:
        value = dic_c[key]
        if value > max_number:
            max_number = value
            max_id_p = key
   
    return max_id_c,max_id_p

def get_action():
    frame = request_frame()

    if frame is None or not frame.any():
        print('get_action -> Frame is None nea')
        return None

    [lines_edges, p_next_action_c, p_next_action, last_valid_slope] = lf.next_action(frame)

    if p_next_action == 'MLR':
        p_next_action =  'lt_rg'

    if p_next_action == 'MF':
        p_next_action = 'fw'

    if p_next_action_c == 'ML':
        p_next_action_c = 'lf'
    
    if p_next_action_c == 'MR':
        p_next_action_c = 'rg'

    if p_next_action == "do_nothing":
        #Example p_next_action == 'do_nothing'
        p_next_action,p_next_action_c = 'bw','bw'

    return p_next_action,p_next_action_c

def request_frame():
    if(cap.isOpened()):  
        ret, frame = cap.read()
        if ret==True:
            
            #cv2.imshow('frame',frame)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    return None
            return frame
        else:
            print('request_frame -> ret FALSE')
            return None
    else:
        print('request_frame -> CAP is no opened')
        return None
    

def exit():
    cap.release()
    cv2.destroyAllWindows()

main('101')