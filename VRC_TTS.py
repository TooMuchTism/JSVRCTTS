import os, sys # we dont need to worry about the user command injecting themselves lol <-- will still fix that 
from pythonosc import udp_client
from custom_libs.file_handler import get_replacement_list
import custom_libs.OSC as OSC
import subprocess

if __name__ != "__main__":
    print("DONT RUN THIS AS A LIBARY OR I WILL MURDER YOU MYSELF. kindly --Jenny")
    exit()
OSC.OSC_init()

    

file_path = os.path.dirname(os.path.realpath(__file__)) # get where we are
CLEAN_UP_SPEAK_PATH = os.path.join(file_path,"SPEECH_REPLACE.conf")
CLEAN_UP_GEN_PATH = os.path.join(file_path,"GEN_REPLACE.conf")
BLACK_LIST_PATH = os.path.join(file_path, "BLACKLIST.conf")
GEN_CONF_PATH = os.path.join(file_path, "GEN.CONF")

CLEAN_UP_SPEAK = get_replacement_list(CLEAN_UP_SPEAK_PATH) 
CLEAN_UP_GEN = get_replacement_list(CLEAN_UP_GEN_PATH)
BLACK_LIST = get_replacement_list(BLACK_LIST_PATH)
GEN_CONF = get_replacement_list(GEN_CONF_PATH)



def clean_up_func(string : str) -> str:
    string = string.replace(".", " ")
    string_shown = string
    for word in BLACK_LIST:
        string =  string.replace(f" {word} ", f"{BLACK_LIST[word]}") # remove the black listed words
    for word in CLEAN_UP_SPEAK:
        string = string.replace(f" {word} ", f" {CLEAN_UP_SPEAK[word]} ")
    for word in CLEAN_UP_GEN:
        string = string.replace(f" {word}", f" {CLEAN_UP_GEN[word]}")
        string_shown = string_shown.replace(f"{word}", f" {CLEAN_UP_GEN[word]} ")
    print(f"=====saying=====\n{string}\n====showing====\n{string_shown}\n===============")
    return string, string_shown


def speak(speak_string : str, input_string : str):
    OSC.OSC_SEND("/chatbox/input", input_string, [True])
    command_string_conf = GEN_CONF["cmd"]
    commands_string_run = []
    current_index = 0
    commands_string_run.append(list())
    for part in command_string_conf.split(" "):
        if part == "'{speak_string}'": 
            part = speak_string
        if part == "&&": # check for >1 command
            current_index += 1
            commands_string_run.append(list())
            continue
        commands_string_run[current_index].append(f"{part}")
    for command in commands_string_run:
        #print(command) # if your debugging this is nice to see
        subprocess.run(command)
    

if os.name.lower() == "nt":
    os.system("cls")
else:
    os.system("clear")
print("JSVRCTSS (Jennys Shitty VRC TTS) V 0.0.0.1 [PUBLIC]")
print("type \"help()\" for help")
print("?", end="", flush=True)
for line in sys.stdin:
    input_string = f" {line} "
    if "exit()" in input_string:
        exit()
    if "help()" in input_string:
        print("only command is \"exit()\"")
    speak_string, input_string = clean_up_func(input_string)
    try:
        speak(speak_string,input_string)
    except Exception as E:
        print(f"SPEAK FAILED; LIKELY FAILED TO READ COMMAND FROM CONF\nis your config setup correctly?\npython error:\n{E}")
    print("?", end="", flush=True)
