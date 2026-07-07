import os, sys 
from pythonosc import udp_client
from custom_libs.file_handler import get_replacement_list
import subprocess

if __name__ != "__main__":
    print("DONT RUN THIS AS A LIBARY OR I WILL MURDER YOU MYSELF. kindly --Jenny")
    exit()

file_path = os.path.dirname(os.path.realpath(__file__)) # get where we are
CLEAN_UP_SPEAK_PATH = os.path.join(file_path,"SPEECH_REPLACE.conf")
CLEAN_UP_GEN_PATH = os.path.join(file_path,"GEN_REPLACE.conf")
BLACK_LIST_PATH = os.path.join(file_path, "BLACKLIST.conf")
GEN_CONF_PATH = os.path.join(file_path, "GEN.CONF")
OSC_SCRIPT_PATH = os.path.join(file_path, "custom_libs", "OSC.py")

def call_OSC_handler(string: str):
    subprocess.run(["pkill","-f","OSC.py"], stderr=subprocess.DEVNULL)
    subprocess.Popen(["python3", OSC_SCRIPT_PATH, string])

def clear_screen(): 
    if os.name.lower() == "nt":
        os.system("cls")
    else:
        os.system("clear")
def term_fixup():
    # does not apply if piped in
    if sys.stdin.isatty():
        # from my understanding this tells the term
        # to handle text correctly
        sys.stdout.write("\033[?45h") 

clear_screen()
term_fixup()
def update_from_config(): 
    global CLEAN_UP_SPEAK
    global CLEAN_UP_GEN
    global BLACK_LIST
    global GEN_CONF
    CLEAN_UP_SPEAK = get_replacement_list(CLEAN_UP_SPEAK_PATH) 
    CLEAN_UP_GEN = get_replacement_list(CLEAN_UP_GEN_PATH)
    BLACK_LIST = get_replacement_list(BLACK_LIST_PATH)
    GEN_CONF = get_replacement_list(GEN_CONF_PATH)

update_from_config()

def clean_up_func(string : str) -> str:
    string = string.replace(".", " ")
    string_shown = string
    for word in CLEAN_UP_GEN:
        string = string.replace(f"{word.upper()}", f"{CLEAN_UP_GEN[word]}")
        string_shown = string_shown.replace(f"{word.upper()}", f"{CLEAN_UP_GEN[word]}")
    for word in CLEAN_UP_SPEAK:
        string = string.replace(f"{word.upper()}", f"{CLEAN_UP_SPEAK[word]}")
    for word in BLACK_LIST:
        string =  string.replace(f" {word.upper()} ", f"{BLACK_LIST[word]}") # remove the black listed words
    print(f"=====saying=====\n{string}\n====showing====\n{string_shown}\n===============")
    return string, string_shown


def speak(speak_string : str, input_string : str):
    call_OSC_handler(input_string)
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
def command_checker(input_string : str) -> bool:
    # not if/elif to allow someone to batch them 
    # eg: "reload_conf() clear()"
    ran_command = False
    if "exit()" in input_string:
        exit() # no point returning
    if "help()" in input_string:
        print("only commands are:\nexit()\nreload_conf()\n")
        ran_command = True
    if "reload_conf()" in input_string:
        update_from_config()
        ran_command = True
    if "clear()" in input_string:
        clear_screen()
        ran_command = True
    return ran_command

print("JSVRCTSS (Jennys Shitty VRC TTS) V 0.0.0.2 [PUBLIC]")
print("type \"help()\" for help")
print("?", end="", flush=True)
for line in sys.stdin:
    input_string = f"  {line}  "
    if command_checker(input_string):
        print("?", end="", flush=True)
        continue
    speak_string, input_string = clean_up_func(input_string)
    try:
        speak(speak_string,input_string)
    except Exception as E:
        print(f"SPEAK FAILED; LIKELY FAILED TO READ COMMAND FROM CONF\nis your config setup correctly?\npython error:\n{E}")
    print("?", end="", flush=True)
