def roundRobin():
  listaInstancias = ['44.202.236.64', '44.202.236.64', '44.202.236.64']

  with open("robin.txt", 'r') as f:
    i = f.readline()
    f.close()

  if i == '0':
    i = int(i) + 1 
    A = open ('robin.txt','w')
    A.write(str(i))
    A.close()
    return listaInstancias[0]
  elif i == '1':
    i = int(i) + 1
    A = open ('robin.txt','w')
    A.write(str(i))
    A.close()
    return listaInstancias[1]
  elif i == '2':
    i = 0
    A = open ('robin.txt','w')
    A.write(str(i))
    A.close()
    return listaInstancias[2]

if __name__ == "__main__":
  roundRobin()
