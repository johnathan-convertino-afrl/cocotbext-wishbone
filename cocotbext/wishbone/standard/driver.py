#******************************************************************************
# file:    driver.py
#
# author:  JAY CONVERTINO
#
# date:    2025/03/11
#
# about:   Brief
# Bus Driver for Wishbone Classic Master/echoSlave
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

# Class: wishboneStandardMaster
# Drive slave devices over the Wishbone Classic bus
class wishboneStandardMaster(wishboneStandardBase):
  # Constructor: __init__
  # Setup defaults and call base class constructor.
  def __init__(self, entity, name, clock, reset, *args, **kwargs):
    super().__init__(entity, name, clock, reset, *args, **kwargs)

    self.log.info("Wishbone Classic Master version %s", __version__)
    self.log.info("Copyright (c) 2025 Jay Convertino")
    self.log.info("https://github.com/johnathan-convertino-afrl/cocotbext-wishbone")

    self.bus.sel.setimmediatevalue(0)
    self.bus.data_i.setimmediatevalue(0)
    self.bus.addr.setimmediatevalue(0)
    self.bus.we.setimmediatevalue(0)
    self.bus.stb.setimmediatevalue(0)
    self.bus.cyc.setimmediatevalue(0)

  # Function: read
  # Read from a address and return data
  async def read(self, address):
    trans = None
    if(isinstance(address, list)):
      temp = []
      for a in address:
        temp.append(wishboneStandardTrans(a))
      temp = await self.read_trans(temp)
      #need a return with the data list only. This is only a guess at this point
      return [temp[i].data for i in range(len(temp))]
    else:
      trans = await self.read_trans(wishboneStandardTrans(address))
      return trans.data

  # Function: write
  # Write to a address some data
  async def write(self, address, data):
    if(isinstance(address, list) or isinstance(data, list)):
      if(len(address) != len(data)):
        self.log.error(f'Address and data vector must be the same length')
      temp = []
      for i in range(len(address)):
        temp.append(wishboneStandardTrans(address[i], data[i]))
      await self.write_trans(temp)
    else:
      await self.write_trans(wishboneStandardTrans(address, data))

  # Function: _check_type
  # Check and make sure we are only sending 2 bytes at a time and that it is a bytes/bytearray
  def _check_type(self, trans):
      if(not isinstance(trans, wishboneStandardTrans)):
          self.log.error(f'Transaction must be of type: {type(wishboneStandardTrans)}')
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
      if self._reset.value:
        self.bus.sel.value = 0
        self.bus.data_i.value = 0
        self.bus.addr.value = 0
        self.bus.we.value = 0
        self.bus.stb.value = 0
        self.bus.cyc.value = 0
        self._idle.set()
        continue

      # write queue is not empty, we need to write that data.
      if not self.wqueue.empty():
        self.active = True
        #keep in active loop
        while self.active:
          if(self._state == wishboneStandardState.IDLE):
            trans = await self.wqueue.get()
            self.bus.sel.value = ~0
            self.bus.addr.value = trans.address
            self.bus.data_i.value = trans.data
            self.bus.we.value = 1
            self.bus.stb.value = 1
            self.bus.cyc.value = 1
            self._idle.set()
            self.log.info(f'WISHBONE STANDARD MASTER STATE: {self._state.name} BUS WRITE')
            self._state = wishboneStandardState.ACTIVE
          elif(self._state == wishboneStandardState.ACTIVE):
            if(self.wqueue.empty() and self.bus.ack.value):
              self.bus.stb.value = 0
              self.bus.sel.value = 0
              self.bus.addr.value = 0
              self.bus.data_i.value = 0
              self.bus.we.value = 0
              self.bus.stb.value = 0
              self.bus.cyc.value = 0
              self._idle.set()
              self.active = False
              self._state = wishboneStandardState.IDLE
            elif(self.bus.ack.value):
              trans = await self.wqueue.get()
              self.bus.sel.value = ~0
              self.bus.addr.value = trans.address
              self.bus.data_i.value = trans.data
              self.bus.we.value = 1
              self.bus.stb.value = 1
              self.bus.cyc.value = 1
              self._idle.set()
              self.log.info(f'WISHBONE STANDARD MASTER STATE: {self._state.name} BUS WRITE')

          #all operations are done on rising edge of clock
          await RisingEdge(self.clock)

      # request queue is not empty, do a read.
      elif not self.qqueue.empty():
        self.active = True
        #keep in active loop
        while self.active:
          if(self._state == wishboneStandardState.IDLE):
            trans = await self.qqueue.get()
            self.bus.sel.value = ~0
            self.bus.addr.value = trans.address
            self.bus.we.value = 0
            self.bus.stb.value = 1
            self.bus.cyc.value = 1
            self._idle.set()
            self.log.info(f'WISHBONE STANDARD MASTER STATE: {self._state.name} BUS READ')
            self._state = wishboneStandardState.ACTIVE
          elif(self._state == wishboneStandardState.ACTIVE):
            # queue is empty and we are ready, time to go to idle.wishboneClassic
            if(self.qqueue.empty() and self.bus.ack.value):
              trans.data = self.bus.data_o.value
              await self.rqueue.put(trans)
              self.bus.sel.value = 0
              self.bus.stb.value = 0
              self.bus.cyc.value = 0
              self.bus.addr.value = 0
              self._state = wishboneStandardState.IDLE
              self.active = False
              self._idle.set()
            # acked and not empty, lets idle the active thread.
            elif(self.bus.ack.value):
              trans.data = self.bus.data_o.value
              await self.rqueue.put(trans)
              trans = await self.qqueue.get()
              self.bus.sel.value = ~0
              self.bus.we.value = 0
              self.bus.addr.value = trans.address
              self.bus.stb.value = 1
              self.bus.cyc.value = 1
              self._idle.set()
              self.log.info(f'WISHBONE STANDARD MASTER STATE: {self._state.name} BUS READ')

          # all operations happen on positive edge
          await RisingEdge(self.clock)

      else:
        # nothing in the queues, idle and set all values to zero
        self._idle.set()

        self.bus.we.value = 0
        self.bus.addr.value = 0
        self.bus.data_i.value = 0
        self.bus.sel.value = 0
        self.bus.stb.value = 0
        self.bus.cyc.value = 0



