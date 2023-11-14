class TMS1000Emulator:
    ROM_SIZE = 256
    RAM_SIZE = 64
    MAX_VALUE = 0xF

    def __init__(self):
        self.rom = [0] * self.ROM_SIZE
        self.ram = [0] * self.RAM_SIZE
        self.registers = {'PC': 0, 'A': 0}  # PC: Program Counter, A: Accumulator
        self.flags = {'C': False, 'Z': False}  # C: Carry/Borrow, Z: Zero
        self.running = False
        self.operations = {
            0x0: self.nop,
            0x1: self.add,
            0x2: self.sub,
            0x3: self.jmp,

        }

    def load_program(self, program):
        if len(program) > self.ROM_SIZE:
            raise ValueError(f"Program size must be <= {self.ROM_SIZE}.")
        self.rom = program[:] + [0] * (self.ROM_SIZE - len(program))  # Fill the rest with zeros

    def fetch(self):
        if self.registers['PC'] >= self.ROM_SIZE:
            self.stop()
            raise ValueError("Program Counter exceeded ROM size.")
        instruction = self.rom[self.registers['PC']]
        self.registers['PC'] = (self.registers['PC'] + 1) % self.ROM_SIZE
        return instruction
    
    def decode(self, instruction):
        operation_code = instruction >> 4
        operand = instruction & self.MAX_VALUE
        operation = self.operations.get(operation_code, self.nop)
        return operation, operand

    def execute(self, operation, operand):
        operation(operand)

    def run(self):
        self.running = True
        while self.running:
            if self.registers['PC'] >= self.ROM_SIZE - 1:  # Stop when the end of the ROM is reached
                self.stop()
            break

        instruction = self.fetch()
        operation, operand = self.decode(instruction)
        self.execute(operation, operand)

    def stop(self):
        self.running = False

    def jmp(self, operand):
        # Jump to the address specified by the operand
        self.registers['PC'] = operand

    def inspect_memory(self, address, length=1):
        # Return a slice of the ROM or RAM for inspection
        if address < self.ROM_SIZE:
            return self.rom[address:address + length]
        elif address < self.ROM_SIZE + self.RAM_SIZE:
            return self.ram[address - self.ROM_SIZE:address - self.ROM_SIZE + length]
        else:
            raise ValueError("Address out of range")

    def nop(self, operand=None):
        # No operation.
        pass
    
    def add(self, operand):
        result = self.registers['A'] + operand
        self.update_flags(result)
        self.registers['A'] = result & self.MAX_VALUE

    def sub(self, operand):
        result = self.registers['A'] - operand
        self.update_flags(result)
        self.registers['A'] = (result + (0x10 if result < 0 else 0)) & self.MAX_VALUE

    def update_flags(self, result):
        self.flags['C'] = result > self.MAX_VALUE or result < 0
        self.flags['Z'] = (result & self.MAX_VALUE) == 0


 # RUN / Example Usage
emulator = TMS1000Emulator()
example_program = [0x10, 0x21, 0x32, 0x43, 0x54]  # Replace with actual program nibbles
emulator.load_program(example_program)
## emulator.update_operations_dictionary()  # Make sure to update the dictionary before running
emulator.run()


print("Inspect ROM from 0x00 to 0x10:", emulator.inspect_memory(0x00, 0x10))
print("Inspect RAM from 0x00 to 0x04:", emulator.inspect_memory(0x100, 0x04))