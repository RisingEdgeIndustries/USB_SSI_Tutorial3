# ################################################################
# Project Name:
# USB Bridge - Tutorial 3
#
# Author: rvalentine
# Date: 10/19/2023
#
#
# Project Description:
# ----------------------------------------------------------------
# Tutorial 3 shows data transfer over both BULK and INT interfaces.
# INT frames are mixed into the BULK datastream which show users
# can interleave data from different interfaces. In this example,
# one could use the INT interface (from the embedded system SSI
# side) to tell the software application how much BULK data to 
# read from the embedded system in a single burst. From this
# example, many other styles of implementations could be used.
#  
#
# Notes:
# ----------------------------------------------------------------
# For increased performance and functionality from the software
# side, develop applications using core lib (libusb) ASYNC
# capability.
# https://libusb.sourceforge.io/api-1.0/libusb_mtasync.html
#
#
# ----------------------------------------------------------------
# Disclaimer:
# ----------------------------------------------------------------
# This library is provided strictly as example code. There is no
# expected reliablity of operation from RisingEdgeIndustries and 
# this source code is not to be sold or represented as a 3'd party
# solution for commercial use. The below code is development code
# for example use only supporting customers as they test the bridge
# products from RisingEdgeIndustries. Nothing in this file is allowed
# to be modified or sold in any way. No code below is released with 
# the intention or expectation of reliable operation.
#
# Packing this module with any 3d part code can only be done with 
# the inclusion of this disclaimer and no modifications.
# ################################################################


try:
	import Queue as queue
except:
	import queue
import ctypes as ct
import libusb as usb
import threading
import time
from USB_SSI_Libs.rei_usb_lib import USB20F_Device



#
# GLOBALs
#
log_file_name = "tutorial3_log_file"



# ----------------------------------------------------------------
# Telemetry reciever thread
#
# Description:
# Perform all USB bridge data reads in thread. This emulates
# real world implementations where the main application loop
# doesn't directly manage USB object accesses.
# ----------------------------------------------------------------
class tly_receiver(threading.Thread):
	#
	# Setup Init()
	#
	def __init__(self, usb_dev_handle):
		threading.Thread.__init__(self)
		self.isAlive = threading.Event()
		self.isAlive.set()
		self.Queue = queue.Queue()
		self.usb_dev_handle = usb_dev_handle


	# over-ride run method
	# poll each interface until threading event set to false
	def run(self):
		bulk_counter = 0

		# send test case command 21d
		data = [0]*64
		data[0] = 21
		self.usb_dev_handle.write_int1(data)

		while(self.isAlive.isSet()):
			ret = self.usb_dev_handle.read_int1(timeout=1)
			if(ret[0] == 0):
				print(f"INT Packet Received: {len(ret[1])}")
			else:
				if(ret[1] == -7):
					pass
				else:
					print(f"INT error: {ret}")

			ret = self.usb_dev_handle.rec_bulk(ep_size=64*128, timeout=1)
			if(ret[0] == 0):
				print(f"BULK: Received 128 packets!")
			else:
				if(ret[1] == -7):
					pass
				else:
					print(f"BULK error: {ret}")

		print(f"Exiting (isAlive value): {self.isAlive.isSet()}")


# ----------------------------------------------------------------
# Main class
#
# Description:
# Main tutorial class encapsulating tutorial functionality
#
# ----------------------------------------------------------------
class main:
	def __init__(self):
		pass

	# testcase_exe - main test case method 
	def testcase_exe(dev_handle):
		# -------------------------------------------------------------------
		print('\n\n\n===================================')
		print('[tutorial #3 - threaded receiver]')
		j = 0


		# open USB device and create object
		usb_dev0 = USB20F_Device(quiet=True, name=log_file_name)
		usb_dev0.open_usb()

		# start receiver thread
		thd = tly_receiver(usb_dev0)
		thd.daemon = True
		thd.start()
	

		time.sleep(3)
		thd.isAlive.clear()

		# Ensure thread closed
		thd.join()
	
	
		# Close USB link gracefully
		usb_dev0.close_usb()
	

		return (0, 0)



#
# Main Application
# Run
app = main()
app.testcase_exe()
