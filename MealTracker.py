
print("this app tracks your routine.")

meals = []
calorie = []
# total_cl = 0
daily_cl_lt = int(input("whats your daily limit of calorie : "))
n = int(input("enter number of meals : "))

for i in range(1,n+1):
    mn = input("enter meal name : ")
    cl = int(input("enter calorie : "))
    # total_cl += cl
    meals.append(mn)
    calorie.append(cl)
    
sum_cl = sum(calorie)
average_cl = sum_cl/n

if daily_cl_lt > sum_cl :
    print("your calorie intake is low than your limit.")
elif daily_cl_lt < sum_cl :
    print("Your daily limit of calorie is crossed now !")
else:
    print("calorie intake is equal right now")

print("\nMeal Name\tCalories\n--------------------------------")

for i in meals:
    for j in calorie:
        print(i,"\t",j)

print(f"total:\t{sum_cl}\nAverage:\t{average_cl}")
