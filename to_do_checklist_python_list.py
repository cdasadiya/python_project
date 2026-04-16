# -------------------------------
# To-Do List Application (Lists)
# -------------------------------

# Initial checklist (demo data)
checklist = [
    "Wake up early",
    "Workout",
    "Read 20 pages",
    "Complete Python project",
    "Attend meetings",
    "Plan next day"
]

# Result lists
completed_tasks = []
incomplete_tasks = []

def display_tasks(tasks, title):
    print(f"\n{title}")
    print("-" * len(title))
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")
    if not tasks:
        print("No tasks")

def mark_tasks():
    if not checklist:
        print("\nNo tasks available to mark.")
        return

    # Iterate over a copy to safely modify original list
    for task in checklist[:]:
        while True:
            status = input(f"\nDid you complete '{task}'? (y/n): ").strip().lower()

            if status == 'y':
                completed_tasks.append(task)
                checklist.remove(task)   # remove from checklist
                break
            elif status == 'n':
                incomplete_tasks.append(task)
                checklist.remove(task)
                break
            else:
                print("Invalid input. Enter 'y' or 'n'.")

def add_task():
    task = input("\nEnter new task: ").strip()
    if task and task.lower() not in {item.lower() for item in checklist}:
        checklist.append(task)
        print("Task added.")
    else:
        print("Invalid or duplicate task.")

def remove_task():
    if not checklist:
        print("\nChecklist is empty. Nothing to remove.")
        return

    display_tasks(checklist, "Current Checklist")
    try:
        idx = int(input("Enter task number to remove: "))
        if idx < 1 or idx > len(checklist):
            raise IndexError
        removed = checklist.pop(idx - 1)   # pop used
        print(f"Removed: {removed}")
    except (ValueError, IndexError):
        print("Invalid selection.")

def advanced_list_ops():
    print("\n--- Advanced List Operations Demo ---")

    # Extend example
    bonus_tasks = ["Meditation", "Journaling"]
    checklist.extend(bonus_tasks)

    # Insert example
    checklist.insert(0, "Check emails")

    # Sort example
    checklist.sort()

    # Reverse example
    checklist.reverse()

    # Count example
    print("Count of 'Workout':", checklist.count("Workout"))

    # Index example
    if "Workout" in checklist:
        print("Index of 'Workout':", checklist.index("Workout"))

def summary():
    display_tasks(completed_tasks, "Completed Tasks")
    display_tasks(incomplete_tasks, "Incomplete Tasks")

def menu():
    while True:
        print("\n====== TO-DO MENU ======")
        print("1. View Checklist")
        print("2. Add Task")
        print("3. Remove Task")
        print("4. Mark Tasks (Complete/Incomplete)")
        print("5. Advanced List Operations Demo")
        print("6. View Summary")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            display_tasks(checklist, "Checklist")
        elif choice == '2':
            add_task()
        elif choice == '3':
            remove_task()
        elif choice == '4':
            mark_tasks()
        elif choice == '5':
            advanced_list_ops()
        elif choice == '6':
            summary()
        elif choice == '7':
            print("Exiting application.")
            break
        else:
            print("Invalid choice.")

# Run the app
if __name__ == "__main__":
    menu()
