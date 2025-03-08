import threading
try:
    import Queue as queue
except:
    import queue
import traceback
import numpy as np

class StreamFileWriter(threading.Thread):
    #
    # Setup Init()
    #
    def __init__(self, FileHandle, ControlPanelObject):
        threading.Thread.__init__(self)

        # build take arrays
        self.ch1_take = [0, 4, 8, 12, 16, 20, 24]
        self.ch2_take = [1, 5, 9, 13, 17, 21, 25]
        self.ch3_take = [2, 6, 10, 14, 18, 22, 26]
        self.ch4_take = [3, 7, 11, 15, 19, 23, 27]

        self.en_flag_count = 0        # enable file logging (throw away first N samples)

        self.ControlPanel_Obj = ControlPanelObject
        self.FileHandle = FileHandle
        self.isAlive = threading.Event()
        self.isAlive.set()
        self.Queue = queue.Queue()

        self.ControlPanel_Obj.wRunLog('---> Stream file writer started!')



    def run(self):
        while self.isAlive.is_set():
            try:
                if (self.en_flag_count > 10):

                    # read data values out of queue
                    data = self.Queue.get(timeout=1)

                    # separate out channels
                    ch1_data = np.take(data, self.ch1_take)
                    ch2_data = np.take(data, self.ch2_take)
                    ch3_data = np.take(data, self.ch3_take)
                    ch4_data = np.take(data, self.ch4_take)

                    # write data
                    for i in range(7):
                        self.FileHandle.write(str(ch1_data[i]) + ', '
                                               + str(ch2_data[i]) + ', '
                                               + str(ch3_data[i]) + ', '
                                               + str(ch4_data[i]) + '\n')
                else:
                    self.en_flag_count += 1


            # to handle 1s timeout pop from queue
            except queue.Empty:
                pass

            except:
                traceback.print_exc()


        self.FileHandle.flush()
        self.FileHandle.close()






    def WriteData(self, data):
        self.Queue.put(data)