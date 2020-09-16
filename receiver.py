import time
import os
from pathlib import Path

DSR_FILE = "/tmp/DSR"
RTR_FILE = "/tmp/RTR"
DATA_FILE = "/tmp/DATA"

shifts = (7, 6, 5, 4, 3, 2, 1, 0)
def print_bits_as_ascii(data):
    chunks = [data[x:x+8] for x in range(0, len(data), 8)]
    chars = [chr(sum(bit << s for bit, s in zip(chunk, shifts))) for chunk in chunks]
    print("Message: ", "".join(chars)) 

def acknowledge():
    # Delete the DSR_FILE. & touch the RTR_FILE 
    os.remove(DSR_FILE)
    Path(RTR_FILE).touch()
    print("Received bit and reset flags")

def get_next_bit():
    #Read the in the bit from DATA_FILE.
    is_even_bytes = os.path.getsize(DATA_FILE) % 2 == 0
    bit = 0 if is_even_bytes else 1
    return bit

def next_bit_is_ready():
    """ By definition, the next bit is not ready until the DSR file exists."""
    return os.path.exists(DSR_FILE) 

def can_receive_next_bit():
    """ We cannot receive the next bit unless the data file exists. """
    return os.path.exists(DATA_FILE)

def has_communication_began():
    """ We cannot receive a communication unless both the data file and dsr file are written,. """
    return can_receive_next_bit() and next_bit_is_ready()

def main():
    # Wait for the sender to send and write the first bit.
    while not has_communication_began():
        print("Communication from sender has not begun")
        time.sleep(1)
    
    # Now that the communication has begun, we need to continually read the bits to
    # from the tmp channel.
    bits = []
    while True:
        while not next_bit_is_ready():
            pass
        if can_receive_next_bit():
            bits.append(get_next_bit())
            acknowledge()
        else:
            acknowledge()
            break
    
    # Now that the loop has terminated, we should be able to convert the bits into ascii
    # and print the response.
    print_bits_as_ascii(bits)

if __name__ == "__main__":
    main()