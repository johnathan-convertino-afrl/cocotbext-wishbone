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

# Class: wishboneClassicState
# An enum class that provides the current operation state.
class wishboneClassicState(enum.IntEnum):
  IDLE  = 1
  WRITE = 2
  READ  = 3
  ERROR = 99

# Class: wishboneCycleState
# An enum class that provides the current cycle state.
class wishboneCycleState(enum.IntEnum):
  CLASSIC   = 0
  CONT_ADDR = 1
  INCR_ADDR = 2
  END_BURST = 7

# Class: wishboneBurstState
# An enum class that provides the current burst type.
class wishboneBurstState(enum.IntEnum):
  LINEAR        = 0
  FOUR_BEAT     = 1
  EIGHT_BEAT    = 2
  SIXTEEN_BURST = 3

# Class: wishboneClassicTrans
# Create an object that associates data, address, and a cycle type.
# Idea is to send a list of the same cycle type, and when it changes cycle/burst type or is empty then do end of burst.
class wishboneClassicTrans(transaction):
    def __init__(self, address, data=None, cycle : wishboneCycleState = CLASSIC, burst : wishboneBurstState = LINEAR):
        self.address = address
        self.data = data
        self.cycle = cycle
        self.burst = burst

# Class: wishboneClassicBase
# abstract base class that defines Wishbone Classic signals
class wishboneClassicBase(busbase):
  # Variable: _signals
  # List of signals that are required
  _signals = ["data_o", "data_i", "addr", "ack", "sel", "we", "stb"]
  # Variable: _optional_signals
  # List of optional signals, these will never be required but will be used if found.
  _optional_signals = ["cti", "bte", "err", "rty"]

  # Constructor: __init__
  # Setup defaults and call base class constructor.
  def __init__(self, entity, name, clock, reset, *args, **kwargs):

    super().__init__(entity, name, clock, *args, **kwargs)

    self._state = wishboneClassicState.IDLE

    self._reset = reset

    # Assign a noSignal object with a value attribute. That way if we
    # do a simple if check, cti does not exist and disables burst (value is always false).
    self._cti = getattr(self.bus, "ack", noSignal(False))

    # Assign a noSignal object with a value attribute. That way if we
    # do a simple if check, bte does not exist and disables burst (value is always false).
    self._bte = getattr(self.bus, "bte", noSignal(False))

    # Assign a noSignal object with a value attribute. That way if we
    # do a simple if check, err does not exist and disables burst (value is always false).
    self._err = getattr(self.bus, "err", noSignal(False))

    # Assign a noSignal object with a value attribute. That way if we
    # do a simple if check, rty does not exist and disables burst (value is always false).
    self._rty = getattr(self.bus, "rty", noSignal(False))
