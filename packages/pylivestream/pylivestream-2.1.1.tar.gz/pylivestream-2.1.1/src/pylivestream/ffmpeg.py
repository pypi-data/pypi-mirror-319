from __future__ import annotations
import typing as T
import subprocess
from time import sleep
import os
from pathlib import Path
import shutil
import json
import functools


class Ffmpeg:
    def __init__(self):

        self.ERROR = ["-loglevel", "error"]
        self.WARNING = ["-loglevel", "warning"]
        self.INFO = ["-loglevel", "info"]

        self.YES = ["-y"]

        # default 8, increasing can help avoid warnings
        self.QUEUE = ["-thread_queue_size", "8"]

        # https://trac.ffmpeg.org/wiki/StreamingGuide#The-reflag
        self.THROTTLE = "-re"

    def timelimit(self, t: str | int | float | None) -> list[str]:
        if t is None:
            return []

        assert isinstance(t, (str, int, float))

        t = str(t)

        if len(t) > 0:
            return ["-t", str(t)]
        else:
            return []

    def drawtext(self, text: str) -> list[str]:
        # fontfile=/path/to/font.ttf:
        if not text:  # None or '' or [] etc.
            return []

        fontcolor = "fontcolor=white"
        fontsize = "fontsize=24"
        box = "box=1"
        boxcolor = "boxcolor=black@0.5"
        border = "boxborderw=5"
        x = "x=(w-text_w)/2"
        y = "y=(h-text_h)*3/4"

        return [
            "-vf",
            f"drawtext=text='{text}':{fontcolor}:{fontsize}:{box}:{boxcolor}:{border}:{x}:{y}",
        ]

    def listener(self):
        """
        no need to check return code, errors will show up in client.

        -timeout 1 is necessary to avoid instant error, since stream starts after the listener.
        I put -timeout 5 to allow for very slow computers.
        -timeout is the delay to wait for stream input before erroring.

        sleep: 0.2 not long enough. 0.3 worked, so set 0.5 for some margin.
        """

        TIMEOUT = 0.5

        cmd = [get_ffplay(), "-loglevel", "error", "-timeout", "5", "-autoexit", "rtmp://localhost"]

        print(
            "starting Localhost RTMP listener. \n\n",
            " ".join(cmd),
            "\n\n Press   q   in this terminal to end stream.",
        )

        proc = subprocess.Popen(cmd)

        #        proc = subprocess.Popen(['ffmpeg', '-v', 'fatal', '-timeout', '5',
        #                                 '-i', 'rtmp://localhost', '-f', 'null', '-'],
        #                                stdout=subprocess.DEVNULL)

        sleep(TIMEOUT)

        return proc

    def movingBG(self, bgfn: Path | None = None) -> list[str]:
        if not bgfn:
            return []

        bg = str(bgfn)
        if os.name == "nt":
            bg = bg.replace("\\", "/")  # for PureWindowsPath

        return ["-filter_complex", f"movie={bg}:loop=0,setpts=N/FRAME_RATE/TB"]


@functools.cache
def get_exe(name: str) -> str:

    for p in (os.environ.get("FFMPEG_ROOT"), None):
        if exe := shutil.which(name, path=p):
            return exe

    raise FileNotFoundError(
        f"""
*** Must have FFmpeg + FFprobe installed to use PyLivestream.
https://www.ffmpeg.org/download.html

could not find {name}
"""
    )


def get_ffmpeg() -> str:
    return get_exe("ffmpeg")


def get_ffplay() -> str:
    return get_exe("ffplay")


def get_ffprobe() -> str:
    return get_exe("ffprobe")


def get_meta(fn: Path, exein: str | None = None) -> dict[str, T.Any]:
    if not fn:  # audio-only
        return {}

    fn = Path(fn).expanduser()

    if not fn.is_file():
        raise FileNotFoundError(fn)

    exe = get_exe("ffprobe") if exein is None else exein

    cmd = [
        str(exe),
        "-loglevel",
        "error",
        "-print_format",
        "json",
        "-show_streams",
        "-show_format",
        str(fn),
    ]

    ret = subprocess.check_output(cmd, text=True)
    # %% decode JSON from FFprobe
    return json.loads(ret)
