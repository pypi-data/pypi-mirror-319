from colorama import Fore, Back, Style
from typing import Union, Tuple, Dict

def reset() -> str:
    """
    Resets all styles and colors to the terminal's default settings.

    Returns:
        str: ANSI escape code for resetting styles.
    """
    return Style.RESET_ALL

def Color(r: int, g: int, b: int) -> str:
    """
    Generates an ANSI escape code for custom RGB text color.

    Args:
        r (int): Red component (0-255).
        g (int): Green component (0-255).
        b (int): Blue component (0-255).

    Returns:
        str: ANSI escape code for the specified RGB color.
    """
    return f"\033[38;2;{r};{g};{b}m"

def colored_text(color: Union[str, Tuple[int, int, int]], text: str, style: str = "Fore") -> str:
    """
    Applies color and style to a given text using ANSI escape codes.

    Args:
        color (Union[str, Tuple[int, int, int]]): Color name (e.g., "RED") or RGB tuple (e.g., (255, 0, 0)).
        text (str): Text to be styled.
        style (str, optional): Determines whether to apply foreground ("Fore") or background ("Back") color. Defaults to "Fore".

    Returns:
        str: Styled text with the specified color and style.

    Raises:
        TypeError: If the style is invalid or the color format is incorrect.
    """
    style = style.capitalize()

    predefined_styles: Dict[str, str] = {}
    if style == "Fore":
        predefined_styles = {
            "BLACK": Fore.BLACK,
            "RED": Fore.RED,
            "GREEN": Fore.GREEN,
            "YELLOW": Fore.YELLOW,
            "BLUE": Fore.BLUE,
            "MAGENTA": Fore.MAGENTA,
            "CYAN": Fore.CYAN,
            "WHITE": Fore.WHITE,
            "LIGHTBLACK": Fore.LIGHTBLACK_EX,
            "LIGHTRED": Fore.LIGHTRED_EX,
            "LIGHTGREEN": Fore.LIGHTGREEN_EX,
            "LIGHTYELLOW": Fore.LIGHTYELLOW_EX,
            "LIGHTBLUE": Fore.LIGHTBLUE_EX,
            "LIGHTMAGENTA": Fore.LIGHTMAGENTA_EX,
            "LIGHTCYAN": Fore.LIGHTCYAN_EX,
            "LIGHTWHITE": Fore.LIGHTWHITE_EX,
        }
    elif style == "Back":
        predefined_styles = {
            "BLACK": Back.BLACK,
            "RED": Back.RED,
            "GREEN": Back.GREEN,
            "YELLOW": Back.YELLOW,
            "BLUE": Back.BLUE,
            "MAGENTA": Back.MAGENTA,
            "CYAN": Back.CYAN,
            "WHITE": Back.WHITE,
            "LIGHTBLACK": Back.LIGHTBLACK_EX,
            "LIGHTRED": Back.LIGHTRED_EX,
            "LIGHTGREEN": Back.LIGHTGREEN_EX,
            "LIGHTYELLOW": Back.LIGHTYELLOW_EX,
            "LIGHTBLUE": Back.LIGHTBLUE_EX,
            "LIGHTMAGENTA": Back.LIGHTMAGENTA_EX,
            "LIGHTCYAN": Back.LIGHTCYAN_EX,
            "LIGHTWHITE": Back.LIGHTWHITE_EX,
        }
    else:
        raise TypeError("[ALTCOLOR]: Invalid style!")

    if isinstance(color, str) and color.upper() in predefined_styles:
        return predefined_styles[color.upper()] + text + Style.RESET_ALL
    elif isinstance(color, tuple) and len(color) == 3:
        return Color(color[0], color[1], color[2]) + text + Style.RESET_ALL
    else:
        raise TypeError("[ALTCOLOR]: Invalid color!")

