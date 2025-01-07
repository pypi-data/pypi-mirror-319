# AltColor

AltColor is a package designed to add color to text in console based applications.

## All predefined colors(colors that are not RGB) **[Credit to [colorama]('https://pypi.org/project/colorama/') for a few of the colors]**: 
"BLACK"
"RED"
"GREEN"
"YELLOW"
"BLUE"
"MAGENTA"
"CYAN"
"WHITE"
"LIGHTBLACK"
"LIGHTRED"
"LIGHTGREEN"
"LIGHTYELLOW"
"LIGHTBLUE"
"LIGHTMAGENTA"
"LIGHTCYAN"
"LIGHTWHITE"

## Installation

Install via pip:

```bash
pip install altcolor
```

Example code: 

```py
from altcolor import *

# Colored text allows you to paint your words with RGB
print(colored_text((244, 5, 7), "Hello World!"))

# Here's a regular print
print("Hello World!")

# We even have predefined colors
print(colored_text("BLUE", "Hello World!"))


# Leaked text splills into other print statements until you use reset()
print(leaked_text("RED", "Hey,"))
print("you")
print("are" + reset())

# Leaked text can even spill into the background
print(leaked_text("WHITE", "cool!", "Back"))
print("How")
print("are")
print("you?" + reset())
```