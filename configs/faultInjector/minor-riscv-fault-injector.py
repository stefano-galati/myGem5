# Copyright (c) 2015 Jason Power
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This is the RISCV equivalent to `simple.py` (which is designed to run using the
X86 ISA). More detailed documentation can be found in `simple.py`.
"""

import argparse
import sys

import m5
from m5 import fatal
from m5.objects import *
from m5.stats import (
    dump,
    reset,
)

BASEPATH = "/home/stefano/Desktop/simulations"
tick_limit = 999999999999999999

parser = argparse.ArgumentParser()  # create object?
parser.add_argument(
    "binary", default="hello", nargs="?", type=str, help="Path to binary file"
)
parser.add_argument("--memory", help="Type of memory")
parser.add_argument("--tick_limit", help="Max number of ticks before stopping")

options = parser.parse_args()
# print("Helloooo")
# print(options)
if options.tick_limit != None:
    tick_limit = int(options.tick_limit)

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]
system.cpu = RiscvMinorCPU()

system.membus = SystemXBar()

system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

system.cpu.createInterruptController()

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

# thispath = os.path.dirname(os.path.realpath(__file__))
binary = os.path.join(BASEPATH, options.binary)

print("Binary: ", binary)

system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

m5.setMaxTick(tick_limit)  # after this number of ticks, stop the simulation

root = Root(full_system=False, system=system)
root.injector = RegisterFaultInjector(inputFile="testString", number=1)
# instantiate the RegisterFaultInjector object
m5.instantiate()

print(f"Beginning simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")

m5.stats.dump()

if exit_event.getCause() == "simulate() limit reached":
    print("Hey, simulate() limit reached!")
    exit(
        2
    )  # exit code 2 if number of ticks greater than maximum (detecting infinite loops)
