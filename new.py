import tkinter as ttk
from tkinter import *
from tkinter.ttk import Combobox 
from tkinter import messagebox ,filedialog
import os

import threading
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time

window = Tk()
window.state("zoomed")

s_base_path = "D:/SKROMAN_ADMIN_CONSOLE/SKROMAN/SK_CERT/"
f_base_path = "D:/SKROMAN_ADMIN_CONSOLE/SKROMAN/FINO_CERT/"

host_address = "a2n4hdipq41ly9-ats.iot.ap-south-1.amazonaws.com"

pub_topic = "NULL"
sub_topic = "NULL"

cert_1 = "NULL"
cert_2 = "NULL"
cert_3 = "NULL"

######## Back End ###############

def pub_clear():
    pub_box.delete(1.0, END)

def sub_Clear():
    sub_box.delete(1.0, END)

def hit_button():

    global client
    global is_connected

    get_pub_box_data = pub_box.get("1.0", "end-1c")
    print(get_pub_box_data)

    if client and is_connected:
        message = get_pub_box_data
        if message:
            client.publish(pub_topic, message, 1)
            print("Published message:", message)
        else:
            print("Please enter a message.")    


def certifica_path():

    global cert_1
    global cert_2
    global cert_3

    var_1 = 0
    var_2 = 0
    var_3 = 0     

    selected_path = client.get()  
    
    if selected_path == "SKROMAN": 

        files = filedialog.askopenfilenames(initialdir = "D:/SKROMAN_ADMIN_CONSOLE/SKROMAN/SK_CERT", title = 'Choose a File')

        for file in files:
            if file == s_base_path + "AmazonRootCA1.pem":
                cert_1 = file
                var_1 = 1   

            elif file == s_base_path + "private.pem.key":
                cert_2 = file
                var_2 = 1                  
                
            elif file == s_base_path + "certificate.pem.crt":
                cert_3 = file
                var_3 = 1 
               


    if(var_1 and var_2 and var_3 == 1):
        messagebox.showinfo("Success", "Certificates Are Selected!")
    else:
        messagebox.showerror("Error", "Certificates Aren't Selected Yet!")               

# MQTT Connection ============================================== 

client = None
is_connected = False     

def get_pub_message(client, userdata, message):
    sub_box.insert(INSERT, message.payload)   


def aws_button():

    global client
    global is_connected

    global pub_topic
    global sub_topic

    global cert_1
    global cert_2
    global cert_3

    root_ca_path        = cert_1
    private_key_path    = cert_2
    certificate_path    = cert_3

    pub_topic = topic_box.get() + "/HA/A/req"
    sub_topic = topic_box.get() + "/HA/E/ack"   

    print(root_ca_path)
    print(private_key_path)
    print(certificate_path)

    print(pub_topic)
    print(sub_topic)       

    while not is_connected:  # Continue attempting to connect until successful
        if client is None or not is_connected:
            client = AWSIoTMQTTClient(host_address)
            client.configureEndpoint(host_address, 8883)
            client.configureCredentials(root_ca_path, private_key_path, certificate_path)
            print("Connection attempt...")

            # Configure MQTT connection settings
            client.configureOfflinePublishQueueing(-1)
            client.configureDrainingFrequency(2)
            client.configureConnectDisconnectTimeout(30)
            client.configureMQTTOperationTimeout(30)

            # Connect to AWS IoT Core
            try:
                client.connect()
                is_connected = True  # Set the connection flag to True
                print("Connected to AWS IoT Core")
            except Exception as e:
                print("Failed to connect:", str(e))
                time.sleep(5)  # Delay between connection attempts

            # Subscribe to a topic
            client.subscribe(sub_topic, 1, get_pub_message)   


#Main Frame:
frame1 = Frame(window, height = 1000, width = 1700, bg = "white")
frame1.place(x = 0, y = 0)

# Console Title:
console_title = Label(frame1, text = " ", width = 100, bg = "#D396FF", font = ("verdana", 20, "bold"))
console_title.place(x = 0, y = 0)

console_title = Label(frame1,text = "SKROMAN ADMIN CONSOLE", fg = "Black", width = 80, bg = "#D396FF", font = ("verdana", 20))
console_title.place(x = 95, y = 0)

# Frame : 2
frame2 = Frame(frame1, height = 660, width = 1400, bg = "lightgreen")
frame2.place(x = 50, y = 70)

frame3 = Frame(frame2,height=590,width=650,bg="white")
frame3.place(x=40,y=30)

frame4 = Frame(frame2,height=590,width=650,bg="white")
frame4.place(x=710,y=30)

pub_title=Label(frame4 , text="PUBLISHED DATA",fg="Black",width=62,bg="lightgreen",font=("verdana",12))
pub_title.place(x=10,y=10)

pub_box = Text(frame4,bg="white",fg="black"  ,height=14,width=62,relief=GROOVE,border=2,font=("verdana",12))
pub_box.place(x=10,y=40)

sub_title=Label(frame4 , text="SUBSCRIBED DATA",fg="Black",width=62,bg="lightgreen",font=("verdana",12))
sub_title.place(x=10,y=308)

sub_box = Text(frame4,bg="white",fg="black" ,height=13,width=62,relief=GROOVE,border=2,font=("verdana",12))
sub_box.place(x=10,y=340)

mqtt_frame = Frame(frame3,height=260,width=610)
mqtt_frame.place(x=20,y=20)

client_title =Label(mqtt_frame,text="CLIENT",font=("verdana",15))
client_title.place(x=30,y=10) 

