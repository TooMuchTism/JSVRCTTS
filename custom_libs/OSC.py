import socket, sys, math, time, os
from file_handler import get_replacement_list

if __name__ != "__main__":
    print("DONT RUN THIS AS A LIBARY OR I WILL MURDER YOU MYSELF. kindly --Jenny")
    exit()
file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) # get where we are (well -1 subfolder)
GEN_CONF_PATH = os.path.join(file_path, "GEN.CONF")

CONF = get_replacement_list(GEN_CONF_PATH)



VRC_IP = "127.0.0.1" # if anyone wants this in a config file just ask me and ill move it there 
VRC_OSC_SOCK : socket.socket
VRC_PORT = 9000
def OSC_init() -> None:
    global VRC_OSC_SOCK 
    VRC_OSC_SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # set up UDP with KERNEL


def GET_4_aligned(len_bytes: int) -> int:
    return ((4 - len_bytes % 4) % 4)


# we dont need to do more then this lol, as long we the single use case works
def OSC_SEND(path: str, string : str, bools : list) -> None:
    try:
        final_message = bytearray(path.encode('utf-8')) # now we round this buffer up to 4 bytes
        final_message.append(0)
        final_message.extend(bytearray(GET_4_aligned(len(final_message)))) # makes it 4 byte rounded

        message = bytearray(string.strip().encode('utf-8'))
        message.append(0)
        message.extend(bytearray(GET_4_aligned(len(message))))
        
        type_string = ","
        if string != "":
            type_string+="s"
        for arg in bools:
            if arg == True: # this could be better lol
                type_string += "T"
            else:
                type_string += "F"
        type_string_bytes = bytearray(type_string.encode('utf-8'))
        type_string_bytes.append(0)
        type_string_padding_num = GET_4_aligned(len(type_string_bytes))
        type_string_bytes.extend(bytearray(type_string_padding_num))

        

        final_message.extend(type_string_bytes)
        final_message.extend(message)

        #print(final_message) nice to see on debug


        VRC_OSC_SOCK.sendto(final_message,(VRC_IP, VRC_PORT)) 
    except Exception as E:
        print(f"WARNING: OSC FAILED, did you send an empty message?\npython error:\n{E}")

OSC_init()

SIZE_AREA = int(CONF["chatbox_chunking_size"]) 
number_areas_input = int(math.ceil(len(sys.argv[1])/SIZE_AREA))
WAIT_TIME = float(CONF["chatbox_chunking_wait_time"]) 
OSC_SEND("/chatbox/typing", "", [True])
# TODO: put better error handling here
for i in range(number_areas_input):
    start_point = i*SIZE_AREA
    end_point = i*SIZE_AREA+SIZE_AREA
    if end_point >= len(sys.argv[1]):
        end_point = len(sys.argv[1])-1

    if start_point >= len(sys.argv[1]):
        break
    text_showing = list(sys.argv[1])[start_point:end_point]
    

    text_showing = f"{''.join(text_showing)}..."
    #print(f"showing: {text_showing}")
    OSC_SEND("/chatbox/input", text_showing, [True, False])
    time.sleep(WAIT_TIME)
OSC_SEND("/chatbox/typing", "", [False])

#print("EOF")
