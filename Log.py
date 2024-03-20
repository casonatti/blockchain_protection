import linecache
import threading

class Log:
  def __init__(self):
    self.buffer = []
    self.mutex = threading.Lock()
    self.flag_new_log = False

    self.counter = 1
    self.line_control = 1

  def append(self, text_log):
    self.buffer.append(text_log)

  def write_log_file(self):    
    while True:
      if len(self.buffer) == 0:
        continue

      self.mutex.acquire()

      try:
        print("Writing to log file.")
        print("Buffer Len: " + str(len(self.buffer)))

        with open("log.txt", "a") as log_file:
          while len(self.buffer) > 0:
            log_file.write(">>>> " + str(self.buffer[0]) + "\n")
            self.buffer.pop(0)
            self.counter += 1

        log_file.close()

      except Exception as e:
        print("Deu pau! Exception: " + str(e))
        exit(1)
      finally:
        self.flag_new_log = True
        self.mutex.release()

  def read_log_file(self, textview_buffer):
    while True:
      if not self.flag_new_log:
        continue

      self.mutex.acquire()

      try:
        while self.counter > 1:
          textview_buffer.append(linecache.getline("log.txt", self.line_control))
          linecache.clearcache()
          self.line_control += 1
          self.counter -= 1

      except Exception as e:
        print("Deu pau! Exception: " + str(e))
        exit(1)
      finally:
        self.flag_new_log = False
        self.mutex.release()

# Colocar no programa principal
log = Log()

threads = []

log_buffer = "Teste"

writing_thread = threading.Thread(target=log.write_log_file, name="Writing_Thread")
threads.append(writing_thread)

reading_thread = threading.Thread(target=log.read_log_file, args=(log_buffer,), name="Reading_Thread")
threads.append(reading_thread)

for thread in threads:
  thread.start()

for thread in threads:
  thread.join()