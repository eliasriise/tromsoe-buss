from requests import get
from json import dumps, loads
from os import system
from datetime import datetime
from time import time

LINES = ['33', '34']
NUM_CALLS = 4
STOPS = {
    "UiT" : '52488',
    "Strandkanten" : '54599'
}
DEST_TEXT = {
    'UiT' : 'Fagereng via sentrum',
    'Strandkanten' : None
}

def in_lines(call):
    for line in LINES:
        if line == call:
            return True
    return False

def get_calls():
    stop = 'UiT' # Change this variable to choose stop
    
    response = get('https://tromsreise.no/api/stopPlace/NSR:StopPlace:' + STOPS[stop])
    now = datetime.now()
    json_r = loads(response.text)
    calls = json_r['calls']
    # print(dumps(calls, indent=2))
    system('clear')
    print('Showing calls: ')
    
    n_valid_calls = 0
    
    for c in calls:
        if not in_lines(c['public_line']) or not c['destination_text'] == DEST_TEXT[stop]:
            calls.remove(c)
        else:
            try:
                print('ETD ' + c['public_line'] + ': ' + c['expected_departure'] + ' (' + c['actual_departure'] + ')')
                n_valid_calls += 1
                if n_valid_calls >= NUM_CALLS:
                    break
            except:
                print('ETD ' + c['public_line'] + ': ' + None + ' (' + c['actual_departure'] + ')')

    print('Last updated: ' + str(now.strftime('%H:%M:%S')))
    
def main():
    ts_start = 0
    timeout = 20
    while (True):
        if time() < ts_start + timeout: # not 
            continue
        else:
            get_calls()
            ts_start = time()
            


if __name__ == '__main__':
    main()
