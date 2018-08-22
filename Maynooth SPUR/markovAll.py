a = [input() for _ in range(611)]
a = list(filter(None, a))

d,i,m,c = 0,0,0,0

for x in range(len(a)-1):
  if(a[x][0] == 'D'): c += 1
  if a[x][0] == 'D' and a[x+1][0] == 'D':
    d += 1
  if a[x][0] == 'D' and a[x+1][0] == 'I':
    i += 1
  if a[x][0] == 'D' and a[x+1][0] == 'M':
    m += 1

print(d/c)
print(i/c)
print(m/c)
print()

action = [
'D_Agent',
'D_Obj',
'D_Menu2D',
'D_User',

'I_Agent',
'I_Obj',
'I_T_Obj',
'I_P_Obj',
'I_U_Obj',
'I_Menu2D',
'I_User',

'M_Gest',
'M_Move',
'M_Tele']

for act in action:
  dagent,dobj,dmenu,duser = 0,0,0,0
  iagent,iobj,itobj,ipobj,iuobj,imenu,iuser = 0,0,0,0,0,0,0
  mgest,mmove,mtele = 0,0,0
  
  for x in range(len(a)-1):
    if(act == a[x]):
      if a[x+1] == action[0]: dagent += 1
      elif a[x+1] == action[1]: dobj += 1
      elif a[x+ 1] == action[2]: dmenu += 1
      elif a[x+1] == action[3]: duser += 1
      elif a[x+1] == action[4]: iagent += 1
      elif a[x+1] == action[5]: iobj += 1
      elif a[x+1] == action[6]: itobj += 1
      elif a[x+1] == action[7]: ipobj += 1
      elif a[x+1] == action[8]: iuobj += 1
      elif a[x+1] == action[9]: imenu += 1
      elif a[x+1] == action[10]: iuser += 1
      elif a[x+1] == action[11]: mgest += 1
      elif a[x+1] == action[12]: mmove += 1 
      elif a[x+1] == action[13]: mtele += 1
    
  #print(act,":",dagent,dobj,dmenu,duser)
    
  #print("%s : (dagent %.2f) (dojb %.2f) (dmenu %.2f) (duser %.2f)" % (act,dagent/5,dobj/173,dmenu/28,duser/30))
  #print("%s : (iagent %.2f) (iojb %.2f) (itobj %.2f) (ipobj %.2f) (iuobj %.2f) (imenu %.2f) (iuser %.2f)" % (act,iagent/1,iobj/41,itobj/32,ipobj/21,iuobj/44,imenu/11,iuser/2))
  #print("%s : (mgest %.2f) (mmove %.2f) (mtele %.2f)" % (act,mgest/15,mmove/36,mtele/65))


  #print("%s : %.2f %.2f %.2f %.2f" % (act,dagent/5,dobj/173,dmenu/28,duser/30))
  #print("%s : %.2f %.2f %.2f %.2f %.2f %.2f %.2f" % (act,iagent/1,iobj/41,itobj/32,ipobj/21,iuobj/44,imenu/11,iuser/2))
  #print("%s : %.2f %.2f %.2f" % (act,mgest/15,mmove/36,mtele/65))
  #print()

  print("%.2f, %.2f, %.2f, %.2f," % (dagent/5,dobj/198,dmenu/31,duser/30), end="")
  print("%.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f," % (iagent/1,iobj/47,itobj/34,ipobj/21,iuobj/44,imenu/11,iuser/2), end="")
  print("%.2f, %.2f, %.2f" % (mgest/15,mmove/44,mtele/68), end="")
  print()