a = ["start","stop","stop","start","start","stop","stop","start","start","stop","stop","start","start","stop","stop","start"]

x = 1
c = 0
b = [int(input()) for i in range(689)]


for i in range(689):
  if b[i] != b[i+1]:
    c += 1

  print(a[c])