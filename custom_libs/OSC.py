import socket

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
        
        type_string = ",s"
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
