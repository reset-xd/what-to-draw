from csv import writer, reader

f = open("users.csv", "r", newline="")
read = reader(f, delimiter=";")
print(list(read))