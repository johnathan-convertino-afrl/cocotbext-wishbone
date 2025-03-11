# Cocotbext for Wishbone Bus
### cocotb extension for Wishbone Classic, and Pipeline

![image](docs/manual/img/AFRL.png)

---

   author: Jay Convertino   
   
   date: 2025.03.11
   
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

### DEPENDENCIES
#### Build
  - cocotb (python)

### COMPONENTS

```bash
├── cocotbext
│   └── wishbone
│       ├── __init__.py
│       ├── version.py
│       ├── wishbone_classic
│       │   ├── absbus.py
│       │   ├── driver.py
│       │   └── monitor.py
│       └── wishbone_pipeline
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
    ├── wishbone_classic
    │   ├── Makefile
    │   ├── test_wishbone.py
    │   └── test_wishbone.v
    └── wishbone_pipeline
        ├── Makefile
        ├── test_wishbone.py
        └── test_wishbone.v

```
