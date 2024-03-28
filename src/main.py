with open("log.txt", "a") as file:
  for i in range(70):
    text = str(i) + '\n'
    file.write(text)