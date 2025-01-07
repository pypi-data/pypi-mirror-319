"""
Classes for Shell-Style package.
This module defines _BaseObject, Theme, Console, ProgressBar and Table.
"""

from time import sleep
from os import get_terminal_size
from abc import ABC
from typing import Any
from .constants import *

# Set __all__
__all__ = ["Theme", "Console", "Table", "ProgressBar", "DEFAULT_THEME"]

class _BaseObject(ABC):
    """
    Abstract Base Class for all other classes defined here.
    Defines the help method.
    
    Args: None
    """
    
    @classmethod
    def help(cls) -> str:
        return f"""{FG_CYAN}{cls.__name__}{STOP}\n{cls.__doc__}"""

class Theme(_BaseObject):
    """
    Class for themes. 
    
    Args:
        **styles
    """
    
    def __init__(self, **styles) -> None:
        self._styles = styles
        
    @property
    def styles(self) -> dict[str, Any]:
        return self._styles
    
    @styles.setter
    def styles(self, **styles) -> None:
        self._styles.update(styles)
        
    def get_style(self, target: str) -> str:
        return self._styles.get(target)

DEFAULT_THEME = Theme(info=FG_CYAN, warning=FG_YELLOW, error=FG_RED, success=FG_GREEN, bold=BOLD, dim=DIM, italic=ITALIC, 
                    underline=UNDERLINE, blink=BLINK, inverse=INVERSE, hidden=HIDDEN, strikethrough=STRIKETHROUGH, 
                    fg_black=FG_BLACK,fg_white=FG_WHITE, fg_green=FG_GREEN, fg_yellow=FG_YELLOW, fg_blue=FG_BLUE, 
                    fg_magenta=FG_MAGENTA, fg_cyan=FG_CYAN, bg_black=BG_BLACK, bg_red=BG_RED, bg_green=BG_GREEN, 
                    bg_yellow=BG_YELLOW, bg_blue=BG_BLUE, bg_magenta=BG_MAGENTA, bg_cyan=BG_CYAN, bg_white=BG_WHITE)

class Console(_BaseObject):
    """
    Console object on which text can be printed and input can be taken.

    Args:
        title: str, 
        theme: Theme = DEFAULT_THEME
    """
    
    def __init__(self, title: str, theme: Theme = DEFAULT_THEME, print_title: bool = True) -> None:
        self._title = title
        self._theme = theme
        
        if print_title:
            self.print_title()
        
    def print_title(self) -> None:
        self.write(f"{BOLD}{UNDERLINE}{self._title}{STOP}", alignment=CENTER)
        
    @property
    def theme(self) -> Theme:
        return self._theme
    
    @theme.setter
    def theme(self, new: Theme = DEFAULT_THEME) -> None:
        self._theme = new
        
    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, new: str) -> None:
        self._title = new
    
    def clear(self, print_title: bool = True) -> None:
        """
        Clear the terminal.
        
        Args:
            print_title: bool = True
            
        Returns: None
        """
        
        print(CLEAR, end="")
        if print_title:
            self.print_title()
        
    def log(self, text: Any, *, end: str = f"{STOP}\n", 
            sep: str = " ", style: str = "default", alignment: str = LEFT) -> None:
        """
        Customized log method.
        
        Args: 
            text: Any, 
            end: str = f"{STOP}\n",
            alignment: str = LEFT,
            sep: str = " ", 
            style: str = "default"
            
        Returns: None
        """
        
        print(self._align_text(self._theme.get_style(style) + text, alignment), end=end, sep=sep)
            
    def write(self, text: Any, *, alignment: str = LEFT, end: str = f"{STOP}\n", 
              sep: str = " ", style: str = "default") -> None:
        """
        Customized print method.
        
        Args:
            text: Any,
            alignment: str, 
            end: str = STOP, 
            sep: str = "", 
            style: str
        
        Returns: None
        """
        
        print(self._align_text(self._theme.get_style(style) + text, alignment), end=end, sep=sep)
        
    def prompt(self, text: Any, *, end: str = STOP, style: str = "default") -> str:
        """
        Customized input method.
        
        Args:
            text: Any,
            end: str = STOP, 
            style: str
        
        Returns: str
        """
        
        return input(self._theme.get_style(style) + text + end)
    
    @staticmethod
    def _align_text(text: Any, alignment: str) -> str | None:
        """
        Private static method for text alignment
        
        Args:
            text: Any, 
            alignment: str
        
        Returns: str 
        
        Raises: ValueError (if alignment is not valid)
        """
        width = get_terminal_size().columns
        
        if alignment == CENTER:
            padding = (width - len(text)) // 2
            return " " * padding + text + " " * (width - len(text) - padding)
        
        elif alignment == RIGHT:
            return (" " * (width - len(text)) + text).rstrip(" ")
        
        elif alignment == LEFT:
            return (text + " " * (width - len(text))).lstrip(" ")
        
        else:
            raise ValueError(f"Invalid argument for function 'Console._align_text': {alignment}")
    
