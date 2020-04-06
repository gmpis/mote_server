from flask import Flask, request  #, redirect, render_template
from mote import Mote
from os import system
import time

app = Flask(__name__)
mote = None

try:
    mote = Mote()
    mote.configure_channel(1, 16, False)
    mote.configure_channel(2, 16, False)
    mote.configure_channel(3, 16, False)
    mote.configure_channel(4, 16, False)
    m_sticks_mapping = {"L_ind": 1, "R_ind": 4, "DL_ind": 2, "DR_ind": 3}  # mapping locations installed to ports
except:
    print("Mote not connected")
    # exit(1)


@app.route('/')
def home():
    return "Hello world! \n Available endpoints: /select , /end , /off"


@app.route('/select')
def select():
    return f_page % ("#707f29", "75")


@app.route('/set')
def set_c():
    u_str = request.args.get("u_sel", default="#ff1122")
    ch_str = request.args.get("ch_sel", default="All")
    br_str = request.args.get("br_sel", default="75")

    br_parsed = int(br_str) * 0.01

    inp_arr = conv_str(u_str)

    if ch_str == "Left":
        for i in range(16):
            mote.set_pixel(m_sticks_mapping["L_ind"], i, inp_arr[0], inp_arr[1], inp_arr[2], br_parsed)
    elif ch_str == "Right":
        for i in range(16):
            mote.set_pixel(m_sticks_mapping["R_ind"], i, inp_arr[0], inp_arr[1], inp_arr[2], br_parsed)
    elif ch_str == "D_Left":
        for i in range(16):
            mote.set_pixel(m_sticks_mapping["DL_ind"], i, inp_arr[0], inp_arr[1], inp_arr[2], br_parsed)
    elif ch_str == "D_Right":
        for i in range(16):
            mote.set_pixel(m_sticks_mapping["DR_ind"], i, inp_arr[0], inp_arr[1], inp_arr[2], br_parsed)
    else:
        mote.set_all(inp_arr[0], inp_arr[1], inp_arr[2], br_parsed)

    mote.show()
    print("\t >> Applying :[" + str(inp_arr[0])+", "+ str(inp_arr[1])+", "+ str(inp_arr[2])+"] on : "+ch_str+", br: "+str(br_parsed))
    # redirect("/select")
    return "Done!" + f_page % ("#707f29", "75")


@app.route('/end')
def end():
    mote.clear()
    mote.show()
    return "Bye!"


@app.route('/off')
def powermng():
    if mote:
        mote.clear()
        mote.show()
        time.sleep(3)

    system("/usr/bin/sudo /sbin/poweroff -f")
    return "Bye!"


# helper function
def conv_str(i_str):
    """ fast hex to dec RGB conversion"""
    tmp_col_str = i_str.replace("%23", "")
    tmp_col_str = tmp_col_str.replace("#", "")

    r_str = tmp_col_str[:2]
    g_str = tmp_col_str[2:4]
    b_str = tmp_col_str[4:]

    r_num = int(r_str, 16)
    g_num = int(g_str, 16)
    b_num = int(b_str, 16)

    return [r_num, g_num, b_num]


f_page = """
<!DOCTYPE html> <html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Mote remote controll</title>
</head>
<body bgcolor="0066cc"> <center> <font color="#ffffff">
    <h1> Select a color </h1>
    <form action="/set">
        <input type="color" name="u_sel" value=\"%s\"> <br> <br>
        <input type="radio" name="ch_sel" value="Left"> Left
        <input type="radio" name="ch_sel" value="Right"> Right <br>
        <input type="radio" name="ch_sel" value="D_Left"> D_Left
        <input type="radio" name="ch_sel" value="D_Right"> D_Right <br>
        <input type="radio" name="ch_sel" value="All" checked> All <br> <br>
        <input type="range" name="br_sel" min="5" max="100" step="5" value=\"%s\"> Brightness <br>
        <br> <br> <input type="submit">
    </form> </font> </center>
<a href="/end"> Clear All</a>
</body> </html> """