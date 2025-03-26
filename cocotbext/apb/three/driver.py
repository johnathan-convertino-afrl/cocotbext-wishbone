#******************************************************************************
# file:    driver.py
#
# author:  JAY CONVERTINO
#
# date:    2025/03/11
#
# about:   Brief
# Bus Driver for APB3
#
# license: License MIT
# Copyright 2025 Jay Convertino
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
#******************************************************************************

from ..version import __version__
from .absbus import *

from cocotb.triggers import FallingEdge, RisingEdge, Event
from cocotb.result import TestFailure
from cocotb.binary import BinaryValue
from cocotb.queue import Queue

# Class: apb3Master
# Drive slave devices over the APB3 bus
class apb3Master(apb3Base):
  # Constructor: __init__
  # Setup defaults and call base class constructor.
  def __init__(self, entity, name, clock, resetn, *args, **kwargs):
    super().__init__(entity, name, clock, resetn, *args, **kwargs)

    self.log.info("APB3 Master")
    self.log.info("APB3 Master version %s", __version__)
    self.log.info("Copyright (c) 2025 Jay Convertino")
    self.log.info("https://github.com/johnathan-convertino-afrl/cocotbext-apb")

    # setup bus to default value imediatly
    self.bus.paddr.setimmediatevalue(0)
    self.bus.psel.setimmediatevalue(0)
    self.bus.penable.setimmediatevalue(0)
    self.bus.pwrite.setimmediatevalue(0)
    self.bus.pwdata.setimmediatevalue(0)

  # Function: read
  # Read from a address and return data
  async def read(self, address):
    trans = None
    if(isinstance(address, list)):
      temp = []
      for a in address:
        temp.append(apb3trans(a))
      temp = await self.read_trans(temp)
      #need a return with the data list only. This is only a guess at this point
      return [temp[i].data for i in range(len(temp))]
    else:
      trans = await self.read_trans(apb3trans(address))
      return trans.data

  # Function: write
  # Write to a address some data
  async def write(self, address, data):
    if(isinstance(address, list) or isinstance(data, list)):
      if(len(address) != len(data)):
        self.log.error(f'Address and data vector must be the same length')
      temp = []
      for i in range(len(address)):
        temp.append(apb3trans(address[i], data[i]))
      await self.write_trans(temp)
    else:
      await self.write_trans(apb3trans(address, data))

  # Function: _check_type
  # Check and make sure we are only sending 2 bytes at a time and that it is a bytes/bytearray
  def _check_type(self, trans):
      if(not isinstance(trans, apb3trans)):
          self.log.error(f'Transaction must be of type: {type(apb3trans)}')
          return False

      return True

  # Method: _run
  # _run thread that deals with read and write queues.
  async def _run(self):
    self.active = False

    trans = None

    while True:
      await RisingEdge(self.clock)

      # when in reset, set values and idle.
      if not self._resetn.value:
        self.bus.psel.value = 0
        self.bus.paddr.value = 0
        self.bus.penable.value = 0
        self.bus.pwrite.value = 0
        self.bus.pwdata.value = 0
        self._idle.set()
        continue

      # write queue is not empty, we need to write that data.
      if not self.wqueue.empty():
        self.active = True
        #keep in active loop
        while self.active:
          self.log.info(f'APB3 MASTER STATE: {self._apbStateMachine.name} BUS WRITE')
          if(self._apbStateMachine == apbState.IDLE):
            trans = await self.wqueue.get()
            self.bus.psel.value = 1
            self.bus.paddr.value = trans.address
            self.bus.pwdata.value = trans.data
            self.bus.pwrite.value = 1
            self._apbStateMachine = apbState.SETUP
          elif(self._apbStateMachine == apbState.SETUP):
            self.bus.penable.value = 1
            self.bus.paddr.value = trans.address
            self.bus.pwdata.value = trans.data
            self._apbStateMachine = apbState.ACCESS
          elif(self._apbStateMachine == apbState.ACCESS):
            # no longer idle as we have nothing else to write
            if(self.wqueue.empty() and self.bus.pready.value):
              self.bus.psel.value = 0
              self.bus.penable.value = 0
              self._apbStateMachine = apbState.IDLE
              self.active = False
              self._idle.set()
            # still active, but we do have a second to idle
            elif(self.bus.pready.value):
              trans = await self.wqueue.get()
              self.bus.penable.value = 0
              self._apbStateMachine = apbState.SETUP
              self._idle.set()

          #all operations are done on rising edge of clock
          await RisingEdge(self.clock)

      # request queue is not empty, do a read.
      elif not self.qqueue.empty():
        self.active = True
        #keep in active loop
        while self.active:
          self.log.info(f'APB3 MASTER STATE: {self._apbStateMachine.name} BUS READ')
          if(self._apbStateMachine == apbState.IDLE):
            trans = await self.qqueue.get()
            self.bus.psel.value = 1
            self.bus.paddr.value = trans.address
            self.bus.pwrite.value = 0
            self._apbStateMachine = apbState.SETUP
          elif(self._apbStateMachine == apbState.SETUP):
            self.bus.penable.value = 1
            self._apbStateMachine = apbState.ACCESS
          elif(self._apbStateMachine == apbState.ACCESS):
            # queue is empty and we are ready, time to go to idle.
            if(self.qqueue.empty() and self.bus.pready.value):
              trans.data = self.bus.prdata.value
              await self.rqueue.put(trans)
              self.bus.psel.value = 0
              self.bus.penable.value = 0
              self._apbStateMachine = apbState.IDLE
              self.active = False
              self._idle.set()
            # ready and not empty, lets idle the active thread.
            elif(self.bus.pready.value):
              trans = await self.qqueue.get()
              self.bus.penable.value = 0
              self.bus.paddr.value = trans.address
              trans.data = self.bus.prdata.value
              await self.rqueue.put(trans)
              self._apbStateMachine = apbState.SETUP
              self._idle.set()

          # all operations happen on positive edge
          await RisingEdge(self.clock)

      else:
        # nothing in the queues, idle and set all values to zero
        self._idle.set()

        self.bus.psel.value = 0
        self.bus.paddr.value = 0
        self.bus.penable.value = 0
        self.bus.pwrite.value = 0
        self.bus.pwdata.value = 0

