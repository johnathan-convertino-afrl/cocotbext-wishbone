#******************************************************************************
# file:    absbus.py
#
# author:  JAY CONVERTINO
#
# date:    2025/03/11
#
# about:   Brief
# abstraction of the apb3 bus
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

import cocotb

from ..busbase import *

import enum

# Class: wishboneClassicTrans
# create an object that associates a data member and address for operation.
class wishboneClassicTrans(transaction):
    def __init__(self, address, data=None):
        self.address = address
        self.data = data

# Class: wishboneClassicState
# An enum class that provides the current state and will change states per spec.
class wishboneClassicState(enum.IntEnum):
  IDLE = 1
  SETUP = 2
  ACCESS = 3
  ERROR = 99

# Class: wishboneClassicBase
# abstract base class that defines Wishbone Classic signals
class wishboneClassicBase(busbase):
  # Variable: _signals
  # List of signals that are required
  _signals = ["data_o", "data_i", "addr", "ack", "sel", "we", "stb", "err"]
  # Variable: _optional_signals
  # List of optional signals, these will never be required but will be used if found.
  _optional_signals = ["cti", "bte"]

  # Constructor: __init__
  # Setup defaults and call base class constructor.
  def __init__(self, entity, name, clock, reset, *args, **kwargs):

    super().__init__(entity, name, clock, *args, **kwargs)

    self._state = wishboneClassicState.IDLE

    self._reset = reset
