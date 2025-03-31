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
from cocotb.queue import Queue                                         s_wb_err,

# Class: wishboneClassicMaster
# Drive slave devices over the Wishbone Classic bus
class wishboneClassicMaster(wishboneClassicBase):
  # Constructor: __init__
  # Setup defaults and call base class constructor.
  def __init__(self, entity, name, clock, reset, *args, **kwargs):
    super().__init__(entity, name, clock, reset, *args, **kwargs)

    self.log.info("Wishbone Classic Master version %s", __version__)
    self.log.info("Copyright (c) 2025 Jay Convertino")
    self.log.info("https://github.com/johnathan-convertino-afrl/cocotbext-wishbone")

    # setup bus to default value imediatly
    if self._cti.value != False:
      self._cti.setimmediatevalue(0)

    if self._bte.value != False:
      self._bte.setimmediatevalue(0)

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
        temp.append(wishboneClassicTrans(a))
      temp = await self.read_trans(temp)
      #need a return with the data list only. This is only a guess at this point
      return [temp[i].data for i in range(len(temp))]
    else:
      trans = await self.read_trans(wishboneClassicTrans(address))
      return trans.data

  # Function: write
  # Write to a address some data
  async def write(self, address, data):
    if(isinstance(address, list) or isinstance(data, list)):
      if(len(address) != len(data)):
        self.log.error(f'Address and data vector must be the same length')
      temp = []
      for i in range(len(address)):
        temp.append(wishboneClassicTrans(address[i], data[i]))
      await self.write_trans(temp)
    else:
      await self.write_trans(wishboneClassicTrans(address, data))

  # Function: _check_type
  # Check and make sure we are only sending 2 bytes at a time and that it is a bytes/bytearray
  def _check_type(self, trans):
      if(not isinstance(trans, wishboneClassicTrans)):
          self.log.error(f'Transaction must be of type: {type(wishboneClassicTrans)}')
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

# Class: wishboneClassicEchoSlave
# Respond to master reads and write by returning data, simple echo core.
class wishboneClassicEchoSlave(wishboneClassicBase):
  # Constructor: __init__
  # Setup defaults and call base class constructor.
  def __init__(self, entity, name, clock, reset, numreg=256, *args, **kwargs):
    super().__init__(entity, name, clock, reset, *args, **kwargs)

    self.log.info("Wishbone Classic Slave version %s", __version__)
    self.log.info("Copyright (c) 2025 Jay Convertino")
    self.log.info("https://github.com/johnathan-convertino-afrl/cocotbext-wishbone")

    self.bus.pready.setimmediatevalue(0)
    self.bus.prdata.setimmediatevalue(0)
    self.bus.pslverr.setimmediatevalue(0)

    self._registers = {}

    for i in range(numreg):
      self._registers[i] = 0

  # Function: _next_address
  # Function to generate next address based on cycle type
  def _next_address(self, trans):
    # what type of cycle
    # what type of burst
    # if its something different then we need to do a end-of-burst and hold off
    return True # :) address in the future

  # Function: _check_type
  # Check and make sure we are only sending a type of wishboneClassicTrans.
  def _check_type(self, trans):
      if(not isinstance(trans, wishboneClassicTrans)):
          self.log.error(f'Transaction must be of type: {type(wishboneClassicTrans)}')
          return False

      return True

  # Method: _run
  # _run thread that deals with read and write request over bus.
  async def _run(self):
    self.active = False

    while True:
      await RisingEdge(self.clock)
