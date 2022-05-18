from datetime import datetime
import traceback
from flask import Flask,request
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import time,requests,json
from threading import Thread




app = Flask(__name__)


queues = []
queue = Queue()
thread_pool = ThreadPoolExecutor()





@app.route('/motion', methods=['POST'])
def motion():
    try:
        data = request.json
        res = queue.put(data)
    except:
        traceback.print_exc()

    return "{ 'response': 'True' }"





def camera_thread(queue):
    while True:
        try:
            temp = queue.get_nowait()
            print(f'in thread{queue} and {temp}')
        except:
            pass#print('EMPTY QUEUE')
            #traceback.print_exc()
        
        
        
       







for _ in range(4):
    temp = Queue()
    queues.append(temp)
    thread_pool.submit(camera_thread, temp )



def controller_task(args):
    queues = args[0]
    queue = args[1]
    motion_lists = []


    for _ in queues:
        motion_lists.append([])
    

    while(True):
        try:

            if queue.empty():
                res = False
            else:
                res = queue.get_nowait()
            
            if res:
                index = int(res['index'])
                print(index)
                date = res['date']
                print(date)
                motion_lists[index].append(date)

            for i, list in enumerate(motion_lists):
                if len(list) > 0:
                    res = queues[i].put(list.pop(0))
                    print(queues[i])
                    
        except:
            traceback.print_exc()

        


thread_pool.submit(controller_task,[queues,queue])

app.run(host='localhost', port=5000, debug=True, threaded=True)



"""
        for entry in queues:
            try:
                entry.put(datetime.now())
            except:
                traceback.print_exc()
        time.sleep(1)"""