
import m5

from m5.objects import *
from m5.objects.O3CPU import O3CPU

system = System()
system.multi_thread = True

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]

system.cpu = O3CPU()
system.cpu.numThreads = 2
system.cpu.smtNumFetchingThreads = 1
system.cpu.smtFetchPolicy = "RoundRobin"
system.cpu.smtCommitPolicy = "RoundRobin"

system.cpu.fetchWidth = 4
system.cpu.decodeWidth = 4
system.cpu.renameWidth = 4
system.cpu.dispatchWidth = 4
system.cpu.issueWidth = 4
system.cpu.wbWidth = 4
system.cpu.commitWidth = 4

system.membus = SystemXBar()

system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

process1 = Process(pid=100)
process1.cmd = ["./ilp_basic"]

process2 = Process(pid=101)
process2.cmd = ["./ilp_basic"]

system.cpu.workload = [process1, process2]
system.cpu.createThreads()

system.cpu.createInterruptController()

for i in range(system.cpu.numThreads):
    system.cpu.interrupts[i].pio = system.membus.mem_side_ports
    system.cpu.interrupts[i].int_requestor = system.membus.cpu_side_ports
    system.cpu.interrupts[i].int_responder = system.membus.mem_side_ports

system.workload = SEWorkload.init_compatible(process1.cmd[0])

root = Root(full_system=False, system=system)

m5.instantiate()

print("Starting O3CPU ILP simulation")

exit_event = m5.simulate()

print("Simulation completed")
print("Exit cause:", exit_event.getCause())
print("Simulated ticks:", m5.curTick())
