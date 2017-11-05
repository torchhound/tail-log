import random

file = open("log.txt", "a+")
while True:
    file.write(str(random.randint(0, 100)) + "\n")
