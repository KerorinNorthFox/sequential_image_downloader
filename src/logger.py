class Logger(object):
    def info(self, msg):
        print(f"[INFO] :{msg}")
        
    def warn(self, msg):
        print(f"[WARN] :{msg}")
        
    def error(self, msg):
        print(f"[ERROR] :{msg}")
        
logger = Logger()