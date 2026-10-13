AI generated

# STerm

Small serial terminal with a dark GUI, written in Python (tkinter + pyserial).

## Features

- Port, baudrate, parity, stop bits, data bits and RTS/CTS flow control settings
- Timestamped log of sent and received data
- Visible line endings: `\r`, `\n` and `\r\n` are shown in orange
- Selectable line ending appended to sent text: None / CR / LF / CRLF
- Received data without a line ending is finished on a new line after a short silence
- Works on Windows and Linux

## Run from source

Requires Python 3.9+ with tkinter.

```bash
pip install pyserial
python gui_terminal.py
```

On Debian/Ubuntu install tkinter first (`sudo apt install python3-tk`) 
and use a virtual environment, because system `pip` is locked:

```bash
python3 -m venv venv
./venv/bin/pip install pyserial
./venv/bin/python gui_terminal.py
```

## Usage

1. **Settings** - choose port and parameters, press **Save**.
2. **Connect** - opens the port. **Detach** closes it.
3. Type text into the bottom field and press Enter. The line ending selected in
   **Send line ending** is appended.
4. `/port settings` typed into the input field prints the current settings.

Linux: to access serial ports your user must be in the `dialout` group:

```bash
sudo usermod -aG dialout $USER   # then log out and in again
```

## Build a standalone executable

### Windows

```bat
pip install pyinstaller pyserial
pyinstaller --onefile --windowed --name STerm --icon icon.ico gui_terminal.py
```

Result: `dist\STerm.exe`

### Linux

```bash
sudo apt install python3-tk python3-venv
python3 -m venv venv
./venv/bin/pip install pyinstaller pyserial
./venv/bin/pyinstaller --onefile --name STerm gui_terminal.py
chmod +x dist/STerm
```

Result: `dist/STerm`. The binary depends on the glibc version of the build
system - build on the oldest distribution you want to support.
