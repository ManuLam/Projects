a = [input() for _ in range(611)]
a = list(filter(None, a))

d,i,m,c = 0,0,0,0
d1,i1,m1,c1 = 0,0,0,0
d2,i2,m2,c2 = 0,0,0,0

for x in range(len(a)-1):
  if(a[x][0] == 'D'): c += 1
  if a[x][0] == 'D' and a[x+1][0] == 'D':
    d += 1
  if a[x][0] == 'D' and a[x+1][0] == 'I':
    i += 1
  if a[x][0] == 'D' and a[x+1][0] == 'M':
    m += 1

print("%.2f, %.2f, %.2f" % (d/c, i/c, m/c))
print()

for x in range(len(a)-1):
  if(a[x][0] == 'I'): c1 += 1
  if a[x][0] == 'I' and a[x+1][0] == 'D':
    d1 += 1
  if a[x][0] == 'I' and a[x+1][0] == 'I':
    i1 += 1
  if a[x][0] == 'I' and a[x+1][0] == 'M':
    m1 += 1

print("%.2f, %.2f, %.2f" % (d1/c1, i1/c1, m1/c1))
print()

for x in range(len(a)-1):
  if(a[x][0] == 'M'): c2 += 1
  if a[x][0] == 'M' and a[x+1][0] == 'D':
    d2 += 1
  if a[x][0] == 'M' and a[x+1][0] == 'I':
    i2 += 1
  if a[x][0] == 'M' and a[x+1][0] == 'M':
    m2 += 1

print("%.2f, %.2f, %.2f" % (d2/c2, i2/c2, m2/c2))