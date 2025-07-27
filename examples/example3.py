employees = [
    ["John", 42, 15],
    ["Ana", -5, 17],  
    ["Lee", 37, 12]
]

for emp in employees:
    if emp[1] > 40:
        total = 40*emp[2] + (emp[1]-40)*emp[2]*1.5
    else:
        total = emp[1]*emp[2]
    print("Pay " + emp[0] + " $" + str(total))  # Lol , the boss is idiot, he forgot to add bonus!


for emp in employees:
    bonus = 100
    if emp[1] > 40:
        total_with_bonus = 40*emp[2] + (emp[1]-40)*emp[2]*1.5 + bonus
    else:
        total_with_bonus = emp[1]*emp[2] + bonus
    print("Bonus pay " + emp[0] + " $" + str(total_with_bonus))