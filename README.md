# Cocotbext for Wishbone Bus
### Provides monitor and driver for Wishbone B4 versions.

![image](docs/manual/img/AFRL.png)

---

   author: Jay Convertino   
   
   date: 2025.03.31
   
   details:
   
   license: MIT   
   
---

### Version
#### Current
  - V0.0.0 - initial release

#### Previous
  - none

### DOCUMENTATION
  For detailed usage information, please navigate to one of the following sources. They are the same, just in a different format.

  - [cocotbext_wishbone.pdf](docs/manual/cocotbext_wishbone.pdf)
  - [github page](https://johnathan-convertino-afrl.github.io/cocotbext-wishbone/)

  Naming of the wishbone bus is as follows:

  - Wishbone Classic Standard = Wishbone Standard without out CTI/BTE
  - Wishbone Classic Registered = Wishbone Registered with CTI/BTE
  - Wishbone Classic Pipelined = Wishbone Pipelined

  Only Wishbone Classic Standard is done at the moment, and honestly will be the only one since I'm not a huge fan of Wishbone as a bus.

### DEPENDENCIES
#### Build
  - cocotb (python)

### COMPONENTS

  - cocotbext = Contains all of the various APB drivers by version.
  - docs = Contains all documents on how to use the core in PDF, and HTML formats.
  - tests = Contains test code to verify drivers and monitors.

```bash
├── cocotbext
│   └── wishbone
│       ├── busbase.py
│       ├── standard
│       │   ├── absbus.py
│       │   ├── driver.py
│       │   ├── __init__.py
│       │   └── monitor.py
│       └── version.py
├── docs
│   ├── index.html
│   └── manual
│       ├── cocotbext-wishbone.html
│       ├── config
│       │   ├── Comments.txt
│       │   ├── Languages.txt
│       │   ├── Project.txt
│       │   └── Working Data
│       │       ├── CodeDB.nd
│       │       ├── Comments.nd
│       │       ├── Files.nd
│       │       ├── Languages.nd
│       │       ├── Output
│       │       │   ├── BuildState.nd
│       │       │   ├── Config.nd
│       │       │   └── SearchIndex.nd
│       │       ├── Parser.nd
│       │       └── Project.nd
│       ├── css
│       │   └── custom_font_l2h.css
│       ├── html
│       ├── img
│       │   ├── AFRL.png
│       │   └── diagrams
│       ├── makefile
│       ├── makefiles
│       │   ├── makefuselatex.mk
│       │   ├── makehtml.mk
│       │   └── makepdf.mk
│       ├── py
│       │   └── gen_fusesoc_latex_info.py
│       └── src
│           ├── common.tex
│           ├── fusesoc
│           ├── html.tex
│           └── pdf.tex
├── LICENSE.md
├── MANIFEST.in
├── README.md
├── setup.cfg
├── setup.py
└── tests
    └── wishbone_standard
        ├── Makefile
        ├── test.py
        └── test.v

```
