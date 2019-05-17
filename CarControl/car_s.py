import requests
import numpy as np
import cv2
from LineDetection.LineFollowing import *
import time
import threading

deafult_link_actions = ''
default_link_stream = ''
default_link_cali = ''
cap = None
lf = None
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
    global cap,deafult_link_actions,default_link_stream,lf,time_to_wait,default_link_cali,time_to_wait_cali
    ip ='192.168.0.'+ip
    deafult_link_actions = 'http://'+ip+':8000/run/'
    default_link_stream =  'http://'+ip+':8080/'
    default_link_cali = 'http://' + ip + ':8000/cali/'
    cap = cv2.VideoCapture( default_link_stream +'?action=stream' )
    lf = LineFollowing()
    time_to_wait = 0.1
    time_to_wait_cali = 4

    '''
    hilo = threading.Thread(name='frame_thread',
            target=display_frame)
    hilo.start()

    '''
    print(deafult_link_actions)
    print(default_link_stream)
    print(default_link_cali)

    #while(True):
    
    #request_action('long_lf')

    #while(True):
    #    request_action('fw')
    recognize_action()



    '''
        fw -> foward
        lf -> left
        rg -> right
        st -> stop
    '''
def recognize_action():
    while(True):
        action = get_action_prom()
        print(action)
        state = get_state()

        #action e (lt_rg, fw)
        if action == 'lf' or action == 'fw' or action == 'rg' or action == 'bw':
            request_action(action)
        if action == 'lt_rg':
            request_action(state)
'''
        fw -> foward
        lf -> left
        rg -> right
        st -> stop
        long_lf -> long left
        long_rg -> long right
''' 
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
    if action == 'long_lf':
        print('long')
        send_action('100',msg='speed')
        send_action('fwleft')
        r = requests.get(default_link_cali)
        send_cali('bwcali')
        send_cali('bwcalileft')
        time.sleep(time_to_wait_cali)
        send_cali('bwcalileft')
        r = requests.get(deafult_link_actions)
        send_action('40',msg='speed')
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
    dic_t = {}
    limit = 12

    while limit > 0:
        print(dic_t)
        response = get_action()

        if response in dic_t:
            dic_t[response] = dic_t[response] + 1
        else:
            dic_t[response] = 1
        limit = limit - 1
    
    max_number, max_id = 0,''


    for key in dic_t:
        value = dic_t[key]
        if value > max_number:
            max_number = value
            max_id = key
   
    return max_id

def get_action():
    frame = request_frame()

    if frame is None or not frame.any():
        print('get_action -> Frame is None nea')
        return None

    [lines_edges, p_next_action_c, p_next_action, last_valid_slope] = lf.next_action(frame)

    if p_next_action_c == 'MLR':
        return 'lt_rg'
    elif p_next_action_c == 'ML':
        return 'lf'
    elif p_next_action_c == 'MR':
        return 'rg'
    elif p_next_action_c == 'MF':
        return 'fw'
    else:
        #Example p_next_action == 'do_nothing'
        return 'bw'    
        

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