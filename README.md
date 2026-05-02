# gem5 with Fault Injection capability

This repository is a fork of the gem5 repository from February 2025 (gem5 v24.1.0.2), extended with support for fault injection during simulation.

## Main changes

### RegisterFaultInjector
The `faultInjection` branch contains the commits that introduce fault injection functionality.

A new class, `RegisterFaultInjector`, was added to provide the following helper methods:
* readFromFile()
* readMasks()
* readTimeIntervals()

The .cc and .hh files are inside `src/faultInjector/RISCV`.

### SimpleThread
File `src/cpu/simple_thread.hh` was modified to enable fault injection.
This file contains the definition of the SimpleThread class, containing the `getReg` and `setReg` methods. These methods were extended so that faults can be injected during register accesses.
The possible faults are:
* Stuck-at-0
* Stuck-at-1
* Bitflip

## Flow
Inside the SimpleThread's constructor, two configuration files are read:

### faultTimeIntervals.txt
This file defines the simulation time intervals (ticks) during which faults may be injected.

The file must contain a list of time instants, where:

* odd-numbered lines represent lower bounds
* even-numbered lines represent upper bounds

For example:
```
100
200
500
700
```

defines the intervals:

* [100, 200]
* [500, 700]

Outside these intervals, the Register File behaves normally.

### registerMasks.txt
It stores the faults to be injected, using the format: `index mask type`, where:
* Index indicates the register index
* Mask indicates which bits to affect
* Type can be `ST0`, `ST1` or `BITFLIP`

### Fault Injection Behavior

Whenever a register is accessed for reading, the simulator checks the accessed register index and the current simulation tick.

If both the register and time interval match the configuration, the corresponding fault is injected.

Current limitation: only the integer register class is considered.

## FaultLogs
If the simulation is ran with DebugFlag `FaultLogs`, the timestamps of the time instants when registers are accessed are logged. It logs only the registers being accessed in one of the time instants specified in faultTimeIntervals.txt.

## Building gem5
To build gem5 it is enough to run:
```
scons build/RISCV/gem5.opt
```

## Building the m5 library
The m5 library can be useful if one wants to include some m5 function calls directly in the c files of the programs to be simulated. For example, one can run `m5_dump_stats(0, 0)` or `m5_exit(0)`.

To do so, first:
```
scons build/riscv/out/m5
```

Then add this include statement in the program:
```
#include "gem5/m5ops.h"
```

Finally, the program can be compiled with:

```
riscv64-unknown-elf-gcc -static -o execFile.elf srcFile.c -Ipath/to/myGem5/include/ path/to/myGem5/util/m5/build/riscv/out/libm5.a
```

## Python config file
A proper python configuration file should be passed as argument to `gem5.opt`.
The `configs/faultInjector/minor-riscv-fault-injector.py` is the one which will be used by the fault injector described in the [Fault Injector Repository](https://github.com/stefano-galati/faultInjector).
