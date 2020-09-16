import os
from functools import reduce
from pathlib import Path

DSR_FILE = "/tmp/DSR"
RTR_FILE = "/tmp/RTR"
DATA_FILE = "/tmp/DATA"

EVEN_SIZE = 1000
ODD_SIZE = 1001

shifts = (7, 6, 5, 4, 3, 2, 1, 0)
def message_to_bits(message):
    ords = (ord(c) for c in message)
    bits_groups = [
        [(o >> shift) & 1 for shift in shifts] 
        for o in ords
    ]
    return [bit for bit_group in bits_groups for bit in bit_group]


def write_bit_to_data_file(bit):
    should_be_even = bit == 0
    size = EVEN_SIZE if should_be_even else ODD_SIZE
    with open(DATA_FILE, "wb") as out:
        out.seek(size - 1)
        out.write(b'\0')

def touch_dsr():
    Path(DSR_FILE).touch()


def wait_for_acknowledgement():
    # Wait for acknowledgement
        ready = False
        while not ready:
            ready = os.path.exists(RTR_FILE)

        # Now they hav acknowledged, we are going to delete their ack 
        os.remove(RTR_FILE)

def main():
    # Take the input for what to send
    bits = message_to_bits(input("What would you like to send?"))

    for bit in bits:
        write_bit_to_data_file(bit)
        touch_dsr()
        wait_for_acknowledgement()

    # When done, delete data file. Wait for it to be handled there.
    os.remove(DATA_FILE)
    touch_dsr()
    wait_for_acknowledgement()
    print("Done sending bits. Deleted data file to signal complete.")

if __name__ == "__main__":
    main()