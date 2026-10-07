# Simple To-Do List Application
# Uses lists, functions, loops, conditionals, input, and try/except.

tasks = []


def show_menu():
    print("\n===== TO-DO LIST =====")
    print()
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Remove Task")
    print("4. Exit")


def add_task():
    task = input("\nEnter task: ").strip()

    if task == "":
        print("\nTask cannot be empty.")
        return

    tasks.append(task)
    print("\nTask added successfully!")


def view_tasks():
    print("\n===== YOUR TASKS =====")
    print()

    if len(tasks) == 0:
        print("You don't have any tasks yet.")
        return

    number = 1
    for task in tasks:
        print(f"{number}. {task}")
        number = number + 1


def remove_task():
    if len(tasks) == 0:
        print("\nYou don't have any tasks yet.")
        return

    view_tasks()

    try:
        choice = int(input("\nWhich task do you want to remove? "))
        task_index = choice - 1

        if task_index < 0 or task_index >= len(tasks):
            print("\nInvalid task number.")
            return

        removed_task = tasks.pop(task_index)
        print(f'\n"{removed_task}" removed successfully!')

    except ValueError:
        print("\nPlease enter a valid number.")


def main():
    while True:
        show_menu()
        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            remove_task()
        elif choice == "4":
            try:
                print("\nGoodbye! 👋")
            except UnicodeEncodeError:
                print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
