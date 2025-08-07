from datetime import datetime, timedelta

from ics import Calendar, Event
import pytz

path = "\\\\turnhoutnas.dekimo.com\\DEKIMOBACKUP\\scripts\\joske\\"

employees = [ x.strip().upper() for x in open(path + "employees.txt").read().strip().split("\n")]
next_joske = open(path + "next_joske.txt").read().strip().upper()

current_week_number = datetime.now().isocalendar()[1]
current_year = datetime.now().year


next_joske_index = employees.index(next_joske) if next_joske in employees else -1
if next_joske_index == -1:
    print(f"Error: {next_joske} not found in employees list.")
    exit(50)

weeks_this_year = 53 if (current_year % 4 == 0 and current_year % 100 != 0) or (current_year % 400 == 0) else 52
first_in_cycle_week_number = (current_week_number - next_joske_index + 1) % weeks_this_year


print(f"First week number in cycle: {first_in_cycle_week_number}")
print(f"Current week number: {current_week_number}")
# do for this year and next year

idx = 0 

def get_monday_of_week(year, week):
    dt = datetime.fromisocalendar(year, week, 1)
    dt_utc = dt.replace(tzinfo=pytz.utc)
    # to local timezone
    local_tz = pytz.timezone('Europe/Brussels')  # Replace with your local timezone
    dt_local = dt_utc.astimezone(local_tz)
    return dt_local

weeks_next_year = 53 if (current_year % 4 == 0 and current_year % 100 != 0) or (current_year % 400 == 0) else 52

def do_filtered(employees, current_year, weeks_this_year, first_in_cycle_week_number, idx, get_monday_of_week, weeks_next_year, filter):
    print(f"Generating calendar for filter: {filter or 'all'}")	

    calendar = Calendar()
    for week in range(first_in_cycle_week_number, weeks_this_year + 1):
        joske = employees[idx % len(employees)]

        if filter == None or joske == filter:
            start = get_monday_of_week(current_year, week)
            end = start + timedelta(days=6)

            print(f"Week number: {week}, Year: {current_year}, Joske: {joske}")
            print(f"Start: {start}, End: {end}")	

            e = Event()
            e.name = f"Joske: {joske}"
            e.begin = start
            e.end = end
            calendar.events.add(e)

        idx += 1

    for week in range(1, weeks_next_year + 1):
        joske = employees[idx % len(employees)]

        if filter == None or joske == filter:
            start = get_monday_of_week(current_year + 1, week)
            end = start + timedelta(days=6)

            print(f"Week number: {week}, Year: {current_year+1}, Joske: {joske}")
            print(f"Start: {start}, End: {end}")

            e = Event()
            e.name = f"Joske: {joske}"
            e.begin = start
            e.end = end
            calendar.events.add(e)

        idx += 1

    with open(f"calendars/joske_{filter or 'all'}.ics", "w") as f:
        f.writelines(calendar)

do_filtered(employees, current_year, weeks_this_year, first_in_cycle_week_number, idx, get_monday_of_week, weeks_next_year, None)

for employee in employees:
    do_filtered(employees, current_year, weeks_this_year, first_in_cycle_week_number, idx, get_monday_of_week, weeks_next_year, employee)

