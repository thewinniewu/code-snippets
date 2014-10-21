#####################################################################
#                                                                   #
# Thumbtack Coding Challenge -- SWE Intern Application Summer 2015  #
# Winnie Wu (weiwu@college.harvard.edu)                             #
#                                                                   #
#####################################################################

####---------------- global variables --------------------- ####

level = 0 #level of 'begins' we are at
vdict = {level : {}} #dictionary to store variables
fdict = {level : {}} #dictionary to store frequency of values
ddict = {level : {}} #dictionary to denote what needs to be deleted at each level
fresh_transaction = True #whether or not we have an untouched transaction

####---------------- helper functions --------------------- ####

# recursively find variable in lower levels of vdict.  
# returns -1 if the variable doesn't exist in any level
def find(v, l):
  if (v in vdict[l]):
    return l
  else:
    if l == 0:
      return -1
    return find(v, l-1)

# recursively find value in lower levels of fdict.
# returns -1 if the value doesn't exist in any level
def findf(x, l):
  if (x in fdict[l]):
    return l
  else:
    if l == 0:
      return -1
    return findf(x, l-1)

####---------------- control subfunctions --------------------- ####

# unsets the variable in the current level
def d_unset(v):
  global fresh_transaction 
  fresh_transaction = False
  # find what level the v is at and denote that it is
  # to be deleted using ddict. also update fdict.
  l = find(v, level)
  if (l != -1):
    if (vdict[l][v] in fdict[level]):
      fdict[level][vdict[l][v]] -= 1
    else:
      fdict[level][vdict[l][v]] = 0
    ddict[level][v] = 1

# sets the variable to the given value
def d_set(v, x):
  global fresh_transaction
  fresh_transaction = False
  #if the variable exists in the current level,
  #we unset it and then reset it to the new value
  #unset takes care of value freq update
  if (v in vdict[level]):
    d_unset(v)
  vdict[level][v] = x 
  #update the new value in the frequency dict 
  if (x in fdict[level]):
    fdict[level][x] += 1
  elif (level > 0 and x in fdict[level-1]):
    fdict[level][x] = fdict[level-1][x] + 1
  else:
    fdict[level][x] = 1

# get the value of the specified variable
# prints NULL if it doesn't exist
def d_get(v):
  l = find(v, level)
  if ((l == -1) or (v in ddict[level] and ddict[level][v] == 1)):
    print "NULL" 
  else:
    print(vdict[l][v])

# gets the number of variables equal to value specified
def d_numeq(x):
  l = findf(x, level)
  if (l != -1):
    if (fdict[l][x] == 0):
      print "0"
    else:
      print fdict[l][x]
  else: 
    print "0"

# recursively copies each level's variable-value
# pairings down to level 0 and resets the global
# level. Effectively 'flattens' the levels.
# Also handles flattening the freq dict.
def commit(l):
  #base case
  if l == 0:
    global level
    level = 0
    global fresh_transaction
    fresh_transaction = True
    return
  # fold variable dict 
  for vx in vdict[l].iteritems():
    vkey = vx[0]
    vdict[l-1][vkey] = vdict[l][vkey]
  del vdict[l] 
  # fold frequency dict 
  for xv in fdict[l].iteritems():
    xkey = xv[0]
    fdict[l-1][xkey] = fdict[l][xkey]
  del fdict[l]
  # delete necessary vars
  for v in ddict[l].iteritems():
    vkey = v[0]
    v_l = find(vkey, l-1)
    if (v_l != -1):
      del vdict[v_l][vkey]
  del ddict[l]
  #recurse
  commit(l-1) 

# open a new transaction block by adding new dict levels 
def begin():
  global level
  level += 1
  fdict[level] = {}
  vdict[level] = {}
  ddict[level] = {} 

# perform a rollback since the last BEGIN or COMMIT
def rollback():
  global level
  global fresh_transaction 
  if (fresh_transaction):
    print "NO TRANSACTION"
  # if already on base level, just clear dicts
  if level == 0:
    vdict[level] = {}
    fdict[level] = {}
    ddict[level] = {}
    return
  # else, strip a level 
  del vdict[level]
  del fdict[level]
  del ddict[level] 
  level -= 1

####---------------- main control--------------------- ####
input = raw_input().split()

while (input[0] != "END"):
  if (input[0] == "SET" and len(input) == 3): 
    d_set(input[1], input[2])
  elif (input[0] == "GET" and len(input) == 2):
    d_get(input[1])
  elif (input[0] == "UNSET" and len(input) == 2):
    d_unset(input[1])
  elif (input[0] == "NUMEQUALTO" and len(input) == 2):
    d_numeq(input[1])
  elif (input[0] == "BEGIN"):
    begin() 
  elif (input[0] == "ROLLBACK"):
    rollback() 
  elif (input[0] == "COMMIT"):
    commit(level) 
  else:
    print "Error! Command not recognized"
  
  input = raw_input().split()

exit()
