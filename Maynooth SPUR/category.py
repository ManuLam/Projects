a = []
for i in range(672):
  x = input()
  if(x != ""):
    if(x[0] == "D"):  a.append(x[0])
    elif(x[0] == "I"): a.append(x[0])
    elif(x[0] == "M"): a.append(x[0])
    else: a.append("")
  else: a.append("")

print('\n'.join(a))
