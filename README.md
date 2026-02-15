# GREEK++ Compiler
This project implements a compiler for the educational programming language **greek++**.  
The compiler reads a source file written in greek++ (`.gr`) and translates it into an equivalent **Assembly (`.asm`)** file.

It was developed as part of the **“Μεταφραστές” (Compilers)** course at the **University of Ioannina**.

## Description

The compiler includes the following stages:

- **Lexical Analysis** – Tokenizes the source code into meaningful symbols.
- **Syntax & Semantic Analysis** – Validates program structure, grammar rules, and logical consistency.
- **Code Generation** – Produces the final Assembly output file.

---

## Features
- Full compilation pipeline (Lexing → Parsing → Code Generation)
- Error detection and reporting for invalid syntax
- Educational implementation focused on clarity and structure
- Assembly output compatible with standard assemblers

---

## Requirements
- **Python 3.8 or higher**

You can check your Python version with:

```bash
python --version
```

---

## How to Run

1. Place your greek++ source file (e.g., `program.gr`) inside the project directory.
2. Open a terminal in the project folder.
3. Run the compiler:

```bash
python compiler.py program.gr
```

4. The generated `.asm` file will appear in the same directory.

---

## Project Structure (Example)

```
CompilerGreek++
│
├── compiler.py
├── lexer.py
├── parser.py
├── codegen.py
└── examples/
```

---

## Educational Purpose
This project is intended for **learning and experimentation** with compiler construction concepts such as parsing, semantic analysis, and low-level code generation.


---

## Team
- Areti Kirpitsa
- Athina Stasinou
