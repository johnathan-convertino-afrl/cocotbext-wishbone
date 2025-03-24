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
 * Test bench loop for apb
 *
 * Parameters:
 *
 *   ADDRESS_WIDTH   - Width of the APB3 address port in bits.
 *   BUS_WIDTH       - Width of the APB3 bus data port in bytes.
 *
 * Ports:
 *
 *   clk            - Clock
 *   rstn           - Negative reset
 *   apb_paddr      - APB3 address bus, up to 32 bits wide.
 *   apb_psel       - APB3 select per slave (1 for this core).
 *   apb_penable    - APB3 enable device for multiple transfers after first.
 *   apb_pready     - APB3 ready is a output from the slave to indicate its able to process the request.
 *   apb_pwrite     - APB3 Direction signal, active high is a write access. Active low is a read access.
 *   apb_pwdata     - APB3 write data port.
 *   apb_prdata     - APB3 read data port.
 *   apb_pslverror  - APB3 error indicates transfer failure, not implimented.
 */
module test #(
    parameter ADDRESS_WIDTH = 32,
    parameter BUS_WIDTH = 4
  )
  (
    input                       clk,
    input                       rstn,
    inout [ADDRESS_WIDTH-1:0]   apb_paddr,
    inout                       apb_psel,
    inout                       apb_penable,
    inout                       apb_pwrite,
    inout [BUS_WIDTH*8-1:0]     apb_pwdata,
    inout                       apb_pready,
    inout [BUS_WIDTH*8-1:0]     apb_prdata,
    inout                       apb_pslverr
  );

  //copy pasta, fst generation
  initial
  begin
    $dumpfile("test.fst");
    $dumpvars(0,test);
  end

endmodule
