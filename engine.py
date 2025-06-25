import engine_util
import subprocess
from threading import RLock

class Engine:
    def __init__(self):
        self.lock = RLock()
        self.search_data = []
        
        self.process = subprocess.Popen(
            #["./engine/peacekeeper"], #on linux
            ["engine/peacekeeper.exe"], #on windows
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
           text=True,
            bufsize=1  # line buffered
        )
        
        self.process.stdin.write("uci\n")
        self.process.stdin.flush()

        response = ""
        while response != "uciok\n":
            response = self.process.stdout.readline()
            
        self.process.stdin.write("setoption name Hash value 32\n")
        self.process.stdin.flush()   
    
    def __del__(self):
        self.process.terminate()
    
    def search(self, move_time, debug=False):
        self.process.stdin.write(f"go movetime {move_time}\n")
        self.process.stdin.flush()
        
        with self.lock:
            self.search_data = []

        response = ""
        while not response.startswith("bestmove"):
            response = self.process.stdout.readline()
            
            if not response.startswith("bestmove"):
                if debug:
                    print("response:", response.strip())
                with self.lock:
                    self.search_data.append(response.strip())
            else:
                if debug:
                    print("response:", response.strip())
                
                return response.strip().split()[1]
        
        return "a8a8"
