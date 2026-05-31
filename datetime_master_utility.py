"""
Datetime Master Utility (Single-File Mini Project)
Python 3.11+ | Standard Library Only

This project demonstrates all major classes in Python's datetime module:
- date
- time
- datetime
- timedelta
- tzinfo
- timezone

It includes:
- Menu-driven CLI
- Real-world use cases (world clock, scheduler, age calculator)
- Naive vs aware datetime demonstrations
- Custom tzinfo class for advanced timezone handling
- Error handling and beginner-friendly explanations
- Interview questions and practice exercises

Author: Chaitanya Dasadiya
GitHub: https://github.com/cdasadiya
LinkedIn: https://in.linkedin.com/in/chaitanya-dasadiya
"""

from __future__ import annotations

from datetime import date, time, datetime, timedelta, tzinfo, timezone
import time as time_module
import warnings
from typing import Optional


# -----------------------------
# Section 1: Helper Utilities
# -----------------------------


def section_heading(title: str) -> None:
    """Print a visual heading to keep CLI output readable."""
    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)


def sub_heading(title: str) -> None:
    """Print a sub-heading for section structure."""
    print(f"\n--- {title} ---")


def safe_input(prompt: str) -> str:
    """Centralized input wrapper to make future input handling easier."""
    return input(prompt).strip()


# ---------------------------------------------------------------
# Section 2: Advanced Concept - Custom tzinfo Implementation
# ---------------------------------------------------------------


class FixedOffsetTZ(tzinfo):
    """
    Custom timezone implementation using tzinfo.

    Why this class exists:
    - Demonstrates how tzinfo is an abstract base for timezone behavior.
    - Lets us define custom UTC offset, DST behavior, and zone name.

    Parameters:
    - offset_hours: offset from UTC (e.g., +5.5, -4)
    - name: timezone label shown in tzname()
    - observes_dst: if True, we simulate a simple DST rule
    """

    def __init__(self, offset_hours: float, name: str, observes_dst: bool = False):
        self._offset = timedelta(hours=offset_hours)
        self._name = name
        self._observes_dst = observes_dst

    def utcoffset(self, dt: Optional[datetime]) -> timedelta:
        """Return UTC offset for aware datetime objects."""
        return self._offset + self.dst(dt)

    def dst(self, dt: Optional[datetime]) -> timedelta:
        """
        Simulated DST rule:
        - DST active from March (month=3) to October (month=10), inclusive.
        - Adds +1 hour while active.

        Note: Real DST rules are region-specific and more complex.
        """
        if not self._observes_dst or dt is None:
            return timedelta(0)
        if 3 <= dt.month <= 10:
            return timedelta(hours=1)
        return timedelta(0)

    def tzname(self, dt: Optional[datetime]) -> str:
        """Return human-readable timezone name."""
        return self._name


# ----------------------------------------------------
# Section 3: Core Educational / Demo Feature Methods
# ----------------------------------------------------


