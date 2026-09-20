#!/usr/bin/env python3
"""
Captain Cubemelon & Friends: Gadget Sandbox, for /play/.

>>> ONE CONSTANT TURNS THE PAGE ON. <<<

    ITCH_URL = "https://carrster43.itch.io/captain-cubemelon-gadget-sandbox"
    python3 make_play.py && python3 build.py && python3 nav.py

While ITCH_URL is None:
  - make_play.py REFUSES to write the page and says why
  - nav.py emits no Play link on any page
  - build.py leaves /play/ out of the sitemap

so there is no way to ship a nav item, a sitemap entry or a page pointing at a
game nobody can buy. That is the failure this guard exists for: the itch project
is created by hand, on a day that is not today, and a half-live link is the
thing most likely to be left behind.

The price and status here must match the itch page. They are stated on the site
because a visitor deciding whether to click through deserves to know both before
they leave, and because "in development" is the reason the price is what it is.
"""

# ------------------------------------------------------------------ the switch
ITCH_URL = None          # e.g. "https://carrster43.itch.io/captain-cubemelon-gadget-sandbox"
PRICE = "$3.99"
STATUS = "In development"
VERSION = "0.14.0"
# -----------------------------------------------------------------------------

TITLE = "Captain Cubemelon & Friends: Gadget Sandbox"
TAGLINE = ("A puzzle platformer where nothing is an enemy. Twelve worlds, one "
           "Gravity Wrench, and glitches you repair instead of fight.")

# Load-bearing, and the same paragraph that leads the itch description. It is
# what makes $3.99 honest rather than merely cheap, so it goes ABOVE the price
# on this page too, not in a footnote under it.
DISCLOSURE = (
    "This is an in development release and the price reflects that. All twelve "
    "worlds are built and playable from the first badge to the last, and the "
    "game saves. What is not finished is the look and the sound: the characters "
    "are drawn, but the worlds are still clean geometry rather than painted "
    "scenery, and the audio is synthesized tones with no music yet. Buy it now "
    "and every update is included, the art pass among them."
)

HOOK = (
    "Captain Cubemelon does not carry a weapon. He carries a Gravity Wrench, "
    "which lifts, pulls and pushes, and he walks into twelve worlds' worth of "
    "things that have stopped working properly. Every glitch in the game went "
    "wrong for a reason, and the way past it is to work out the reason. Nothing "
    "in it is an enemy. Nothing in it dies."
)

FACTS = [
    ("Twelve worlds, two seasons",
     "Season One is machinery: springs and fans, momentum, ice, wind, gears and "
     "conveyors, and Portal Park itself as the sixth. Season Two is the Glitch "
     "Blocks arc, where the worlds themselves are the thing that went wrong."),
    ("One wrench, three modes",
     "Lift, Pull and Push, switched on the fly. Five gears each grant a small "
     "power while you carry them, and none of them gate anything."),
    ("Forty seven characters from the books",
     "An ability station for each of the main cast, and a badge from every world "
     "that seats into the Master Gate and says what it taught you."),
    ("It saves, and it means it",
     "Versioned, validated, and it survives being closed, corrupted or reset."),
    ("Reduced motion is a real setting",
     "Not a label. With it on, the drifting ambient particles in every world are "
     "placed once as still specks, with no movement and no flashing."),
]

# Keyboard only. There is no gamepad or touch support yet and the page says so,
# because claiming it is how a browser game earns refunds.
CONTROLS = [
    ("Move", "A / D, or the arrow keys"),
    ("Jump", "W, Up, or Space"),
    ("Talk, advance dialogue", "E"),
    ("Gravity Wrench", "F to use, R to switch mode"),
    ("Pause", "P or Escape"),
]

# The art that IS finished. Deliberately the cast rather than screenshots: the
# world scenery is the unfinished part, and leading a sales page with it would
# undercut the disclosure two paragraphs above.
HERO = "/assets/game/captain_cubemelon_large.png"
CAST = [
    ("drip_byte.png", "Drip Byte"),
    ("patch_bolt.png", "Patch Bolt"),
    ("pip_pop.png", "Pip Pop"),
    ("ember_slice.png", "Ember Slice"),
    ("moss_guard.png", "Moss Guard"),
    ("brick_bloom.png", "Brick Bloom"),
]
