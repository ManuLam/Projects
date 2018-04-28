def doIt(ar):
  r,c = 0,0
  
  for i in range(9):
    for j in range(9):
      if(ar[i][j] == 0): 
        r,c = i,j
        break
    
  if(filled(ar)): return True  #until solved
      
  for k in range(1,10):
    if(check(ar, r, c, k)): 
      ar[r][c] = k
      if(doIt(ar)): return True
      ar[r][c] = 0
      
  return False
  
def check(ar, r, c, k):
  for p in range(9):
    if(ar[r][p] == k): return False
    if(ar[p][c] == k): return False
    
    for n in range(3):
      for m in range(3):
        if(ar[n+(r-(r%3))][m+(c-(c%3))] == k): return False
  return True
        
def filled(ar):
  for i in range(9):
    for j in range(9):
      if(ar[i][j] == 0): return False
  return True
  
def fin(array):
  if(doIt(array) == True): print("\n", array)
  else: print("Unsolvable")


array = [[0, 0, 0, 0, 0, 7, 0, 1, 6], [0, 0, 0, 0, 6, 0, 7, 9, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [9, 0, 0, 6, 0, 1, 0, 5, 0], [0, 0, 3, 0, 0, 0, 8, 2, 1], [0, 0, 4, 0, 8, 6, 0, 0, 0], [0, 1, 5, 9, 2, 0, 0, 0, 0], [0, 0, 9, 0, 4, 0, 0, 0, 0]]

print(array)
fin(array)