def explain_datetime_classes() -> None:
    """Print theory + practical notes for each major datetime class."""
    section_heading("DATETIME MODULE MASTER GUIDE")

    knowledge = {
        "date": {
            "definition": "Represents a calendar date (year, month, day) without time.",
            "purpose": "Store birthdays, deadlines, holidays, reporting dates.",
            "syntax": "date(YYYY, MM, DD)",
            "methods": "today(), fromtimestamp(), isoformat(), weekday(), isoweekday(), ctime(), replace()",
            "example": "date.today()",
            "benefits": "Simple and less error-prone when time is irrelevant.",
            "use_cases": "Attendance date, invoice date, subscription renewal date.",
            "best_practices": "Use date when only day-level precision is needed.",
            "mistakes": "Mixing date with datetime without explicit conversion.",
        },
        "time": {
            "definition": "Represents time-of-day (hour, minute, second, microsecond, optional tz).",
            "purpose": "Store store opening times, alarm times, recurring clock times.",
            "syntax": "time(HH, MM, SS, microsecond=0, tzinfo=None)",
            "methods": "strftime(), isoformat(), replace(), utcoffset(), dst(), tzname()",
            "example": "time(9, 30)",
            "benefits": "Separates pure time from calendar date logic.",
            "use_cases": "Meeting starts at 09:00 daily, shift starts at 18:00.",
            "best_practices": "Attach timezone context when time comparisons cross regions.",
            "mistakes": "Comparing times from different timezones without normalization.",
        },
        "datetime": {
            "definition": "Represents date + time in one object (optionally timezone-aware).",
            "purpose": "Timestamps, logs, events, transaction time, scheduling.",
            "syntax": "datetime(YYYY, MM, DD, HH, MM, SS, tzinfo=None)",
            "methods": "now(), utcnow(), strftime(), strptime(), combine(), fromtimestamp(), timestamp(), astimezone(), replace(), ctime(), isoformat()",
            "example": "datetime.now(timezone.utc)",
            "benefits": "Most complete temporal object for real-world systems.",
            "use_cases": "Booking system, notifications, audit logs, API payloads.",
            "best_practices": "Store in UTC; convert to local time for display.",
            "mistakes": "Using naive datetimes in distributed applications.",
        },
        "timedelta": {
            "definition": "Represents a duration (difference between date/time points).",
            "purpose": "Add/subtract days, hours, minutes and compute intervals.",
            "syntax": "timedelta(days=0, hours=0, minutes=0, seconds=0)",
            "methods": "total_seconds()",
            "example": "timedelta(days=7)",
            "benefits": "Reliable temporal arithmetic without manual unit math.",
            "use_cases": "Trial period extension, countdown timers, SLA deadlines.",
            "best_practices": "Use total_seconds() for precise numeric calculations.",
            "mistakes": "Manually converting seconds/days and introducing rounding bugs.",
        },
        "tzinfo": {
            "definition": "Abstract base class for timezone metadata and rules.",
            "purpose": "Customize timezone behavior (offset, DST, name).",
            "syntax": "class MyTZ(tzinfo): ...",
            "methods": "utcoffset(), dst(), tzname()",
            "example": "Custom class FixedOffsetTZ(+5.5, 'IST-LIKE')",
            "benefits": "Fine-grained control when built-in timezone is insufficient.",
            "use_cases": "Legacy systems, simulation, custom enterprise rules.",
            "best_practices": "Implement utcoffset/dst/tzname consistently.",
            "mistakes": "Returning incorrect offsets or ignoring DST interactions.",
        },
        "timezone": {
            "definition": "Concrete tzinfo implementation with fixed UTC offset.",
            "purpose": "Easily create aware datetime objects using fixed offsets.",
            "syntax": "timezone(timedelta(hours=offset), name='Label')",
            "methods": "utcoffset(), tzname(), dst() via tzinfo contract",
            "example": "timezone.utc or timezone(timedelta(hours=5, minutes=30))",
            "benefits": "Simple and standard way to handle fixed-offset timezone data.",
            "use_cases": "APIs, logs, UTC workflows, offset-based display.",
            "best_practices": "Prefer timezone-aware datetimes for cross-region apps.",
            "mistakes": "Assuming fixed-offset timezone handles all DST transitions.",
        },
    }

    for class_name, info in knowledge.items():
        sub_heading(class_name.upper())
        for key, value in info.items():
            print(f"{key.title():<16}: {value}")


def demonstrate_core_methods() -> None:
    """Demonstrate key datetime/date/time methods requested in the prompt."""
    section_heading("CORE METHODS DEMO")

    local_now = datetime.now()
    aware_utc_now = datetime.now(timezone.utc)

    print(f"date.today()                         -> {date.today()}")
    print(f"datetime.now()                      -> {local_now}")
    # utcnow() is deprecated in modern Python, but shown here for educational completeness.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        legacy_utc_now = datetime.utcnow()
    print(f"datetime.utcnow() (naive UTC, legacy)-> {legacy_utc_now}")
    print(f"datetime.now(timezone.utc)          -> {aware_utc_now}")

    print(f"strftime('%Y-%m-%d %H:%M:%S')       -> {local_now.strftime('%Y-%m-%d %H:%M:%S')}")

    parsed = datetime.strptime("2026-12-31 23:59", "%Y-%m-%d %H:%M")
    print(f"strptime('2026-12-31 23:59', fmt)   -> {parsed}")

    replaced = local_now.replace(year=2030)
    print(f"replace(year=2030)                  -> {replaced}")

    combined = datetime.combine(date.today(), time(9, 30))
    print(f"combine(date.today(), time(9,30))   -> {combined}")

    ts_dt = datetime.fromtimestamp(1_700_000_000)
    print(f"fromtimestamp(1700000000)           -> {ts_dt}")
    print(f"timestamp()                         -> {local_now.timestamp()}")

    print(f"isoformat()                         -> {local_now.isoformat()}")
    print(f"weekday() [Mon=0]                   -> {date.today().weekday()}")
    print(f"isoweekday() [Mon=1]                -> {date.today().isoweekday()}")
    print(f"ctime()                             -> {local_now.ctime()}")

    india = timezone(timedelta(hours=5, minutes=30), name="IST")
    print(f"astimezone(IST)                     -> {aware_utc_now.astimezone(india)}")
    print(f"utcoffset()                         -> {aware_utc_now.utcoffset()}")
    print(f"dst()                               -> {aware_utc_now.dst()}")
    print(f"tzname()                            -> {aware_utc_now.tzname()}")