class ProgressBar(_BaseObject):
    """
    Class for representing basic progress bars.
    
    Args:
        values: int,
        theme: Theme = DEFAULT_THEME
        symbol: str = "-",
        delay: float = 1
    """
    
    def __init__(self, values: int, *, theme: Theme = DEFAULT_THEME, symbol: str = "-", 
                 delay: float = 1) -> None:
        self._values = values
        self._theme = theme
        self._symbol = symbol
        self._delay = delay
        
    @property
    def values(self) -> int:
        return self._values
    
    @values.setter
    def values(self, new: int) -> None:
        self._values = new
        
    @property
    def theme(self) -> Theme:
        return self._theme
    
    @theme.setter
    def theme(self, new: Theme) -> None:
        self._theme = new
        
    @property
    def symbol(self) -> str:
        return self._symbol
    
    @symbol.setter
    def symbol(self, new: str) -> None:
        self._symbol = new
        
    @property
    def delay(self) -> float:
        return self._delay
    
    @delay.setter
    def delay(self, new: float) -> None:
        self._delay = new
        
    def run(self, style: str = "default", del_self: bool = False) -> None:
        """
        Run the progress bar.
        
        Args:
            style: str = "default",
            del_self: bool = False
            
        Returns: None
        """
        
        for _ in range(self._values):
            print(self._theme.get_style(style) + self._symbol, end=STOP, flush=True)
            sleep(self._delay)
            
        if del_self:
            del self
            
class Table(_BaseObject):
    """
    Table class for representing data.
    
    Args: 
        columns: int = 0
    """
    
    def __init__(self, columns: int = 0) -> None:
        self._columns = columns
        self._rows = 0
        self._table = []
        
    def add_row(self, *objects: Any) -> None:
        """
        Add a row to self._table.
        
        Args:
            *objects: Any
            
        Returns: None
        """
        
        objects = list(objects)
        
        while len(objects) < self._columns:
            objects.append(None)
            
        while len(objects) > self._columns:
            objects.pop()
            
        self._table.append(objects)
        self._rows += 1
        
    def del_row(self, index: int) -> None:
        """
        Delete a row in self._table.
        
        Args:
            index: int
            
        Returns: None    
        """
        
        del self._table[index]
        self._rows -= 1
        
    def del_column(self, index: int) -> None:
        """
        Delete a column in self._table.
        
        Args:
            index: int
            
        Returns: None
        """
        
        for row in self._table:
            del row[index]
            
        self._columns -= 1
        
    def add_column(self, placeholder: Any = "") -> None:
        """
        Add a column in self._table.
        
        Args:
            placeholder: Any = ""
            
        Returns: None
        """
        
        for row in self._table:
            row.append(placeholder)
        
        self._columns += 1
            
    def get_column(self, row_index: int, column_index: int) -> Any:
        """
        Get the information in a column in self._table.
        
        Args:
            row_index: int,
            column_index: int
            
        Returns: Any
        """
        
        return self._table[row_index][column_index]
    
    def set_column(self, info: Any, row_index: int, column_index: int) -> None:
        """
        Set the information in a column in self._table.
        
        Args:
            info: Any,
            row_index: int,
            column_index: int
            
        Returns: None
        """
        
        self._table[row_index][column_index] = info
        
    def get_row(self, index: int) -> list:
        """
        Returns a row in self._table.
        
        Args:
            index: int
            
        Returns: list
        """
        
        return self._table[index]
    
    def get_table(self) -> str:
        """
        Return a string representation of self._table.
        
        Args: None
        
        Returns: str
        """
        
        return_str = ""
        
        for row in self._table:
            return_str += "| " + " | ".join(str(cell) if cell is not None else "" for cell in row) + " |" + "\n"
            
        return return_str
    
    def display(self) -> None:
        print(self.get_table())
        
    @property
    def rows(self) -> int:
        return self._rows
    
    @property
    def columns(self) -> int:
        return self._columns
    
    @property
    def table(self) -> list[list]:
        return self._table
    