# Class: wishboneStandardEchoSlave
# Respond to master reads and write by returning data, simple echo core.
class wishboneStandardEchoSlave(wishboneStandardBase):
  # Constructor: __init__
  # Setup defaults and call base class constructor.
  def __init__(self, entity, name, clock, reset, numreg=256, *args, **kwargs):
    super().__init__(entity, name, clock, reset, *args, **kwargs)

    self.log.info("Wishbone Classic Echo Slave version %s", __version__)
    self.log.info("Copyright (c) 2025 Jay Convertino")
    self.log.info("https://github.com/johnathan-convertino-afrl/cocotbext-wishbone")

    self.bus.err.setimmediatevalue(0)
    self.bus.data_o.setimmediatevalue(0)
    self.bus.ack.setimmediatevalue(0)

    self._registers = {}

    for i in range(numreg):
      self._registers[i] = 0

  # Function: _check_type
  # Check and make sure we are only sending a type of wishboneStandardTrans.
  def _check_type(self, trans):
      if(not isinstance(trans, wishboneStandardTrans)):
          self.log.error(f'Transaction must be of type: {type(wishboneStandardTrans)}')
          return False

      return True

  # Method: _run
  # _run thread that deals with read and write request over bus.
  async def _run(self):
    self.active = False

    while True:
      await RisingEdge(self.clock)

      if not self._reset.value:
        self.active = True
        previous_state = self._state
        while self.active:
          if(self._state == wishboneStandardState.IDLE):
            if(self.bus.cyc.value and self.bus.stb.value):
              self.bus.err.value = 0
              self.bus.ack.value = 1
              if(self.bus.we.value):
                self._registers[self.bus.addr.value.integer] = self.bus.data_i.value
              else:
                self.bus.data_o.value = self._registers[self.bus.addr.value.integer]

              self._idle.set()
              self._state = wishboneStandardState.ACTIVE
            elif(not self.bus.cyc.value):
              self.active = False
          elif(self._state == wishboneStandardState.ACTIVE):
            if(not self.bus.cyc.value):
              self.active = False

            if(self.bus.cyc.value and self.bus.stb.value):
              self.bus.ack.value = 0
              self._state = wishboneStandardState.IDLE
              self._idle.set()

          if(previous_state != self._state):
            self.log.info(f'WISHBONE STANDARD ECHO SLAVE STATE: {self._state.name}')

          previous_state = self._state

          await RisingEdge(self.clock)
      else:
        self._idle.set()

        self._state = wishboneStandardState.IDLE

        self.bus.ack.value = 0
        self.bus.err.value = 0
        self.bus.data_o.value = 0
