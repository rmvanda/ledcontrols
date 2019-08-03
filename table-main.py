import json
import logging
import os

import webcolors

from flask import Flask, request, session, g, render_template, flash, current_app, send_from_directory

from ledcontrol import *

import memcache

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
logging.basicConfig(filename="table.log",level=logging.WARN)

NEW_HAND = True
BLINDER  = 0 
LAST_SEAT= 0
BACKGROUND_COLOR = [0,0,0]
CURRENT_COLOR = [255,255,255]
DEALER = 0 
# quick color name

def qcn(color):
    return list(webcolors.name_to_rgb(color))

# quick color from hex
def qch(color):
    return list(webcolors.hex_to_rgb(color))


@app.route("/")
def index():
    return render_template("table.html")

@app.route("/light", methods=['GET','POST'])
def lightSeat(): 
    global NEW_HAND
    global BLINDER
    global LAST_SEAT
    global BACKGROUND_COLOR
    global CURRENT_COLOR 
    global DEALER 
    if NEW_HAND: 
        if BLINDER == 0:
            color = qcn("white")
            DEALER = request.args['seat']
        if BLINDER == 1:
            color = qcn("yellow")
        if BLINDER == 2: 
            color = qcn("blue")
            NEW_HAND=False
            CURRENT_COLOR = a.getRandUnbiased()
        BLINDER+=1; 

        a.lightSection(color, request.args['seat'])
    else:
        if BLINDER == 3:
            BLINDER = 0
        else:
            if(LAST_SEAT != DEALER):
                a.lightSection(BACKGROUND_COLOR, LAST_SEAT)
            else: 
                a.lightSection([255,255,255], DEALER)

        a.lightSection(CURRENT_COLOR, request.args['seat'])
        LAST_SEAT = request.args['seat']
    return json.dumps({'sucess':True}), 200, {'ContentType':'application/json'} # lazy? maybe. 


@app.route("/reset", methods=['GET'])
def reset(): 
    mc.set("c",0)
    global NEW_HAND
    global BLINDER
    global LAST_SEAT
    global BACKGROUND_COLOR
    global CURRENT_COLOR 
    global DEALER
    DEALER = 0
    NEW_HAND = True 
    BLINDER  = 0 
    color = a.getRandUnbiased()
    BACKGROUND_COLOR = color
    a.ringOn(color)
    return render_template("table.html")

@app.route("/showtime")
def clutchTest():
    rgb = a.getRandUnbiased()
    mc.set("c",1)
    while mc.get('c'): 
        a.showtime(rgb)
    a.setAll(rgb)
    return json.dumps({'sucess':True}), 200, {'ContentType':'application/json'} # lazy? maybe. 

@app.route("/shimmer")
def shimmerTest():
    mc.set('c',1)
    a.shimmerRandom()
    return json.dumps({'sucess':True}), 200, {'ContentType':'application/json'} # lazy? maybe. 

@app.route("/stop")
def stop():
    mc.set('c',0)
    return json.dumps({'sucess':True}), 200, {'ContentType':'application/json'} # lazy? maybe. 


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000); 
