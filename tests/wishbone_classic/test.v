//******************************************************************************
// file:    test.v
//
// author:  JAY CONVERTINO
//
// date:    2025/03/17
//
// about:   Brief
// Test bench for apb using cocotb
//
// license: License MIT
// Copyright 2025 Jay Convertino
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to
// deal in the Software without restriction, including without limitation the
// rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
// sell copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
// IN THE SOFTWARE.
//
//******************************************************************************

`timescale 1ns/100ps

/*
 * Module: test
 *
 * Test of Wishbone Classic
 *
 * Parameters:
 *
 *   ADDRESS_WIDTH   - Width of the Wishbone address port in bits.
 *   BUS_WIDTH       - Width of the Wishbone bus data port in bytes.
 *
 * Ports:
 *
 *   clk              - Clock
 *   rst              - Positive reset
 *   s_wb_cyc         - Bus Cycle in process
 *   s_wb_stb         - Valid data transfer cycle
 *   s_wb_we          - Active High write, low read
 *   s_wb_addr        - Bus address
 *   s_wb_data_i      - Input data
 *   s_wb_sel         - Device Select
 *   s_wb_ack         - Bus transaction terminated
 *   s_wb_data_o      - Output data
 *   s_wb_err         - Active high when a bus error is present
 */
module test #(
    parameter ADDRESS_WIDTH = 16,
    parameter BUS_WIDTH     = 4
  )
  (
    input                                           clk,
    input                                           rst,
    inout                                           s_wb_cyc,
    inout                                           s_wb_stb,
    inout                                           s_wb_we,
    inout   [ADDRESS_WIDTH-1:0]                     s_wb_addr,
    inout   [BUS_WIDTH*8-1:0]                       s_wb_data_i,
    inout   [BUS_WIDTH-1:0]                         s_wb_sel,
    inout                                           s_wb_ack,
    inout   [BUS_WIDTH*8-1:0]                       s_wb_data_o,
    inout                                           s_wb_err
  );

  //copy pasta, fst generation
  initial
  begin
    $dumpfile("test.fst");
    $dumpvars(0,test);
  end

endmodule
