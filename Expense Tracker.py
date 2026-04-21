budget = float(input("Enter your daily budget: $"))

total = 0.0

while True:
    expense = input("\nEnter expense amount (or type 'q' to quit): ")
    
    if expense.lower() == "q":
        break

    if expense.replace('.', '', 1).isdigit():
        amount = float(expense)

        total += amount

        print("Total spent: $", format(total, ".2f"))
        
        print("Remaining budget: $", format(budget - total, ".2f"))

        if total > budget:
            print("You are over budget!")

    else:
        print("Invalid input, try again.")

print("\nFinal total spent: $", format(total, ".2f"))
print("Goodbye!")