# Class: apb3EchoSlave
# Respond to master reads and write by returning data, simple echo core.
class apb3EchoSlave(apb3Base):
  # Constructor: __init__
  # Setup defaults and call base class constructor.
  def __init__(self, entity, name, clock, resetn, numreg=256, *args, **kwargs):
    super().__init__(entity, name, clock, resetn, *args, **kwargs)

    self.log.info("APB3 Slave")
    self.log.info("APB3 Slave version %s", __version__)
    self.log.info("Copyright (c) 2025 Jay Convertino")
    self.log.info("https://github.com/johnathan-convertino-afrl/cocotbext-apb")

    self.bus.pready.setimmediatevalue(0)
    self.bus.prdata.setimmediatevalue(0)
    self.bus.pslverr.setimmediatevalue(0)

    self._registers = {}

    for i in range(numreg):
      self._registers[i] = 0

  # Function: _check_type
  # Check and make sure we are only sending a type of apb3trans.
  def _check_type(self, trans):
      if(not isinstance(trans, apb3trans)):
          self.log.error(f'Transaction must be of type: {type(apb3trans)}')
          return False

      return True

  # Method: _run
  # _run thread that deals with read and write request over bus.
  async def _run(self):
    self.active = False

    while True:
      await RisingEdge(self.clock)

      if self.bus.psel.value and self._resetn:
        self.active = True
        while self.active:
          self.log.info(f'APB3 SLAVE STATE: {self._apbStateMachine.name}')

          if(self._apbStateMachine == apbState.IDLE):
            self.bus.pslverr.value = 0
            self.bus.pready.value = 0
            if(self.bus.psel.value):
              self._apbStateMachine = apbState.SETUP
          elif(self._apbStateMachine == apbState.SETUP):
            if(self.bus.psel.value and self.bus.penable.value):
              self.bus.pready.value = 1
              if self.bus.pwrite.value:
                self._registers[self.bus.paddr.value.integer] = self.bus.pwdata.value
              else:
                self.bus.prdata.value = self._registers[self.bus.paddr.value.integer]
              self._apbStateMachine = apbState.ACCESS
            else:
              self._apbStateMachine = apbState.IDLE
              self.bus.pready.value = 0
              self.active = False
              self._idle.set()
          elif(self._apbStateMachine == apbState.ACCESS):
            if(self.bus.psel.value and self.bus.penable.value):
              self.bus.pready.value = 0
              self._apbStateMachine = apbState.SETUP
              self.bus.prdata.value = 0
              self._idle.set()
            else:
              self._apbStateMachine = apbState.IDLE
              self.bus.pready.value = 0
              self.bus.prdata.value = 0
              self.active = False
              self._idle.set()

          await RisingEdge(self.clock)
      else:
        self._idle.set()

        self._apbStateMachine = apbState.IDLE

        self.bus.pready.value = 0
        self.bus.prdata.value = 0
        self.bus.pslverr.value = 0
