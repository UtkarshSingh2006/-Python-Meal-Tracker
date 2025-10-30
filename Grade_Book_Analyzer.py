print("=== GradeBook Analyzer ===")

n = int(input("Enter number of students: "))
names = []
marks = []

for i in range(n):
    name = input("Enter name of student: ")
    mark = float(input("Enter marks of " + name + ": "))
    names.append(name)
    marks.append(mark)

total = sum(marks)
avg = total / n
marks.sort()
if n % 2 == 0:
    median = (marks[n//2 - 1] + marks[n//2]) / 2
else:
    median = marks[n//2]

max_mark = max(marks)
min_mark = min(marks)

grades = []
for m in marks:
    if m >= 90:
        grades.append("A")
    elif m >= 80:
        grades.append("B")
    elif m >= 70:
        grades.append("C")
    elif m >= 60:
        grades.append("D")
    else:
        grades.append("F")

print("\n--- Result ---")
for i in range(n):
    print(names[i], "-", marks[i], "-", grades[i])

print("\nTotal Students:", n)
print("Average Marks:", avg)
print("Median Marks:", median)
print("Highest Marks:", max_mark)
print("Lowest Marks:", min_mark)

pass_students = 0
fail_students = 0
for m in marks:
    if m >= 40:
        pass_students += 1
    else:
        fail_students += 1

print("Passed Students:", pass_students)
print("Failed Students:", fail_students)
