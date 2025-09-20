import random

# Computer picks a secret number between 1 and 10
secret_number = random.randint(1, 10)

print("🎮 Welcome to the Guessing Game! 🎮")
print("I'm thinking of a number between 1 and 10")

# Give player 3 tries
for tries in range(3):
    guess = int(input("What's your guess? "))
    
    if guess == secret_number:
        print("🎉 You won! Great job!")
        break
    elif guess < secret_number:
        print("Too low! Try higher")
    else:
        print("Too high! Try lower")
else:
    print(f"Game over! The number was {secret_number}")
