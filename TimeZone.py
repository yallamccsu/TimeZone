import tkinter
import sys
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import reduce


class Region(Enum):
    EASTERN          = auto()
    CENTRAL          = auto()
    MOUNTAIN         = auto()
    PACIFIC          = auto()
    HAWAII_ALEUTIAN  = auto()
    ALASKA           = auto()


@dataclass(frozen=True)
class TimeZoneRecord:
    city: str
    region: Region
    utc_offset: int
    observes_dst: bool

    def display_name(self) -> str:
        return self.region.name.replace('_', '-').title()

    def offset_label(self) -> str:
        sign = '-' if self.utc_offset < 0 else '+'
        return f"UTC{sign}{abs(self.utc_offset)}"


CITY_REGISTRY: List[TimeZoneRecord] = [
    TimeZoneRecord("New York",     Region.EASTERN,         -5, True),
    TimeZoneRecord("Minneapolis",  Region.CENTRAL,         -6, True),
    TimeZoneRecord("Denver",       Region.MOUNTAIN,        -7, True),
    TimeZoneRecord("San Francisco",Region.PACIFIC,         -8, True),
    TimeZoneRecord("Anchorage",    Region.ALASKA,          -9, True),
    TimeZoneRecord("Honolulu",     Region.HAWAII_ALEUTIAN, -10, False),
]

CITY_INDEX: Dict[str, TimeZoneRecord] = {r.city: r for r in CITY_REGISTRY}

FONT_LABEL   = ('Arial', 11)
FONT_HEADER  = ('Arial', 11, 'bold')
FONT_RESULT  = ('Arial', 11, 'bold')


def _lookup_city(name: str) -> Optional[TimeZoneRecord]:
    return CITY_INDEX.get(name)


def _sorted_city_names(registry: List[TimeZoneRecord]) -> List[str]:
    # sort by utc offset so the list reads west to east
    sorted_records = sorted(registry, key=lambda r: r.utc_offset)
    return [r.city for r in sorted_records]


def _compute_offset_spread(registry: List[TimeZoneRecord]) -> int:
    offsets = [r.utc_offset for r in registry]
    return reduce(lambda span, o: max(span, o) - min(span, o), offsets, 0)


class TimeZoneLookupEngine:
    def __init__(self, registry: List[TimeZoneRecord] = CITY_REGISTRY):
        self._registry = registry
        self._history: List[Tuple[str, TimeZoneRecord]] = []

    def query(self, city: str) -> Optional[TimeZoneRecord]:
        result = _lookup_city(city)
        if result:
            self._history.append((city, result))
        return result

    def get_history(self) -> List[Tuple[str, TimeZoneRecord]]:
        return list(self._history)

    def most_queried(self) -> Optional[str]:
        if not self._history:
            return None
        counts: Dict[str, int] = {}
        for city, _ in self._history:
            counts[city] = counts.get(city, 0) + 1
        return max(counts, key=lambda k: counts[k])


class TimeZone:
    def __init__(self):
        self.engine = TimeZoneLookupEngine()

        self._timezone_var  = tkinter.StringVar()
        self._offset_var    = tkinter.StringVar()
        self._dst_var       = tkinter.StringVar()

        self.main_window = tkinter.Tk()
        self.main_window.title("Time Zones")
        self.main_window.resizable(False, False)

        self.__build_prompt_label()
        self.__build_listbox()
        self.__build_output_frame()
        self.__build_button_row()

        tkinter.mainloop()

    def __build_prompt_label(self):
        tkinter.Label(
            self.main_window,
            text="select a city",
            font=FONT_HEADER,
        ).pack(padx=5, pady=6)

    def __build_listbox(self):
        self.__city_names = _sorted_city_names(CITY_REGISTRY)
        self.city_listbox = tkinter.Listbox(
            self.main_window,
            height=len(self.__city_names),
            width=20,
            font=FONT_LABEL,
            selectmode=tkinter.SINGLE,
        )
        self.city_listbox.pack(padx=10, pady=4)
        self.city_listbox.bind('<<ListboxSelect>>', self.__handle_selection)

        for city in self.__city_names:
            self.city_listbox.insert(tkinter.END, city)

    def __build_output_frame(self):
        outer = tkinter.Frame(self.main_window)
        outer.pack(padx=10, pady=6)

        # each output row shares the same structure
        rows = [
            ("time zone:",  self._timezone_var),
            ("utc offset:", self._offset_var),
            ("dst:",        self._dst_var),
        ]
        for label_text, var in rows:
            row = tkinter.Frame(outer)
            tkinter.Label(row, text=label_text, font=FONT_LABEL, width=12, anchor='w').pack(side='left', padx=4)
            tkinter.Label(
                row,
                textvariable=var,
                font=FONT_RESULT,
                width=18,
                anchor='w',
                borderwidth=1,
                relief='solid',
            ).pack(side='left', padx=4)
            row.pack(pady=3)

    def __build_button_row(self):
        frame = tkinter.Frame(self.main_window)
        tkinter.Button(
            frame, text="clear", command=self.__handle_clear, width=10
        ).pack(side='left', padx=5)
        tkinter.Button(
            frame, text="quit", command=self.__handle_quit, width=10
        ).pack(side='left', padx=5)
        frame.pack(pady=8)

    def __handle_selection(self, event):
        selection = self.city_listbox.curselection()
        if not selection:
            return
        city = self.city_listbox.get(selection[0])
        record = self.engine.query(city)
        if record is None:
            self._timezone_var.set("not found")
            self._offset_var.set("")
            self._dst_var.set("")
            return
        self._timezone_var.set(record.display_name())
        self._offset_var.set(record.offset_label())
        self._dst_var.set("yes" if record.observes_dst else "no")

    def __handle_clear(self):
        self.city_listbox.selection_clear(0, tkinter.END)
        self._timezone_var.set("")
        self._offset_var.set("")
        self._dst_var.set("")

    def __handle_quit(self):
        self.main_window.destroy()
        sys.exit(0)


if __name__ == '__main__':
    TimeZone()
