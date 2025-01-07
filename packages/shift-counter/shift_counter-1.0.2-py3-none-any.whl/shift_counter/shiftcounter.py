from enum import Enum
import pandas as pd
from datetime import datetime, timedelta


class ShiftType(Enum):
    """Enumeration of possible shift types in the attendance plan."""
    NORMAL = 1  # Regular working shift
    VD = 2  # Variable day shift
    RED = 3  # Red shift (special category)
    VACATION = 4  # Vacation/leave
    OTHER = 5  # Other types of shifts/absences


class ShiftTypeDecider:
    """Determines the type of shift based on shift attributes from JSON data."""

    @staticmethod
    def get_type(shift: dict) -> ShiftType:
        """
        Analyze shift data and return corresponding ShiftType.

        Args:
            shift: Dictionary containing shift attributes ('test', 'name', 'color', 'reason')

        Returns:
            ShiftType: Classified shift type based on attributes
        """
        if shift.get("test") == 5:
            return ShiftType.OTHER
        elif shift.get("name") == "VD":
            return ShiftType.VD
        elif shift.get("color") == "red":
            return ShiftType.RED
        elif shift.get("reason") == "vacation-2021":
            return ShiftType.VACATION
        return ShiftType.NORMAL


class ShiftCounter:
    """
    Processes attendance data into a DataFrame with 30-minute time segments.
    Calculates hours for different shift types (normal, VD, red, vacation).
    """

    def __init__(self):
        """Initialize ShiftCounter with empty DataFrame containing required columns and types."""
        self.extraction_date = pd.Timestamp.now(tz='UTC').tz_localize(None).floor('s')
        self.df = pd.DataFrame(columns=[
            'department_id',  # Department/unit identifier
            'detail_level',  # Granularity of data (hour)
            'time_segment',  # Start time of 30-minute segment
            'extraction_date',  # When the data was processed
            'hours_normal',  # Regular shift hours
            'hours_vd',  # Variable day hours
            'hours_red',  # Red shift hours
            'hours_vacation'  # Vacation/leave hours
        ])

        # Set proper types for columns
        self.df['department_id'] = self.df['department_id'].astype(int)
        self.df['detail_level'] = self.df['detail_level'].astype(str)
        self.df['time_segment'] = pd.to_datetime(self.df['time_segment']).dt.floor('s')
        self.df['extraction_date'] = pd.to_datetime(self.df['extraction_date']).dt.floor('s')
        self.df['hours_normal'] = self.df['hours_normal'].astype(float)
        self.df['hours_vd'] = self.df['hours_vd'].astype(float)
        self.df['hours_red'] = self.df['hours_red'].astype(float)
        self.df['hours_vacation'] = self.df['hours_vacation'].astype(float)

    def _generate_time_segments(self, start_time: datetime, end_time: datetime) -> list:
        """
        Generate list of time segments between start and end time in 30-minute intervals.

        Args:
            start_time: Start datetime
            end_time: End datetime

        Returns:
            list: List of datetime objects representing segment start times
        """
        segments = []
        current_time = start_time

        while current_time < end_time:
            segments.append(current_time)
            current_time += timedelta(minutes=30)

        return segments

    def add_shift(self, from_time: str, to_time: str, unit_id: int, shift_type: ShiftType):
        """
        Add a shift to the DataFrame, splitting it into 30-minute segments.

        Args:
            from_time: Start time in ISO format with timezone (e.g., '2025-01-08T08:00:00+01:00')
            to_time: End time in ISO format with timezone (e.g., '2025-01-08T14:00:00+01:00')
            unit_id: Department/unit identifier
            shift_type: Type of shift (ShiftType enum value)
        """
        # Convert string timestamps to datetime objects, normalize to UTC
        start_time = pd.to_datetime(from_time).tz_convert('UTC').tz_localize(None).floor('s')
        end_time = pd.to_datetime(to_time).tz_convert('UTC').tz_localize(None).floor('s')

        time_segments = self._generate_time_segments(start_time, end_time)

        # Map shift types to corresponding DataFrame columns
        hours_columns = {
            ShiftType.VD: 'hours_vd',
            ShiftType.RED: 'hours_red',
            ShiftType.VACATION: 'hours_vacation',
            ShiftType.NORMAL: 'hours_normal',
            ShiftType.OTHER: 'hours_other'
        }
        hours_column = hours_columns.get(shift_type, 'hours_normal')

        # Process each 30-minute segment
        for segment_start in time_segments:
            mask = (
                    (self.df['department_id'] == unit_id) &
                    (self.df['time_segment'] == segment_start)
            )

            if mask.any():
                # Update existing time segment
                self.df.loc[mask, hours_column] += 0.5
                self.df.loc[mask, 'extraction_date'] = self.extraction_date
            else:
                # Create new time segment
                new_row = {
                    'department_id': unit_id,
                    'detail_level': 'hour',
                    'time_segment': segment_start,
                    'extraction_date': self.extraction_date,
                    'hours_normal': 0.0,
                    'hours_vd': 0.0,
                    'hours_red': 0.0,
                    'hours_vacation': 0.0
                }
                new_row[hours_column] = 0.5
                self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)

    def get_dataframe(self) -> pd.DataFrame:
        """
        Return the current state of the shifts DataFrame.

        Returns:
            pd.DataFrame: Copy of the internal DataFrame with all shifts
        """
        return self.df.copy()

    def count_attendance_plan(self, plan: dict):
        """
        Process attendance plan JSON data and add all shifts and absences.

        Args:
            plan: Dictionary containing attendance plan data with structure:
                {
                    "data": [
                        {
                            "shifts": [
                                {
                                    "date_time_from": str,
                                    "date_time_to": str,
                                    ...shift attributes...
                                }
                            ],
                            "absences": [
                                {
                                    "date_time_from": str,
                                    "date_time_to": str
                                }
                            ]
                        }
                    ]
                }
        """
        data = plan["data"]

        for employee in data:
            # Process regular shifts
            for shift in employee["shifts"]:
                self.add_shift(
                    shift["date_time_from"],
                    shift["date_time_to"],
                    120,  # Example department_id
                    ShiftTypeDecider.get_type(shift)
                )

            # Process absences (always counted as vacation)
            for absence in employee["absences"]:
                self.add_shift(
                    absence["date_time_from"],
                    absence["date_time_to"],
                    120,  # Example department_id
                    ShiftType.VACATION
                )


# Example usage
if __name__ == "__main__":
    # Initialize counter
    counter = ShiftCounter()

    # Example attendance plan data
    example_plan = {
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

    # Process the plan
    counter.count_attendance_plan(example_plan)

    # Get results
    result_df = counter.get_dataframe()
    print(result_df)

