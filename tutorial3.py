#
# Project Name:
# USB Bridge - Tutorial 2
#
# Author: rvalentine
# Date: 10/19/2023
#
# Project Description:
# ----------------------
# Tutorial 3 performs basic read/write operations
# with interface 1 - HID.
#
# Disclaimer:
# ----------------------
# This code is provided as is and is not supported
# by RisingEdgeIndsutreis in any way. The user
# accepts all risk when running all or some of 
# this python module.
#

import ctypes as ct
import libusb as usb
import threading
import time

## -> GIT PUSH TEST

# 
# Defines
#
DEF_VID = 0x1cbf
DEF_PID = 0x0007
ENDPOINT1_OUT = 0x02
ENDPOINT1_IN = 0x82

EP1IN_SIZE = 64*1
EP1IN_TIMEOUT = 1000 	# mS

EP1OUT_SIZE = 64*1
EP1OUT_TIMEOUT = 250 	# mS

THD_TIMEOUT = 100


# 
# Libusb variables/data structures
#
dev = None
dev_found = False
dev_handle = ct.POINTER(usb.device_handle)() # creates device handle (not device obj)
devs = ct.POINTER(ct.POINTER(usb.device))() # creates device structure
ep_data_out = (ct.c_ubyte*(EP1OUT_SIZE))()
ep_data_in = (ct.c_ubyte*(EP1IN_SIZE))()
bulk_transferred = ct.POINTER(ct.c_int)()	

#
# inits
#
bulk_transferred.contents = ct.c_int(0)


"""
Name: 
thd_test2()

Parameters:
dev_handle - usb device handle

Return:
Nothing

Notes:
This function serves as the receiver thread for
test case #2.  The intent is to receive data
from the embedded emulator showing the value
in the lower bandwidth HID interface.

"""
def thd_test2(dev_handle):
	print("[Test case #2 - Thread Entry!]")
	i = 0

	# loop 5x rx packets
	while(i<5):
		# execute read transaction
		r = usb.bulk_transfer(dev_handle, ENDPOINT1_IN, ep_data_in, 
								EP1IN_SIZE, bulk_transferred, THD_TIMEOUT)

		if(r == 0):
			# HID packet found - print first byte indiciating packet
			# count from emulator
			print(f"{'byte[0]: ':.<30}{f'{ep_data_in[0]:#02x}':.>20}")
			i += 1

	print("Thread terminated!")



"""
Name: 
find_bridge()

Parameters:
VID - USB Vendor ID
PID - USB Product ID

Return:
Tuple consisting of error flag and either
error code or on success an object handle
to the USB device opened.

Notes:
This function searches through the host system
USB devices to find a device that matches the
VID/PID.  In this module, this would be the
USB bridge.

"""
def find_bridge(VID, PID):
	print('===================================')
	print('[Search and Connect to Bridge]!')
	print('Searching - Finding Bridge!')
	# open usb library
	r = usb.init(None)
	if r < 0:
		print(f'usb init failure: {r}')
		return (1, -1)

	# get list of USB devices
	cnt = usb.get_device_list(None, ct.byref(devs))
	# error check
	if cnt < 0:
		print(f'get device list failure: {cnt}')
		return (1, -1)

	# Check all USB devices for VID/PID match
	i = 0
	while devs[i]:
		dev = devs[i]

		# get device descriptor information
		desc = usb.device_descriptor()
		r = usb.get_device_descriptor(dev, ct.byref(desc))
		# error check
		if r < 0:
			print(f'failed to get device descriptor: {r}')
			return (1, -1)

		if(desc.idVendor == DEF_VID) and (desc.idProduct == DEF_PID):
			dev_found = True		
			break

		i += 1

	#
	# open device if matching vid/pid was found
	#
	if(dev_found == True):
		print('Searching - Bridge Found!')
		print('Connecting - Opening Bridge Connection!')
		r = usb.open(dev, dev_handle)
		# error check
		if r < 0:
			print(f"ret val: {r} - {usb.strerror(r)}")
			print("failed to open device!")
			return (1, -1)
		else:
			print('Connecting - Open Connection Success!')

		return (0, dev_handle)