client = Combobox(mqtt_frame,width=30,values=["SKROMAN","FINOLEX"] ,font=("verdana",15))
client.place(x=150,y=10)
client.set("SKROMAN")

topic_title = Label(mqtt_frame,text="TOPIC",font=("verdana",15))
topic_title.place(x=30,y=60)

# Get Topic Info:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: 

get_topic = StringVar()
topic_box = Entry(mqtt_frame, textvariable = get_topic, width = 34, font = ("verdana", 14), relief = "groove", border = 2) 
topic_box.place(x = 150, y = 60,height = 32)
topic_box.insert(0, "SKSL_")

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Cert_button = Button(mqtt_frame,width=12, bg = "#ffd995",text="CERTIFICATE",font=("verdana",15),relief="groove",border=2,command=certifica_path)
Cert_button.place(x=30,y=120)

fetch_all_button = Button(mqtt_frame,width=12, bg = "#ffd995", text="FETCH ALL",font=("verdana",15),relief="groove",border=2)
fetch_all_button.place(x=210,y=120)

#Get Data
get_data_button = Button(mqtt_frame,width=12, bg = "#ffd995",text="GET DATA",font=("verdana",15),relief="groove",border=2)
get_data_button.place(x=400,y=120)

# AWS:
aws_button = Button(mqtt_frame,width=12, bg = "#ffd995", text="AWS",font=("verdana",15),relief="groove",border = 2, command = aws_button)
aws_button.place(x=30,y=190)

# Pub Clear:
pub_clear_button = Button(mqtt_frame,width=12, bg = "#ffd995", text="PUB CLEAR",font=("verdana",15),relief="groove",border=2,command=pub_clear)
pub_clear_button.place(x=210,y=190)

# Sub Clear:
sub_clear_button = Button(mqtt_frame,width=12, bg = "#ffd995", text="SUB CLEAR",font=("verdana",15),relief="groove",border=2,command=sub_Clear)
sub_clear_button.place(x=400,y=190)

ctrl_frame = Frame(frame3,height=260,width=610)
ctrl_frame.place(x=20,y=310)

module_title =Label(ctrl_frame, text = "MODULE",font = ("verdana", 15))
module_title.place(x = 30, y = 10)

module_box = Combobox(ctrl_frame, width = 30, values = ["10000", "44010", "46000", "66010", "68000", "88010", "87020", "8000", "23000", "20000", "13000"], font = ("verdana", 15))
module_box.place(x = 150, y = 10)
module_box.set("44010")

# Type:
type_title = Label(ctrl_frame, text = "TYPE",font = ("verdana", 15))
type_title.place(x = 30, y = 50)

type_box = Combobox(ctrl_frame, width = 7, values = ["L", "F", "M", "A"], font = ("verdana", 15))
type_box.place(x = 30, y = 85)
type_box.set("L")

# Number:
no_title = Label(ctrl_frame, text = "NO",font = ("verdana", 15))
no_title.place(x = 170, y = 50)

no_box = Combobox(ctrl_frame, width = 7, values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"], font = ("verdana", 15))
no_box.place(x = 170, y = 85)
no_box.set("1")

# State:
state_title =Label(ctrl_frame, text = "STATE",font = ("verdana", 15))
state_title.place(x = 310, y = 50)

state_box = Combobox(ctrl_frame, width = 7, values = ["1", "0"], font = ("verdana", 15))
state_box.place(x = 310, y = 85)
state_box.set("1")

# Speed:
speed_title =Label(ctrl_frame, text = "SPEED",font = ("verdana", 15))
speed_title.place(x = 450, y = 50)

speed_box = Combobox(ctrl_frame, width = 7, values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], font = ("verdana", 15))
speed_box.place(x = 450, y = 85)
speed_box.set("1")

# Red:
red_title = Label(ctrl_frame, text = "RED",font = ("verdana", 15))
red_title.place(x = 30, y = 130)

red_box = Entry(ctrl_frame, width = 7, font = ("verdana", 17),relief="groove",border=2)
red_box.place(x = 30, y = 165)

# Green:
green_title = Label(ctrl_frame, text = "GREEN",font = ("verdana", 15))
green_title.place(x = 170, y = 130)

green_box = Entry(ctrl_frame, width = 7, font = ("verdana", 17),relief="groove",border=2)
green_box.place(x = 170, y = 165)

# Blue:
blue_title = Label(ctrl_frame, text = "BLUE",font = ("verdana", 15))
blue_title.place(x = 310, y = 130)

blue_box = Entry(ctrl_frame, width = 7, font = ("verdana", 17),relief="groove",border=2)
blue_box.place(x = 310, y = 165)

# Brightness:
brightness_title = Label(ctrl_frame, text = "BRIGHT",font = ("verdana", 15))
brightness_title.place(x = 450, y = 130)

brightness_box = Entry(ctrl_frame, width = 7, font = ("verdana", 17),relief="groove",border=2)
brightness_box.place(x = 450, y = 165)

# OTA:
ota_button = Button(ctrl_frame,width=11, bg = "#ffd995", text="OTA",font=("verdana",15),relief="groove",border=2)
ota_button.place(x=30,y=220,height=30)


# Config:
config_button = Button(ctrl_frame,width=12, bg = "#ffd995", text="CONFIG",font=("verdana",15),relief="groove",border=2)
config_button.place(x=210,y=220,height=30)

# Hit:
hit_button = Button(ctrl_frame, width=12,bg = "#ffd995", text="HIT",font=("verdana",15),relief="groove",border=2, command = hit_button)
hit_button.place(x=400,y=220,height=30)

window.mainloop()