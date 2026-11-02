#!/usr/bin/env python3
"""A small text editor: Tkinter GUI when available, otherwise a line editor."""
import argparse
import os
import tempfile

class Document:
    def __init__(self, path=None):
        self.path = path
        self.lines = []
        if path and os.path.exists(path):
            with open(path, encoding="utf-8", errors="ignore") as fh:
                self.lines = fh.read().splitlines()

    def view(self) -> str:
        return "\n".join(f"{i+1:>4} | {line}" for i, line in enumerate(self.lines))

    def append(self, text: str) -> None:
        self.lines.append(text)

    def insert(self, line_number: int, text: str) -> None:
        if not 1 <= line_number <= len(self.lines) + 1:
            raise ValueError("line number out of range")
        self.lines.insert(line_number - 1, text)

    def delete(self, line_number: int) -> None:
        if not 1 <= line_number <= len(self.lines):
            raise ValueError("line number out of range")
        del self.lines[line_number - 1]

    def replace(self, old: str, new: str) -> int:
        replaced = 0
        for index, line in enumerate(self.lines):
            if old in line:
                self.lines[index] = line.replace(old, new)
                replaced += 1
        return replaced

    def save(self, path=None) -> str:
        target = path or self.path
        if not target:
            raise ValueError("no filename set; use 'save <path>'")
        with open(target, "w", encoding="utf-8") as fh:
            fh.write("\n".join(self.lines) + ("\n" if self.lines else ""))
        self.path = target
        return target

def gui(path=None) -> int:
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
    except ImportError:
        print("Tkinter is not installed. Use the line editor instead (omit --gui).")
        return 1
    root = tk.Tk()
    root.title("Text Editor")
    text = tk.Text(root, undo=True, wrap="word")
    text.pack(fill="both", expand=True)
    if path and os.path.exists(path):
        text.insert("1.0", open(path, encoding="utf-8").read())

    def open_file():
        chosen = filedialog.askopenfilename()
        if chosen:
            text.delete("1.0", "end")
            text.insert("1.0", open(chosen, encoding="utf-8").read())
            root.title(f"Text Editor - {chosen}")

    def save_file():
        chosen = filedialog.asksaveasfilename(defaultextension=".txt")
        if chosen:
            with open(chosen, "w", encoding="utf-8") as fh:
                fh.write(text.get("1.0", "end-1c"))
            messagebox.showinfo("Saved", f"Saved to {chosen}")

    menu = tk.Menu(root)
    file_menu = tk.Menu(menu, tearoff=0)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save as", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Quit", command=root.destroy)
    menu.add_cascade(label="File", menu=file_menu)
    root.config(menu=menu)
    root.mainloop()
    return 0

def line_editor(document: Document) -> None:
    print("Commands: view | append TEXT | insert N TEXT | delete N | replace OLD NEW | save [PATH] | quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw:
            continue
        command, _, rest = raw.partition(" ")
        try:
            if command == "view":
                print(document.view())
            elif command == "append":
                document.append(rest)
            elif command == "insert":
                number, _, text = rest.partition(" ")
                document.insert(int(number), text)
            elif command == "delete":
                document.delete(int(rest))
            elif command == "replace":
                old, _, new = rest.partition(" ")
                print(f"replaced on {document.replace(old, new)} line(s)")
            elif command == "save":
                print(f"saved {document.save(rest.strip() or None)}")
            elif command in ("quit", "exit"):
                break
            else:
                print("unknown command")
        except (ValueError, OSError) as exc:
            print(f"Error: {exc}")

def demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "draft.txt")
        document = Document()
        document.append("First draft line")
        document.append("Second draft line")
        document.insert(2, "Inserted in the middle")
        document.replace("draft", "final")
        document.delete(3)
        document.save(path)
        print(document.view())
        print(f"saved: {path} ({os.path.getsize(path)} bytes)")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?")
    parser.add_argument("--gui", action="store_true", help="open the Tkinter editor")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        demo()
    elif args.gui:
        raise SystemExit(gui(args.file))
    else:
        line_editor(Document(args.file))

if __name__ == "__main__":
    main()
