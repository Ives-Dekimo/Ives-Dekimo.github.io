from datetime import datetime, timedelta

from ics import Calendar, Event

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

calendar = Calendar()

def get_monday_of_week(year, week):
    return datetime.fromisocalendar(year, week, 1)

weeks_next_year = 53 if (current_year % 4 == 0 and current_year % 100 != 0) or (current_year % 400 == 0) else 52

def do_filtered(employees, current_year, weeks_this_year, first_in_cycle_week_number, idx, calendar, get_monday_of_week, weeks_next_year, filter):
    for week in range(first_in_cycle_week_number, weeks_this_year + 1):
        joske = employees[idx % len(employees)]

        start = get_monday_of_week(current_year, week)
        end = start + timedelta(days=6)

        print(f"Week number: {week}, Year: {current_year}, Joske: {joske}")
        print(f"Start: {start}, End: {end}")	

        if filter or joske == filter:
            e = Event()
            e.name = f"Joske: {joske}"
            e.begin = start
            e.end = end
            calendar.events.add(e)

        idx += 1

    for week in range(1, weeks_next_year + 1):
        joske = employees[idx % len(employees)]

        start = get_monday_of_week(current_year + 1, week)
        end = start + timedelta(days=6)

        print(f"Week number: {week}, Year: {current_year+1}, Joske: {joske}")
        print(f"Start: {start}, End: {end}")

        if filter or joske == filter:
            e = Event()
            e.name = f"Joske: {joske}"
            e.begin = start
            e.end = end
            calendar.events.add(e)

        idx += 1

    with open(f"calendars/joske_{filter or 'all'}.ics", "w") as f:
        f.writelines(calendar)

do_filtered(employees, current_year, weeks_this_year, first_in_cycle_week_number, idx, calendar, get_monday_of_week, weeks_next_year, None)

for employee in employees:
    do_filtered(employees, current_year, weeks_this_year, first_in_cycle_week_number, idx, calendar, get_monday_of_week, weeks_next_year, employee)