def leaked_text(color: Union[str, Tuple[int, int, int]], text: str, style: str = "Fore") -> str:
    """
    Applies color and style to a given text without resetting styles at the end.

    Args:
        color (Union[str, Tuple[int, int, int]]): Color name (e.g., "RED") or RGB tuple (e.g., (255, 0, 0)).
        text (str): Text to be styled.
        style (str, optional): Determines whether to apply foreground ("Fore") or background ("Back") color. Defaults to "Fore".

    Returns:
        str: Styled text with the specified color and style.

    Raises:
        TypeError: If the style is invalid or the color format is incorrect.
    """
    style = style.capitalize()

    predefined_styles: Dict[str, str] = {}
    if style == "Fore":
        predefined_styles = {
            "BLACK": Fore.BLACK,
            "RED": Fore.RED,
            "GREEN": Fore.GREEN,
            "YELLOW": Fore.YELLOW,
            "BLUE": Fore.BLUE,
            "MAGENTA": Fore.MAGENTA,
            "CYAN": Fore.CYAN,
            "WHITE": Fore.WHITE,
            "LIGHTBLACK": Fore.LIGHTBLACK_EX,
            "LIGHTRED": Fore.LIGHTRED_EX,
            "LIGHTGREEN": Fore.LIGHTGREEN_EX,
            "LIGHTYELLOW": Fore.LIGHTYELLOW_EX,
            "LIGHTBLUE": Fore.LIGHTBLUE_EX,
            "LIGHTMAGENTA": Fore.LIGHTMAGENTA_EX,
            "LIGHTCYAN": Fore.LIGHTCYAN_EX,
            "LIGHTWHITE": Fore.LIGHTWHITE_EX,
        }
    elif style == "Back":
        predefined_styles = {
            "BLACK": Back.BLACK,
            "RED": Back.RED,
            "GREEN": Back.GREEN,
            "YELLOW": Back.YELLOW,
            "BLUE": Back.BLUE,
            "MAGENTA": Back.MAGENTA,
            "CYAN": Back.CYAN,
            "WHITE": Back.WHITE,
            "LIGHTBLACK": Back.LIGHTBLACK_EX,
            "LIGHTRED": Back.LIGHTRED_EX,
            "LIGHTGREEN": Back.LIGHTGREEN_EX,
            "LIGHTYELLOW": Back.LIGHTYELLOW_EX,
            "LIGHTBLUE": Back.LIGHTBLUE_EX,
            "LIGHTMAGENTA": Back.LIGHTMAGENTA_EX,
            "LIGHTCYAN": Back.LIGHTCYAN_EX,
            "LIGHTWHITE": Back.LIGHTWHITE_EX,
        }
    else:
        raise TypeError("[ALTCOLOR]: Invalid style!")

    if isinstance(color, str) and color.upper() in predefined_styles:
        return predefined_styles[color.upper()] + text
    elif isinstance(color, tuple) and len(color) == 3:
        return Color(color[0], color[1], color[2]) + text
    else:
        raise TypeError("[ALTCOLOR]: Invalid color!")

def cPrint(
    color: Union[Tuple[int, int, int], str] = "WHITE",
    text: str = "",
    style: str = "Fore",
    objective: str = "controlled",
) -> None:
    """
    Prints colored text to the console, with options for resetting styles or leaking styles.

    Args:
        color (Union[Tuple[int, int, int], str], optional): Text color, either as a predefined color name or an RGB tuple. Defaults to "WHITE".
        text (str, optional): Text to be printed. Defaults to an empty string.
        style (str, optional): Style of color application ("Fore" for text color, "Back" for background color). Defaults to "Fore".
        objective (str, optional): Determines whether to reset styles after printing ("controlled") or leave styles active ("leaked"). Defaults to "controlled".

    Returns:
        None

    Raises:
        TypeError: If the objective is not "controlled" or "leaked".
    """
    if objective.lower() == "controlled":
        print(colored_text(color=color, text=text, style=style))
    elif objective.lower() == "leaked":
        print(leaked_text(color=color, text=text, style=style))
    else:
        raise TypeError("[ALTCOLOR]: Invalid objective!")

# Credits:
cPrint(color="BLUE", text="\n\nThanks for using AltColor! Consider using our other products at 'https://tairerullc.vercel.app'\n\n")