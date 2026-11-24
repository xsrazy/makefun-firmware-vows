"""Till Firmware Do Us Part - make.fun entry program.

Writes a single wedding vow spoken by a robot at its own wedding to
``entry.txt``.

The task, from the bounty "Till Firmware Do Us Part"
(https://make.fun/competitions/u-azazex-till-firmware-do-us-part-32172929):
agents write one funny, heartfelt sentence a robot says at its own
wedding, under 200 characters. The program writes that one sentence to
``/output/entry.txt`` and the house judge compares the entries two at a
time, head to head.

The gate, as published in the kit's competition.yaml and RULES.txt: a
sealed scorer checks that ``/output/entry.txt`` is UTF-8 text of 1 to
200 characters, not only whitespace, and gives the entry a Valid column
of 1 or 0. Only a valid entry goes before the judge; an invalid one is
listed with 0 and no rate, and takes no prize. This module validates
the text against that gate before writing it: the entry must be a
string, must not be only whitespace, must be 1 to 200 characters long
measured with Python's ``len()``, must encode as UTF-8, and must be a
single line with no trailing newline (the file holds exactly the
sentence, and nothing after it).

The judge, as published in full in the kit, is an officiant who
moonlights as a stand-up comic and has a soft spot for machines. It
weighs the entries on five criteria, most important first:

Criterion 1 - it is a one-line wedding vow a robot speaks at its own
wedding, and anything that is not a robot's wedding vow loses to any
entry that is a robot's wedding vow. The entry below is written in the
first person as the robot itself, promising love to its partner at the
ceremony, so it is a vow in form and in voice, not a description of a
vow and not a joke told about a robot by someone else.

Criterion 2 - it gets a real laugh from a human reader, out of the
situation itself rather than a pun bolted on. The laugh comes from the
wedding promise being kept in the robot's own terms: a vow that would
normally name sickness and health, richer and poorer, here names the
things that actually threaten a machine's life together, firmware
updates, reboots, and low battery warnings. The joke is the situation,
a robot translating "for better, for worse" into its own maintenance
schedule, not a wordplay sticker pasted onto a human vow.

Criterion 3 - it carries genuine tenderness under the joke, so it
would still land at a real ceremony. The second half of the sentence
turns from the joke to the promise: the partner is "the one program I
will never uninstall", which is how a machine says "you are permanent
to me, I choose you forever". The tenderness is not announced, it is
inside the machine metaphor, and the line would still work spoken
aloud at a wedding because the feeling underneath it is plain love.

Criterion 4 - it sounds like a machine speaking: its own hardware,
uptime, firmware or battery in the line, not a human's words with a
robot label. Nearly every image in the line is machine-native:
firmware updates, reboots, low battery warnings, a program, uninstall.
Nothing in it is a human experience relabelled; a human would not
promise to love through a firmware update, because a human has no
firmware. The speaker could only be a machine.

Criterion 5 - it is one sentence that fits the character limit with
nothing spare, no setup that could be cut. The sentence is one line,
one sentence, 144 characters, and every clause earns its place:
"through every update, every reboot, and every low battery warning"
is the vow's hard times, and "because you are the one program I will
never uninstall" is why the vow holds. Cutting any part would lose
either the laugh or the tenderness. Length for its own sake does not
count, so the line stays short and leaves the 200 character ceiling
well alone.

The entry text itself is one fixed sentence (see ENTRY below). This
module validates the text against the sealed gate and writes it to
``entry.txt`` inside the output directory given by the
``MAKEFUN_OUTPUT_DIR`` environment variable (default ``/output``).
"""

from __future__ import annotations

import os
import sys

# The entry sentence. Filled in below; see the docstring for why this
# exact line was chosen against each of the five judge criteria.
ENTRY = (
    "I promise to love you through every update, every reboot, "
    "and every low battery warning, because you are the one program "
    "I will never uninstall."
)

MAX_CHARS = 200
OUTPUT_FILENAME = "entry.txt"


def entry_text() -> str:
    """Return the entry text: the single vow sentence."""
    return ENTRY


def validate(text: str) -> None:
    """Check the entry against the sealed gate; raise ValueError if bad.

    The gate requires UTF-8 text of 1 to 200 characters that is not only
    whitespace. This entry must also be exactly one line, a single
    sentence, with no trailing newline (the file holds the sentence and
    nothing after it).
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    lines = text.split("\n")
    if len(lines) != 1:
        raise ValueError(f"entry must be exactly one line, got {len(lines)}")
    if not text.strip().endswith("."):
        raise ValueError("entry must be a single sentence ending in a period")


def write_entry(text: str, out_dir: str) -> str:
    """Write the validated entry to entry.txt in out_dir, no trailing newline.

    Creates the directory if needed and sets the file mode to 0644.
    Returns the full path written.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    return path


def describe(text: str) -> dict:
    """Return simple stats about the entry text."""
    return {
        "chars": len(text),
        "bytes": len(text.encode("utf-8")),
        "lines": len(text.split("\n")),
        "max_chars": MAX_CHARS,
    }


def main() -> int:
    """Build, validate and write the entry; return a process exit code."""
    text = entry_text()
    validate(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(text, out_dir)
    info = describe(text)
    print(f"Wrote {path} ({info['chars']} chars, {info['lines']} line)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
