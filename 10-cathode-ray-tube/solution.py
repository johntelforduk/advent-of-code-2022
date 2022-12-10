# Solution to day 10 of AOC 2022,
# https://adventofcode.com/2022/day/10

import structlog

structlog.configure(
    processors=[
        # Add callsite parameters.
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            }
        ),

        # Render the final event dict as JSON.
        structlog.dev.ConsoleRenderer()
    ]
)

log = structlog.get_logger()


class Device:

    def __init__(self, program: str):
        f = open(program)
        t = f.read()
        f.close()

        self.instructions = t.split('\n')
        self.ip = 0                 # Instruction pointer. Points to next instruction to be executed.
        self.x = 1                  # X register.
        self.cycles = 0             # Number of cycles started.
        self.cycles_left = 0        # How many more cycle to complete current instruction.
        self.curr_terms = []
        self.sum_sig_strengths = 0

        log.info('Ending __init__',
                 instructions=self.instructions,
                 ip=self.ip,
                 x=self.x,
                 cycles=self.cycles,
                 cycles_left=self.cycles_left)

    def noop(self):
        self.cycles_left = 1

    def start_addx(self):
        self.cycles_left = 2

    def end_addx(self, a: int):
        self.x += a

    def start_cycle(self):
        self.cycles += 1

        if self.cycles_left == 0:
            self.curr_terms = self.instructions[self.ip].split(' ')
            if self.curr_terms[0] == 'noop':
                self.noop()
            elif self.curr_terms[0] == 'addx':
                self.start_addx()
            else:
                raise 'No instruction found'

        # log.info('Ending start_cycle',
        #          ip=self.ip,
        #          x=self.x,
        #          cycles=self.cycles,
        #          cycles_left=self.cycles_left)

    def end_cycle(self):
        if self.cycles_left > 0:
            self.cycles_left -= 1
        if self.cycles_left == 0:
            self.ip += 1

        if self.cycles_left == 0:
            if self.curr_terms[0] == 'addx':
                self.end_addx(int(self.curr_terms[1]))

        # log.info('Ending end_cycle',
        #          ip=self.ip,
        #          x=self.x,
        #          cycles=self.cycles,
        #          cycles_left=self.cycles_left)

    def draw_pixel(self):
        pixel_pos = (self.cycles - 1) % 40
        if pixel_pos == self.x -1 or pixel_pos == self.x or pixel_pos == self.x + 1:
            pixel = '#'
        else:
            pixel = '.'
        print(pixel, end='')
        if pixel_pos == 39:
            print()
        # log.info('draw_pixel', cycles=self.cycles, pixel_pos=pixel_pos, x=self.x, pixel=pixel)


    def run_program(self):
        while self.ip < len(self.instructions):
            self.start_cycle()

            # For now, consider the signal strength (the cycle number multiplied by the value of the X register)
            # during the 20th cycle and every 40 cycles after that
            if (self.cycles - 20) % 40 == 0:
                # print(self.cycles, self.x)
                self.sum_sig_strengths += self.cycles * self.x

            self.draw_pixel()

            self.end_cycle()


my_device = Device(program='input.txt')
my_device.run_program()
print('Part 1:', my_device.sum_sig_strengths)
