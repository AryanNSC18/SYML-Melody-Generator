import os.path
import tkinter
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from Melody_Generator import LoFiGen,seq_len
from File_Merger import wav_gen
from mido import MidiFile
from pydub import AudioSegment
import pygame


lg = LoFiGen()

root = ctk.CTk()
ctk.set_appearance_mode("Dark")
root.geometry("1000x800")
root.title("SYML MEl GEN")

def compile_func():
    try:
        code= seed_code_ent.get()
        string_code = str(code)
        lofi_tune = lg.gen_lofi(string_code,140,seq_len,0.3)
        lg.save_lofi(lofi_tune)
        gen_sum.insert(tk.INSERT,"Melody Generated Sucessfully\n")
        print("The code is",code)
        print("The string code is",string_code)
    except:
        gen_sum.insert(tk.INSERT,"Compilation ERROR\n")



def browse():
    file_dir =filedialog.askopenfile(initialdir="/:",title="Choose the midi File")
    print("the file dir is",file_dir)
    return file_dir

def play_midi(my_midi):
    clock = pygame.time.Clock
    try:
        pygame.mixer.music.load(my_midi)
    except:
        print("Error While opening file")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(30)

def click_play_midi():
    gen_sum.insert(tk.INSERT, "\nPlaying a MIDI File!!\n")
    x = browse()
    my_midi = x
    freq =44100
    bitsize = -16
    channels = 2
    buffer = 1024
    pygame.mixer.init(freq,bitsize,channels,buffer)
    try:
        play_midi(my_midi)
    except KeyboardInterrupt:
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit

def stop_int():
    gen_sum.insert(tk.INSERT, "\nMIDI Melody stopped")
    pygame.mixer.music.fadeout(100)
    pygame.mixer.music.stop()

def clear_window():
    gen_sum.delete("1.0",tk.END)


def temp_tex(events):
    seed_code_ent.delete(0,"end")

def browse_mid_wav():
    file_dir = filedialog.askopenfile(mode='r',initialdir="/", title="Choose the midi File")
    if file_dir:
        file_path = os.path.abspath(file_dir.name)

    return file_path


def convert_wav():
    x = browse_mid_wav()
    mid = MidiFile(x)
    output = AudioSegment.silent(mid.length * 1000.0)
    wav_gen(output,mid)
    print("Wav_conversion completed")

def browse_lofi_tune():
    file_dir = filedialog.askopenfile(mode='r', initialdir="C:", title="Choose the lofi_side File")
    if file_dir:
        file_path = os.path.abspath(file_dir.name)

    return file_path


def lofi_gen():
    lof =browse_lofi_tune()
    sound_1= AudioSegment.from_file("Generated_mels/SYML_WAV.wav") # same path as generated wav
    sound_2 = AudioSegment.from_file(lof)
    combied = sound_2.overlay(sound_1)
    combied.export("Generated_mels/SYML_gen_lofi.wav",format='wav') # exporting path for final lofi
    print("Augmen Done")
def browse_fish():
    file_dir = filedialog.askopenfile(mode='r', initialdir="C:", title="Choose the lofi_side File")
    if file_dir:
        file_path = os.path.abspath(file_dir.name)

    return file_path

def play_wav():
    my_dir = browse_fish()
    pygame.init()
    pygame.mixer.init()
    sounda = pygame.mixer.Sound(my_dir)
    sounda.play()
def stop_wav():
    pass


def open_lofi_window():
    lofi_workshop = ctk.CTkToplevel()
    lofi_workshop.geometry("900x600")
    lofi_workshop.title("LOFI-WORKSHOP")
    if lofi_workshop is None or not lofi_workshop.winfo_exists():
        lofi_workshop = ctk.CTkToplevel()
        lofi_workshop.geometry("900x600")
        lofi_workshop.title("LOFI-WORKSHOP")
    else:
        #lofi_workshop.focus()
        label = ctk.CTkLabel(master=lofi_workshop,text="Welcome to LoFi Gen House",width=120,height=60,fg_color=("black","gray75"),corner_radius=8)
        label.place(relx=0.52,rely=0.1,anchor=tkinter.CENTER)

        button_wav =  ctk.CTkButton(master=lofi_workshop,text="SYML_SPS",corner_radius=8,command=convert_wav)
        button_wav.place(relx=0.52, rely=0.47, anchor=tk.CENTER)
        button_wav_gen = ctk.CTkButton(master=lofi_workshop,text="LOFI",corner_radius=8,command=lofi_gen)
        button_wav_gen.place(relx=0.52, rely=0.57, anchor=tk.CENTER)
        button_wav_play = ctk.CTkButton(master=lofi_workshop, text="Play WAV", corner_radius=8, command=play_wav)
        button_wav_play.place(relx=0.52, rely=0.67, anchor=tk.CENTER)
        button_wav_stop = ctk.CTkButton(master=lofi_workshop, text="Stop WAV", corner_radius=8, command=stop_wav)
        button_wav_stop.place(relx=0.52, rely=0.77, anchor=tk.CENTER)



welnote  = ctk.CTkLabel(master=root,text="WELCOME TO SYML MEL GENERATOR",width=120,height=60,fg_color=("black","gray75"),corner_radius=8)
welnote.place(x=360,y=23)

code_note  = ctk.CTkLabel(master=root,text="SYML Language Compiler",width=120,height=60,fg_color=("black","gray75"),corner_radius=10)
code_note.place(x=390,y=400)



gen_sum = ctk.CTkTextbox(master=root,width=350,height=80,corner_radius=8)
gen_sum.grid(row=0,column=0,sticky="nsew")
gen_sum.place(x=320,y=100)

# seed_code_ent = tk.Entry(root,font=("Helvetica",16,"bold"),width=60,bg="white",fg="blue")
# seed_code_ent.insert(0,"Enter your code here")
# seed_code_ent.bind("<FocusIn>",temp_tex)
# seed_code_ent.place(x=100,y=600)

seed_code_ent = ctk.CTkEntry(master=root,placeholder_text="Enter Your code here",width=600,height=40,border_width=4,corner_radius=8)
seed_code_ent.place(x=160,y=600)


button = ctk.CTkButton(master=root,text="Compile",corner_radius=14,height=40,command=compile_func)
button.place(relx=0.9,rely=0.79,anchor=tk.CENTER)

button_2 = ctk.CTkButton(master=root,text="Browse",corner_radius=8,command=browse)
button_2.place(relx=0.9,rely=0.4,anchor=tk.CENTER)

button_3 = ctk.CTkButton(master=root,text="play",corner_radius=8,command=click_play_midi)
button_3.place(relx=0.9,rely=0.2,anchor=tk.CENTER)

button_4 = ctk.CTkButton(master=root,text="stop",corner_radius=8,command=stop_int)
button_4.place(relx=0.9,rely=0.3,anchor=tk.CENTER)

button_5 = ctk.CTkButton(master=root,width=40,height=20,text="clear",corner_radius=6,command=clear_window)
button_5.place(relx=0.49,rely=0.27,anchor=tk.CENTER)


button_6 = ctk.CTkButton(master=root,width=70,height=40,text="LoFi-Workspace",corner_radius=6,command=open_lofi_window)
button_6.place(relx=0.9,rely=0.65,anchor=tk.CENTER)

root.mainloop()
