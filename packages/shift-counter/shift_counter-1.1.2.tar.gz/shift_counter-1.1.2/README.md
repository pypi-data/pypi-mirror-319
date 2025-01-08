# Shift Counter

A Python library for processing attendance plan data into time-segmented DataFrames. This library takes JSON attendance data and converts it into a structured pandas DataFrame with 30-minute time segments, making it easy to analyze working hours by different shift types.

## Installation

```bash
pip install shift-counter
```

## Features

- Processes attendance data into 30-minute segments
- Classifies shifts into different types (Normal, VD, Red, Vacation)
- Handles timezone-aware timestamps
- Aggregates overlapping shifts
- Compatible with Tria HR API output format

## Usage

### Basic Usage

```python
from shift_counter import ShiftCounter, ShiftType

# Initialize counter
counter = ShiftCounter()

# Add individual shifts
counter.add_shift(
    from_time="2025-01-08T08:00:00+01:00",
    to_time="2025-01-08T16:00:00+01:00",
    unit_id=120,
    shift_type=ShiftType.NORMAL
)

# Get resulting DataFrame
df = counter.get_dataframe()
```

### Processing Attendance Plan

```python
# Process complete attendance plan (e.g., from Tria HR API)
attendance_plan = {
    "data": [{
        "shifts": [{
            "date_time_from": "2025-01-08T08:00:00+01:00",
            "date_time_to": "2025-01-08T16:00:00+01:00",
            "name": "VD"
        }],
        "absences": [{
            "date_time_from": "2025-01-09T08:00:00+01:00",
            "date_time_to": "2025-01-09T16:00:00+01:00"
        }]
    }]
}

counter = ShiftCounter()
counter.count_attendance_plan(attendance_plan)
```

### Output Format

The resulting DataFrame contains the following columns:

- `department_id`: Integer identifier for the organizational unit
- `detail_level`: Granularity of the data (always 'hour')
- `time_segment`: Start time of the 30-minute segment
- `extraction_date`: When the data was processed
- `hours_normal`: Regular shift hours
- `hours_vd`: Variable day shift hours
- `hours_red`: Red shift hours
- `hours_vacation`: Vacation/leave hours

Each row represents a 30-minute segment, with hours columns showing 0.5 for each shift type present in that segment.

## Integration with Tria HR API

While this library can be used independently, it's designed to work seamlessly with data from the Tria HR API:

```python
from triahr import TriaHRAPI
from shift_counter import ShiftCounter

# Get attendance data
api = TriaHRAPI.from_config()
attendance = api.attendance_plan(
    date_from="2025-01-01",
    date_to="2025-01-31",
    unit_id=120
)

# Process into DataFrame
counter = ShiftCounter()
counter.count_attendance_plan(attendance)
df = counter.get_dataframe()
```

## Error Handling

The library automatically handles:
- Timezone conversions
- Overlapping shifts
- Missing or invalid shift types
- Data type consistency

## Requirements

- Python ≥ 3.7
- pandas ≥ 1.0.0

## License

MIT License