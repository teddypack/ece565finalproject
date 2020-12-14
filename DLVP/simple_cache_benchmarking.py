# -*- coding: utf-8 -*-

# Title: simple_cache_benchmarking
# Author: Conor Green
# Purpose: Final Project for ECE565
# Description: Runs benchmarks (as specified through the command line) on
#     the O3CPU with a "simple_cache." Heavily based on Jason Lowe Power's
#     simple_cache config script. His copyright is given below.
# Usage: Call as script through command line.
#         Command line parameter '-b' for spec2k6 benchmark to run


# Copyright (c) 2017 Jason Lowe-Power
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

""" This file creates a barebones system and executes 'hello', a simple Hello
World application. Adds a simple cache between the CPU and the membus.

This config file assumes that the x86 ISA was built.
"""

from __future__ import print_function
from __future__ import absolute_import

# import the m5 (gem5) library created when gem5 is built
import m5
# import all of the SimObjects
from m5.objects import *

import optparse

import spec2k6_simple_cache


m5.util.addToPath('../common')

bench_dir='/home/min/a/ece565/benchspec-2020/CPU2006/'
# X86
benchtype = '-m64-gcc43-nn'


parser = optparse.OptionParser()

parser.add_option("-b", "--benchmark", default="",
                 help="The benchmark to be loaded.")

# Run duration options
parser.add_option("-I", "--maxinsts", action="store", type="int",
    default=100000000, help="""Total number of instructions to simulate (default: run forever)""")

(options, args) = parser.parse_args()

print(options)

if args:
    print("Error: script doesn't take any positional arguments")
    sys.exit(1)

# create the system we are going to simulate
system = System()

# Set the clock fequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = 'timing'               # Use timing accesses
system.mem_ranges = [AddrRange('512MB')] # Create an address range

# Create a simple CPU
system.cpu = DerivO3CPU();

# Create a memory bus, a coherent crossbar, in this case
system.membus = SystemXBar()

# Create a simple cache
system.cache = SimpleCache(size='1kB')

# Connect the I and D cache ports of the CPU to the memobj.
# Since cpu_side is a vector port, each time one of these is connected, it will
# create a new instance of the CPUSidePort class
system.cpu.icache_port = system.cache.cpu_side
system.cpu.dcache_port = system.cache.cpu_side

# Hook the cache up to the memory bus
system.cache.mem_side = system.membus.slave

# create the interrupt controller for the CPU and connect to the membus
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

# Create a DDR3 memory controller and connect it to the membus
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Connect the system up to the membus
system.system_port = system.membus.slave

# Create a process for a simple "Hello World" application
process = spec2k6_simple_cache.get_process(options)

# Set the cpu to use the process as its workload and create thread contexts
system.cpu.workload = process
system.cpu.createThreads()

max_i = options.maxinsts
system.cpu.max_insts_any_thread = max_i

# set up the root SimObject and start the simulation
root = Root(full_system = False, system = system)
# instantiate all of the objects we've created above
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()#options)
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))