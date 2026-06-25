# U.S. City Timezone Lookup Tool

A Python desktop application for querying timezone metadata by U.S. city. 
Built with Tkinter, the tool displays timezone name, UTC offset, and DST 
observance for any selected city from a structured registry.

## Features

- Select any city from a sortable listbox to instantly retrieve its timezone data
- Displays timezone name, UTC offset, and DST observance simultaneously
- Cities sorted west to east by UTC offset for intuitive navigation
- Query history logged internally with most-selected city tracking
- Reset and Quit controls for clean session management
- Input-safe with graceful fallback if a lookup returns no result

## How to Run

```bash
python TimeZone.py
```

No external dependencies. Requires Python 3 with Tkinter, which is 
included in all standard Python installations.

## Cities Covered

| City          | Timezone         | UTC Offset | DST |
|---------------|------------------|------------|-----|
| Honolulu      | Hawaii-Aleutian  | UTC-10     | No  |
| Anchorage     | Alaska           | UTC-9      | Yes |
| San Francisco | Pacific          | UTC-8      | Yes |
| Denver        | Mountain         | UTC-7      | Yes |
| Minneapolis   | Central          | UTC-6      | Yes |
| New York      | Eastern          | UTC-5      | Yes |

## Technical Highlights

- `TimeZoneRecord` frozen dataclass stores all city metadata immutably
- `Region` enum drives classification logic independently of display
- `TimeZoneLookupEngine` logs every query and tracks session activity
- `ResultRowFactory` builds all output rows from a shared template
- Rendering and lookup logic fully separated for clean architecture

## Tech Stack

Python 3 | Tkinter | dataclasses | enums | functools
