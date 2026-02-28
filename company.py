import random

# Constants
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SHIFTS = ["Morning", "Afternoon", "Evening"]
MIN_PER_SHIFT = 2
MAX_DAYS = 5

def generate_schedule(employees, preferences):
    schedule = {day: {shift: [] for shift in SHIFTS} for day in DAYS}
    work_counts = {name: 0 for name in employees}

    for day in DAYS:
        # 1. Assign based on preferences
        for name in employees:
            pref = preferences[name][day]
            if work_counts[name] < MAX_DAYS and len(schedule[day][pref]) < 5: # Limit per shift capacity
                schedule[day][pref].append(name)
                work_counts[name] += 1
            elif work_counts[name] < MAX_DAYS:
                # Conflict Resolution: Try another shift same day
                for alt_shift in SHIFTS:
                    if len(schedule[day][alt_shift]) < 5:
                        schedule[day][alt_shift].append(name)
                        work_counts[name] += 1
                        break

        # 2. Minimum Staffing Enforcement
        for shift in SHIFTS:
            while len(schedule[day][shift]) < MIN_PER_SHIFT:
                eligible = [n for n in employees if work_counts[n] < MAX_DAYS and n not in schedule[day][shift]]
                if not eligible: break
                chosen = random.choice(eligible)
                schedule[day][shift].append(chosen)
                work_counts[chosen] += 1
    
    return schedule

# Sample Data Execution
employees_list = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"]
# Simplified preference mock
prefs = {name: {day: random.choice(SHIFTS) for day in DAYS} for name in employees_list}

final_schedule = generate_schedule(employees_list, prefs)

# Output
for day, shifts in final_schedule.items():
    print(f"--- {day} ---")
    for shift, names in shifts.items():
        print(f"{shift}: {', '.join(names)}")