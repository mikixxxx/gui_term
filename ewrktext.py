import re
import datetime
import tkinter as tk

# \r\n must be first, so that it is matched as one token and not as \r + \n
EOL_RE = re.compile(r"\r\n|\r|\n")
EOL_LABELS = {"\r\n": "\\r\\n", "\r": "\\r", "\n": "\\n"}


class extText(tk.Text):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(state="disabled")
        self.tag_configure("timestamp", foreground="green")
        self.tag_configure("shortmsg", foreground="green", font=("Arial", 10, "bold"))
        # visible end-of-line marker (\r, \n, \r\n) in a different color
        self.tag_configure("eol", foreground="#ff9900")
        # shortmsg of the line that is still "open" (no EOL received yet)
        self._open_line = None

    def append(self, shortmsg, msg, stream=False):
        """Append a message to the terminal.

        EOL characters in msg are shown as a colored marker (\\r, \\n, \\r\\n)
        followed by a real line break.

        stream=True: data arrives in chunks (serial RX). A chunk that does not
        end with EOL leaves the line open and the next chunk continues on the
        same line (without a new timestamp).
        """
        if stream and not msg:
            return

        self.config(state="normal")

        # close a dangling line if something else is going to be printed
        if self._open_line is not None and not (stream and self._open_line == shortmsg):
            self.insert(tk.END, "\n")
            self._open_line = None

        # prefix only on a fresh line
        if self._open_line is None:
            timestamp = datetime.datetime.now().strftime("[%H:%M:%S] ")
            self.insert(tk.END, timestamp, "timestamp")
            self.insert(tk.END, f"{shortmsg}: ", "shortmsg")

        pos = 0
        for m in EOL_RE.finditer(msg):
            if m.start() > pos:
                self.insert(tk.END, msg[pos:m.start()])
            self.insert(tk.END, EOL_LABELS[m.group()], "eol")
            self.insert(tk.END, "\n")
            pos = m.end()
        if pos < len(msg):
            self.insert(tk.END, msg[pos:])

        ended_with_eol = pos > 0 and pos == len(msg)
        if stream:
            self._open_line = None if ended_with_eol else shortmsg
        else:
            if not ended_with_eol:
                self.insert(tk.END, "\n")
            self._open_line = None

        self.see(tk.END)
        self.config(state="disabled")

    def has_open_line(self):
        return self._open_line is not None

    def close_line(self):
        """Terminate a line that was left open (received data without EOL),
        so the next data start on a new line with a new timestamp."""
        if self._open_line is None:
            return
        self.config(state="normal")
        self.insert(tk.END, "\n")
        self._open_line = None
        self.see(tk.END)
        self.config(state="disabled")
