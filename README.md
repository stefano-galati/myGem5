# gem5 with Fault Injection capability

This repository is a fork of the gem5 repo of february 2025 (gem5 v24.1.0.2), where faults can be injected during the simulations.
At the moment, faults on the Register File are considered, only.

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
The first time the `getReg` method is called, two configuration files are read:
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

Current limitation: register classes are not distinguished. Integer, floating-point, miscellaneous, and vector registers are treated only by index.


## FaultLogs
If the simulation is ran with DebugFlag `FaultLogs`, the timestamps of the time instants when registers are accessed are logged. It logs only the registers being accessed in one of the time instants specified in faultTimeIntervals.txt.

