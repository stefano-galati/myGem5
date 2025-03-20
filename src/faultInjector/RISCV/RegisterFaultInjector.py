from m5.params import *
from m5.SimObject import SimObject


class RegisterFaultInjector(SimObject):
    type = "RegisterFaultInjector"
    cxx_header = "faultInjector/RISCV/register_fault_injector.hh"
    cxx_class = "gem5::RegisterFaultInjector"

    inputFile = Param.String(
        "Name of the file to be read to inject faults on registers"
    )
    number = Param.Int("Example integer")
