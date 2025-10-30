print("=== Daily Calorie Tracker ===")

n = int(input("How many meals did you eat today? "))
total = 0
calories = []

for i in range(n):
    meal = input("Enter meal name: ")
    cal = float(input("Enter calories for " + meal + ": "))
    calories.append(cal)
    total = total + cal

avg = total / n
limit = float(input("Enter your daily calorie limit: "))

print("\n--- Calorie Report ---")
for i in range(n):
    print("Meal", i+1, ":", calories[i], "calories")

print("Total Calories =", total)
print("Average Calories =", avg)

if total > limit:
    print("You have exceeded your daily limit!")
else:
    print("You are within your daily limit.")

save = input("Do you want to save this report? (y/n): ")
if save.lower() == 'y':
    file = open("calorie_report.txt", "w")
    file.write("Calorie Report\n")
    file.write("Total Calories: " + str(total) + "\n")
    file.write("Average Calories: " + str(avg) + "\n")
    file.write("Daily Limit: " + str(limit) + "\n")
    if total > limit:
        file.write("Status: Limit Exceeded\n")
    else:
        file.write("Status: Within Limit\n")
    file.close()
    print("Report saved successfully!")
else:
    print("Report not saved.")
