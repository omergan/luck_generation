
class Logger:
    def __init__(self):
        self.disabled = False
        self.debug_disabled = False
        self.tie_strength_disabled = False
        self.generate_luck_disabled = False
        self.critical_disabled = False

    def critical(self, msg):
        if not self.disabled and not self.critical_disabled:
            print("\033[91m {}\033[00m".format(msg))

    def debug(self, msg):
        if not self.disabled and not self.debug_disabled:
            print("\033[93m {}\033[00m".format(msg))

    def tie(self, msg):
        if not self.disabled and not self.tie_strength_disabled:
            print("\033[34m TIE:{}\033[00m".format(msg))

    def luck(self, msg):
        if not self.disabled and not self.generate_luck_disabled:
            print("\033[35m LUCK:{}\033[00m".format(msg))
