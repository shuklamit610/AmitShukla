import java.util.*;

public class ScheduleManager {
    private static final String[] DAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"};
    private static final String[] SHIFTS = {"Morning", "Afternoon", "Evening"};
    private static final int MIN_STAFF = 2;
    private static final int MAX_WORK_DAYS = 5;

    public static void main(String[] args) {
        // This is the first line that will appear in your terminal
        System.out.println("Testing...");
        System.out.println(">>> Starting Employee Scheduler Logic...");
        
        List<String> employees = Arrays.asList("Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi");
        Map<String, Integer> workCounts = new HashMap<>();
        for (String emp : employees) workCounts.put(emp, 0);

        Map<String, Map<String, List<String>>> schedule = new LinkedHashMap<>();
        Random rand = new Random();

        for (String day : DAYS) {
            System.out.println("-> Currently generating schedule for: " + day);
            schedule.put(day, new HashMap<>());
            for (String shift : SHIFTS) {
                schedule.get(day).put(shift, new ArrayList<>());
            }

            // Phase 1: Preference Assignment
            for (String emp : employees) {
                if (workCounts.get(emp) < MAX_WORK_DAYS) {
                    String pref = SHIFTS[rand.nextInt(SHIFTS.length)];
                    schedule.get(day).get(pref).add(emp);
                    workCounts.put(emp, workCounts.get(emp) + 1);
                }
            }

            // Phase 2: Minimum Staffing Check
            for (String shift : SHIFTS) {
                List<String> assigned = schedule.get(day).get(shift);
                System.out.println("   Checking " + shift + " (Current Staff: " + assigned.size() + ")");
                
                while (assigned.size() < MIN_STAFF) {
                    String candidate = null;
                    for (String emp : employees) {
                        if (workCounts.get(emp) < MAX_WORK_DAYS && !assigned.contains(emp)) {
                            candidate = emp;
                            break;
                        }
                    }

                    if (candidate != null) {
                        assigned.add(candidate);
                        workCounts.put(candidate, workCounts.get(candidate) + 1);
                        System.out.println("      + Added " + candidate + " to fill gap.");
                    } else {
                        System.out.println("      ! Critical: No more eligible staff for this shift.");
                        break; 
                    }
                }
            }
        }

        System.out.println("\n>>> Logic Complete. Printing Final Table...");
        System.out.println("====================================================");
        for (String day : DAYS) {
            System.out.println(day.toUpperCase());
            schedule.get(day).forEach((shift, emps) -> {
                System.out.printf("%-10s : %s\n", shift, emps);
            });
            System.out.println("----------------------------------------------------");
        }
    }
}