"""
Name: 
testcase1_exe()

Parameters:
dev_handle - usb device handle

Return:
Tuple consisting of error flag and the
associated error code if any exists.

Notes:
This function executes a single HID packet
loop back test.  A 64 byte HID/Interrupt
packet is sent to the embedded emulator
which echos that packet back through the
bridge to the host sw application (this
module).

"""
def testcase1_exe(dev_handle):
	# -------------------------------------------------------------------
	print('\n\n\n===================================')
	print('[Test case#1 - hid write transaction]')

	# claim interface 0 - register access
	r = usb.claim_interface(dev_handle, 1)
	# error check
	if(r != 0):
		print(f'ERROR: failed to claim interface, ret val = {r}')
		print(f"ERROR: code - {usb.strerror(r)}")


	# --------------------------------------
	# Handle Transmit Case
	# --------------------------------------
	ep_data_out[0] = 10	 	# indicates loopback operation to
							# embedded emulator

	ep_data_out[1] = 1		# dummy data to check to verify rx'd
	ep_data_out[2] = 2 		# looped back data
	ep_data_out[3] = 3
	ep_data_out[4] = 4
	ep_data_out[5] = 5

	# execute write transaction
	r = usb.bulk_transfer(dev_handle, ENDPOINT1_OUT, ep_data_out, 
							EP1OUT_SIZE, bulk_transferred, EP1OUT_TIMEOUT)	
	print(f'Transferred {bulk_transferred.contents} bytes!')



	# --------------------------------------
	# Handle Receive Case
	# --------------------------------------

	# execute read transaction
	r = usb.bulk_transfer(dev_handle, ENDPOINT1_IN, ep_data_in, 
							EP1IN_SIZE, bulk_transferred, EP1IN_TIMEOUT)	
	# error check
	if (r < 0):
		print(f'ERROR: Total bytes transferred <{bulk_transferred.contents}> bytes!')
		print(f'ERROR: Expected to xfer <{EP1IN_SIZE}> bytes!')
		print(f'ERROR: bulk_transfer() ret code <{r}> bytes!')
		return (1, -1)
	else:	
		print(f'Received {bulk_transferred.contents} bytes!')



	# print read result
	print(f"{'byte[1]: ':.<30}{f'{ep_data_in[1]:#02x}':.>20}")
	print(f"{'byte[2]: ':.<30}{f'{ep_data_in[2]:#02x}':.>20}")
	print(f"{'byte[3]: ':.<30}{f'{ep_data_in[3]:#02x}':.>20}")
	print(f"{'byte[4]: ':.<30}{f'{ep_data_in[4]:#02x}':.>20}")
	print(f"{'byte[5]: ':.<30}{f'{ep_data_in[5]:#02x}':.>20}")

	return (0, 0)




"""
Name: 
testcase2_exe()

Parameters:
dev_handle - usb device handle

Return:
Tuple consisting of error flag and the
associated error code if any exists.

Notes:
This function executes a write transaction
over interface 1 (HID / Interrupt interface)
which tells the host emulator to respond with
5x packets at a rate of 1Hz. The first byte
in the transmit buffer (15d) indicates to the
embedded emulator it should respond this way.

A thread is started to receive all 5x packets
after the transmit "command" is sent to the
emulator.  This thread auto terminates after
the 5x packets are received.

"""
def testcase2_exe(dev_handle):
	# -------------------------------------------------------------------
	print('\n\n\n===================================')
	print('[Test case#2 - hid write transaction]')

	# --------------------------------------
	# Handle Transmit Case
	# --------------------------------------
	ep_data_out[0] = 15	 	# indicates 5x async HID packet response
							# to emulator

	ep_data_out[1] = 11		# dummy data to check to verify rx'd
	ep_data_out[2] = 12 	# looped back data
	ep_data_out[3] = 13
	ep_data_out[4] = 14
	ep_data_out[5] = 15

	# execute write transaction
	r = usb.bulk_transfer(dev_handle, ENDPOINT1_OUT, ep_data_out, 
							EP1OUT_SIZE, bulk_transferred, EP1OUT_TIMEOUT)	
	print(f'Transferred {bulk_transferred.contents} bytes!')		

	# start thread to receive 5 incoming packets from emulator
	x = threading.Thread(target=thd_test2, args=(dev_handle,))
	x.start()

	return (0, 0)


#
# Run module
#
r = find_bridge(DEF_VID, DEF_PID)

if(r[0] == 1):
	print(f"ERROR: ret val: {r}""}")
else:
	testcase1_exe(r[1])
	testcase2_exe(r[1])

	

