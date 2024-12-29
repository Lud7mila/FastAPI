# Задача 1 (просто) "Арифметика":
print("1st program")
print("9 ** 0.5 * 5 = ", 9 ** 0.5 * 5)

# Задача 2 (просто) "Логика":
print("\n2nd program")
print("9.99 > 9.98 and 1000 != 1000.1 - ", 9.99 > 9.98 and 1000 != 1000.1)

# Задача 3 (средне) "Школьная загадка":
print("\n3rd program")
number1 = 2 * 2 + 2
number2 = 2 * (2 + 2)
print(f"number1 = {number1}\nnumber2 = {number2}\nnumber1 == number2 - {number1 == number2}")

# Задача 4 (сложно) "Первый после точки":
print("\n4th program")
string = '123.456'
int_number = int(float(string) * 10) % 10
print(f"Первая цифра в строке {string} после запятой - {int_number}")