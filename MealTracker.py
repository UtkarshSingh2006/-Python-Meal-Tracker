# Project: Daily Calorie Tracker CLI - Programming for Problem Solving using Python
import datetime
import os

def get_float(prompt):
    while True:
        try:
            val = input(prompt).strip()
            num = float(val)
            if num < 0:
                print("Please enter a non-negative number.")
                continue
            return num
        except ValueError:
            print("Please enter a valid number (e.g., 350 or 350.5).")

def main():
    print("=== Daily Calorie Tracker ===")
    print("Log your meals, compute total & average calories, compare with a daily limit, and optionally save the report.\n")

    while True:
        try:
            n = int(input("How many meals do you want to enter? ").strip())
            if n <= 0:
                print("Enter a positive integer.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer (e.g., 3).")

    meals = []
    calories = []

    for i in range(1, n+1):
        meal_name = input(f"Meal {i} name: ").strip()
        if meal_name == "":
            meal_name = f"Meal_{i}"
        cal = get_float(f"Calories for '{meal_name}': ")
        meals.append(meal_name)
        calories.append(cal)

    total = sum(calories)
    average = total / len(calories) if calories else 0.0

    daily_limit = get_float("Enter your daily calorie limit: ")

    print("\n--- Summary Report ---")
    print(f"{'Meal Name':20s}{'Calories':>10s}")
    print("-" * 32)
    for m, c in zip(meals, calories):
        print(f"{m:20s}{c:10.2f}")
    print("\n" + "-" * 32)
    print(f"{'Total:':20s}{total:10.2f}")
    print(f"{'Average per meal:':20s}{average:10.2f}")
    status = "EXCEEDED" if total > daily_limit else "Within limit"
    print(f"Daily limit: {daily_limit:.2f}   Status: {status}")

    save = input("\nDo you want to save this report to a text file? (y/n): ").strip().lower()
    if save.startswith('y'):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"calorie_log_{timestamp}.txt"
        with open(filename, "w") as f:
            f.write("Daily Calorie Tracker Session\n")
            f.write(f"Date: {datetime.datetime.now().isoformat()}\n\n")
            f.write(f"{'Meal Name':20s}{'Calories':>10s}\n")
            f.write("-" * 32 + "\n")
            for m, c in zip(meals, calories):
                f.write(f"{m:20s}{c:10.2f}\n")
            f.write("\n" + "-" * 32 + "\n")
            f.write(f"{'Total:':20s}{total:10.2f}\n")
            f.write(f"{'Average per meal:':20s}{average:10.2f}\n")
            f.write(f"Daily limit: {daily_limit:.2f}   Status: {status}\n")
        print(f"Saved report as: {os.path.abspath(filename)}")
    else:
        print("Report not saved.")
    print("\nThank you for using Daily Calorie Tracker!")

if __name__ == "__main__":
    main()
