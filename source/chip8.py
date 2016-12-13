import random

class Chip8:
    MAX_INT = 255
    
    def __init__(self):
        self.V = [0]*16
        self.mem = [0] * 4096
        self.PC = 0
        self.SP = 0
        self.stack = [0] * 16
        
class Emulator:
    def __init__(self, chip, display):
        self.chip = chip
        self.display = display

    def _00E0(self): # CLS
        self.display.clear()

    def _00EE(self): # RET
        self.chip.PC = self.chip.stack[self.chip.SP]
        self.chip.SP -= 1
        
    def _1nnn(self, loc): # JP adrr
        self.chip.PC = loc 

    def _2nnn(self, loc): # CALL adrr
        self.chip.SP +=1
        self.chip.stack[self.chip.sp] = self.chip.PC
        self.chip.PC = loc

    def _3xkk(self, x, byte): # SE Vx, byte
        if self.chip.V[x] == byte:
            self.chip.PC += 1

    def _4xkk(self, x, kk): # SNE Vx, byte
        if self.chip.V[x] != kk:
            self.chip.PC += 1

    def _5xy0(self, x, y): # SE Vx, Vy
        if self.chip.V[x] == self.chip.V[y]:
              self.chip.PC += 1
              
    def _6xkk(self, x, byte): # LD Vx, byte
        self.chip.V[x] = byte

    def _7xkk(self, x, byte): # ADD Vx, byte
        self.chip.V[x] += byte
        self.chip.V{x] %= self.chip.MAX_INT

    def _8xy0(self, x, y): # LD Vx, Vy
        self.chip.V[x] = self.chip.V[y]

    def _8xy1(self, x, y): # OR Vx, Vy
        self.chip.V[x] |= self.chip.V[y]

    def _8xy2(self, x, y): # AND Vx, Vy
        self.chip.V[x] &= self.chip.V[y]

    def _8xy3(self, x, y):  # XOR Vx, Vy
        self.chip.V[x] ^= self.chip.V[y]

    def _8xy4(self, x, y): # SUB Vx, Vy (carry -> VF)
        self.chip.V[x] += self.chip.V[y]

        if self.chip.V[x] > self.chip.MAX_INT:
            self.chip.V[0xF] = 1
            self.chip.V[x] %= self.chip.MAX_INT
            
        else:
            self.chip.V[0xF] = 0

    def _8xy5(self, x, y): # SUB Vx, Vy (not borrow -> VF)
        self.chip.V[0xF] = int(self.chip.V[x] > self.chip.V[y])

        """ Currently subtraction behaviour is implemented with wrapping. """
        self.chip.V[x] -= self.chip.V[y]
        self.chip.V[x] %= self.chip.MAX_INT

    def _8xy6(self, x, y = None): # SHR Vx {, Vy}
        # Get least significant bit of Vx
        LSB = self.chip.V[x] % 2
        
        self.chip.V[x] //= 2
        self.chip.V[0xF] = LSB

    def _8xy7(self, x, y): #SUBN Vx, Vy (not borrow -> VF)
        self.chip.V[0xF] = int(self.chip.V[y] > self.chip.V[x])

        """ Currently subtraction behaviour is implemented with wrapping. """
        self.chip.V[x] = (self.chip.V[x] - self.chip.V[y]) % self.chip.MAX_INT

    def _8xyE(self, x, y = None): # SHL Vx {, Vy}
        # Get least significant bit of Vx
        LSB = self.chip.V[x] % 2
        
        self.chip.V[x] *= 2
        self.chip.V[x] %= self.chip.MAX_INT
        self.chip.V[0xf] = LSB

    def _9xy0(self, x, y): # SNE Vx, Vy
        if Vx != Vy:
            self.chip.PC += 2
