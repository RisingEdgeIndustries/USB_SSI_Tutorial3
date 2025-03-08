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
# To Do:
# Launch thread to receive async INT packets and 
# use main application for time.sleep delays and
# to receive multiple blocks of BULK data.
#
# Set SCLK to 8Mhz and make sure fw in emulator
# uses flow control.
#
# Might want to write data to file and verify it
# as well. Nice thing to show. Justuse CSV files.
#
#

import ctypes as ct
import libusb as usb
import threading
import time
from USB_SSI_Libs.rei_usb_lib import USB20F_Device

## -> GIT PUSH TEST 2




# for logger
log_file_name = "tutorial3_log_file"




"""
Name: 
testcase1_exe()

Parameters:
dev_handle - usb device handle

Return:
Tuple consisting of error flag and the
associated error code if any exists.

Notes:
Start thread, command async INT packet generation EN, mix in 
1k or so BULK xfers as well and then close everything out. Store
in CSV file and check value, probably counter inc values as an
example.

"""
def testcase1_exe(dev_handle):
	# -------------------------------------------------------------------
	print('\n\n\n===================================')
	print('[tutorial #3 - threaded receiver]')



	return (0, 0)






#
# Run module
#
# open USB lib
usb_dev0 = USB20F_Device(quiet=False, name=log_file_name)
usb_dev0.open_usb()



# test - error with logger or something failing
# original error due to not calling close() method
usb_dev0.dump_regspace()




# need this to exit gracefully
usb_dev0.close_usb()
