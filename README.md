# Text Editor

**Category:** Text

## Problem

Notepad style application that can open, edit, and save text documents. Optional: Add syntax highlighting and other features.

## Solution

Two front ends share one `Document` model: `--gui` opens a Tkinter window with Open/Save-as menus (requires Tk), while the default mode is a line editor with view/append/insert/delete/replace/save commands. The model itself is headless and fully testable, as the demo shows.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --gui
python3 main.py draft.txt
python3 main.py --demo
```

## Example

```text
1 | First final line
   2 | Inserted in the middle
saved: draft.txt (40 bytes)
```

## Attribution

The problem statement is from [karan/Projects](https://github.com/karan/Projects), a list of practical projects that anyone can solve in any programming language (MIT License, Copyright (c) 2013 Karan Goel). The Python solution in this repository was implemented by [bspreston-esq](https://github.com/bspreston-esq).

This repository is part of the [Projects-Python-All](https://github.com/bspreston-esq/Projects-Python-All) collection.
