lista = [1, "Python", [40, 30, 20]]

lista.copy()

print(lista)  # [1, "Python", [40, 30, 20]]

l2 = lista.copy()

print(id(l2),id(lista))  # IDs diferentes