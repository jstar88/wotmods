from libs.nbstreamreader import NonBlockingStreamReader as NBSR
import subprocess
import threading
from libs.Event  import Event as EVNT


class FrontEnd(object):
    onRead = EVNT()
    
    def __init__(self, service):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        self.process = subprocess.Popen(service,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        shell=False,
                        startupinfo=startupinfo
                        )
        
        self.stdin = self.process.stdin
        self.stdout = NBSR(self.process.stdout,self.process.stderr)
        
    def run(self,timeout = 4):
        
        def rund():
            while True:
                output = self.stdout.readline(timeout)
                # 0.1 secs to let the shell output the result
                if not output:
                    break
                self.on_read(output)

        t = threading.Thread(target=rund)
        t.start()
            
            
    def write(self, data):
        self.stdin.write(data + '\n')
        
    def on_read(self,data):
        self.onRead(data)
        
