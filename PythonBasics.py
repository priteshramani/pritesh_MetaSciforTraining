# 1 Write a Python program that prints "Hello, World!" to the console.

print("Hello,World!")

# 2 Declare a variable x with the value 10. Assign another variable y with the string "Python". Print both values along with their types

x = 10
y = "Python"
print(type(x),x)
print(type(y),y)

# 3 Create a list of five numbers. Write a Python program to find the sum and average of all numbers in the list

list = [10,12,13,16,19]
print(sum(list))

print(sum(list)/len(list))

# 4 Write a Python program that takes two numbers as input and prints their sum, difference, product, and quotient.

a=int(input("Enter Num 1:- "))
b=int(input("Enter Num 2:- "))

print("Sum",a+b)
print("Difference",a-b)
print("Product",a*b)
print("Quotient",a/b)

# 5 Given name = "Alice" and age = 25, use different string formatting techniques (%, .format(), and f-strings) to print "Alice is 25 years old."

name = "Alice"
age = 25
print(f"{name} is {age} years old")

# 6 Write a Python program that takes a string as input and:
    # ⦁ Converts it to uppercase and lowercase.

demo = str(input("Input Your name :- "))

print("In Uppercase",demo.upper())
print("In Lowercase",demo.lower())

   # ⦁ Counts the number of vowels in the string.

text = str(input("Count vowels function :- "))
vowels="aeiouAEIOU"
count=0
for char in text:
    if char in vowels:
        count+=1
print("Vowels In Function is :-",count)  

   # ⦁ Reverses the string.

text = str(input("enter the string :-"))

print(text[::-1])

# 7 Write a Python program that takes a number as input and checks whether it is even or odd.

num = int(input("enter a number :-"))
if num%2 == 0:
    print("number is Even:-",num)
else:
    print("number is Odd :-",num)    


# 8 Write a Python program that prints all prime numbers between 1 and 50.

def isPrime(x):
        for i in range(2,x):
            for j in range(2,x):
                 if (x % i) == 0:
                      return False       
            if i == j :
                 return True
for x in range(1,51):
    if isPrime(x):
        print(x)



# 9 Write a function factorial(n) that returns the factorial of a given number n.

n = int(input("Enter a num:-"))
def factorial(n):
    if n < 0:
        return
    elif n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        print(result)
factorial(n)    
    


# 10 Create a Car class with attributes brand, model, and year. Define a method display_info() that prints car details. Instantiate an object and call the method.
   
class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def display_info(self):
        print(f"Car Brand: {self.brand}")
        print(f"Car Model: {self.model}")
        print(f"Car Year: {self.year}")

my_car = Car("Toyota", "Fortuner", 2015)
my_car.display_info()



# 11 Create a dictionary containing three students' names as keys and their scores as values. Write a program to : Print all keys and values. Find the highest score.

students_scores = {
    "Alice": 85,
    "Bob": 92,
    "Charlie": 78
}

print("Students and their scores:")
for student, score in students_scores.items():
    print(f"{student}: {score}")

highest_score = max(students_scores.values())
highest= [student for student, score in students_scores.items() if score == highest_score]

print(f"\nHighest Score:", highest_score)

# 12 Write a Python program that imports the math module and calculates the square root and factorial of a given number.

import math

num=int(input("Enter number:-"))
sqrt = math.sqrt(num)
if num < 0:
        print("Factorial is not defined for negative numbers.")
else:
       fact = math.factorial(num)

print(f"Square root of {num}: {sqrt}")
print(f"Factorial of {num}: {fact}")

# 13 Write a Python program that asks the user for their name and age, then prints a message saying "Hello [name], you are [age] years old!".

name = input("What is your name? ")
age = input("How old are you? ")
print(f"Hello {name}, you are {age} years old!")



