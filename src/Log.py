import linecache
import threading
import time

class Log:
  def __init__(self):
    self.buffer = []
    self.mutex = threading.Lock()
    self.flag_new_log = False
    self.counter = 1
    self.line_control = 1

  def config_initialization(self, textview):
    with open('log.txt', 'r') as file:
      lines = file.readlines()
    
    file.close()

    self.line_control = len(lines) + 1
    
    for i, line in enumerate(lines):
      textview.append(linecache.getline("log.txt", i+1))
      linecache.clearcache()

  def append(self, text_log):
    self.buffer.append(text_log)

  def write_log_file(self): 
    print("Writing Thread Initilized")

    while True:
      if len(self.buffer) == 0:
        time.sleep(0.1)
        continue

      self.mutex.acquire()

      try:
        # print("Writing to log file.")

        with open("log.txt", "a") as log_file:
          while len(self.buffer) > 0:
            log_file.write(">>>> " + str(self.buffer[0]) + '\n')
            self.buffer.pop(0)
            self.counter += 1

        log_file.close()

      except Exception as e:
        print("Exception: " + str(e))
        exit(1)

      except KeyboardInterrupt:
        break

      finally:
        self.flag_new_log = True
        self.mutex.release()

  def read_log_file(self, textview_buffer):
    print("Reading Thread Initilized")

    while True:
      if not self.flag_new_log:
        time.sleep(0.1)
        continue

      self.mutex.acquire()

      try:
        # print("Reading log file")
        
        while self.counter > 1:
          textview_buffer.append(linecache.getline("log.txt", self.line_control))
          linecache.clearcache()
          self.line_control += 1
          self.counter -= 1

      except Exception as e:
        print("Exception: " + str(e))
        exit(1)

      except KeyboardInterrupt:
        break

      finally:
        self.flag_new_log = False
        self.mutex.release()