def age_calculator() -> None:
    """Calculate age using date and timedelta logic."""
    section_heading("AGE CALCULATOR")
    raw = safe_input("Enter birth date (YYYY-MM-DD): ")
    try:
        birth = datetime.strptime(raw, "%Y-%m-%d").date()
        today = date.today()
        years = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        days_lived = (today - birth).days
        print(f"You are {years} years old and have lived approximately {days_lived} days.")
    except ValueError:
        print("Invalid input. Please use format YYYY-MM-DD (example: 1998-04-15).")


def countdown_timer() -> None:
    """Countdown timer demo using timedelta + stdlib time.sleep."""
    section_heading("COUNTDOWN TIMER")
    raw = safe_input("Enter countdown in seconds (1-20 recommended): ")
    try:
        seconds = int(raw)
        if seconds <= 0:
            raise ValueError
        end_time = datetime.now() + timedelta(seconds=seconds)
        while True:
            remaining = end_time - datetime.now()
            if remaining <= timedelta(0):
                print("Time's up! Countdown completed.")
                break
            print(f"Remaining: {int(remaining.total_seconds())} seconds", end="\r")
            time_module.sleep(1)
        print()
    except ValueError:
        print("Invalid value. Please enter a positive whole number.")


def timezone_meeting_scheduler() -> None:
    """Schedule meeting across timezones; demonstrates aware datetimes and conversion."""
    section_heading("MEETING SCHEDULER ACROSS TIMEZONES")

    raw = safe_input("Enter meeting datetime in UTC (YYYY-MM-DD HH:MM): ")
    try:
        utc_meeting = datetime.strptime(raw, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
    except ValueError:
        print("Invalid datetime format. Use YYYY-MM-DD HH:MM.")
        return

    zones = {
        "New York (UTC-5)": timezone(timedelta(hours=-5), name="EST"),
        "London (UTC+0)": timezone.utc,
        "India (UTC+5:30)": timezone(timedelta(hours=5, minutes=30), name="IST"),
        "Tokyo (UTC+9)": timezone(timedelta(hours=9), name="JST"),
    }

    print(f"\nBase UTC meeting time: {utc_meeting.isoformat()}")
    for city, tz_obj in zones.items():
        local_time = utc_meeting.astimezone(tz_obj)
        print(f"{city:<22} -> {local_time.strftime('%Y-%m-%d %H:%M %Z %z')}")


def naive_vs_aware_demo() -> None:
    """Show difference between naive and aware datetime objects."""
    section_heading("NAIVE VS AWARE DATETIME")

    naive = datetime.now()  # no tzinfo
    aware = datetime.now(timezone.utc)  # tz-aware
    print(f"Naive datetime : {naive} | tzinfo={naive.tzinfo}")
    print(f"Aware datetime : {aware} | tzinfo={aware.tzinfo}")
    print("Best practice: use aware datetime in production systems.")


def custom_tzinfo_demo() -> None:
    """Demonstrate custom tzinfo with utcoffset, dst, tzname methods."""
    section_heading("CUSTOM TZINFO DEMONSTRATION")

    custom_zone = FixedOffsetTZ(offset_hours=2, name="COMPANY_EU", observes_dst=True)
    dt = datetime(2026, 6, 15, 10, 0, tzinfo=custom_zone)

    print(f"Datetime with custom tzinfo: {dt}")
    print(f"utcoffset(): {dt.utcoffset()}")
    print(f"dst(): {dt.dst()}")
    print(f"tzname(): {dt.tzname()}")
    print("Note: This DST logic is intentionally simplified for teaching.")


def utc_local_comparison() -> None:
    """Compare local time vs UTC and explain conversion."""
    section_heading("UTC VS LOCAL TIME COMPARISON")

    local = datetime.now().astimezone()  # attach system local timezone
    utc = datetime.now(timezone.utc)
    print(f"Local aware time: {local.strftime('%Y-%m-%d %H:%M:%S %Z %z')}")
    print(f"UTC aware time  : {utc.strftime('%Y-%m-%d %H:%M:%S %Z %z')}")
    print(f"Local converted to UTC: {local.astimezone(timezone.utc).isoformat()}")


def summary_and_learning_resources() -> None:
    """Final summary + interview questions + exercises + mini challenges."""
    section_heading("FINAL SUMMARY + LEARNING RESOURCES")

    print("When to use each class:")
    print("- date: Use when only calendar day matters.")
    print("- time: Use for clock times independent of date.")
    print("- datetime: Use for full timestamps/events.")
    print("- timedelta: Use for durations/arithmetic.")
    print("- tzinfo: Use to define custom timezone behavior.")
    print("- timezone: Use built-in fixed offset or UTC zones.")

    print("\nKey differences:")
    print("- date has no hours/minutes; datetime does.")
    print("- time is only time-of-day, optionally timezone-aware.")
    print("- timedelta is not a point in time; it is a duration.")
    print("- timezone is a concrete tzinfo implementation.")

    print("\nReal-world industry applications:")
    print("- Banking: transaction timestamps in UTC.")
    print("- Aviation/Travel: schedule normalization across timezones.")
    print("- HR systems: attendance and shift calculations.")
    print("- E-commerce: order lifecycle and delivery ETA windows.")

    print("\nPerformance tips:")
    print("- Reuse timezone objects rather than recreating repeatedly.")
    print("- Prefer arithmetic with timedelta over manual second math.")
    print("- Parse once with strptime, store structured values.")

    print("\nCommon mistakes to avoid:")
    print("- Mixing naive and aware datetimes in comparisons.")
    print("- Assuming UTC offset alone models real DST rules.")
    print("- Storing local time without timezone metadata.")

    print("\nInterview Questions:")
    print("1) What is the difference between naive and aware datetime objects?")
    print("2) Why is datetime.utcnow() often less preferred than datetime.now(timezone.utc)?")
    print("3) How does timedelta.total_seconds() differ from .seconds?")
    print("4) What methods must be implemented when subclassing tzinfo?")
    print("5) When should you use date instead of datetime?")

    print("\nPractice Exercises:")
    print("1) Build a birthday reminder that shows days left until next birthday.")
    print("2) Convert a user-entered local datetime to UTC and back.")
    print("3) Parse CSV date strings and compute average processing time.")

    print("\nMini Challenges:")
    print("- Challenge 1: Add persistent event storage (text file) with timezone-aware timestamps.")
    print("- Challenge 2: Implement a recurring weekly meeting planner.")
    print("- Challenge 3: Improve custom DST rules based on actual transition dates.")


def sample_input_output_block() -> None:
    """Display sample usage transcript for beginners."""
    section_heading("SAMPLE INPUT / OUTPUT")
    print("Sample: Age Calculator")
    print("> Enter birth date (YYYY-MM-DD): 2000-01-15")
    print("< You are 26 years old and have lived approximately 9625 days.\n")
    print("Sample: Meeting Scheduler")
    print("> Enter meeting datetime in UTC (YYYY-MM-DD HH:MM): 2026-08-10 14:30")
    print("< New York (UTC-5)       -> 2026-08-10 09:30 EST -0500")
    print("< India (UTC+5:30)       -> 2026-08-10 20:00 IST +0530")


# -----------------------------
# Section 4: Menu-Driven CLI
# -----------------------------


def menu() -> None:
    """Main interactive menu loop."""
    while True:
        section_heading("DATETIME MASTER UTILITY - MENU")
        print("1) Datetime class theory guide")
        print("2) Core methods demonstration")
        print("3) Age calculator")
        print("4) Countdown timer")
        print("5) Meeting scheduler across timezones")
        print("6) Naive vs aware datetime demo")
        print("7) Custom tzinfo demo")
        print("8) UTC vs local comparison")
        print("9) Sample input/output")
        print("10) Final summary + interview prep")
        print("0) Exit")

        choice = safe_input("Choose an option: ")

        if choice == "1":
            explain_datetime_classes()
        elif choice == "2":
            demonstrate_core_methods()
        elif choice == "3":
            age_calculator()
        elif choice == "4":
            countdown_timer()
        elif choice == "5":
            timezone_meeting_scheduler()
        elif choice == "6":
            naive_vs_aware_demo()
        elif choice == "7":
            custom_tzinfo_demo()
        elif choice == "8":
            utc_local_comparison()
        elif choice == "9":
            sample_input_output_block()
        elif choice == "10":
            summary_and_learning_resources()
        elif choice == "0":
            print("Goodbye! Keep practicing datetime mastery.")
            break
        else:
            print("Invalid choice. Please select a valid menu option.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    # Entry point keeps file directly runnable: python datetime_master_utility.py
    menu()
