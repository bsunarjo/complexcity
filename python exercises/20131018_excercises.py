# Ex a
for a in range(0,3):
    print('####')

# Ex b
for a in range(0,4):
    c = '0' if a % 2 else '#'
    print(4 * c)

# Ex c
for a in range(1,6):
    print(a * '#')

# Ex d
for a in range(0,4):
    print(3 * '#0')

# Ex e
for a in range(0,4):
    c = '0#' if a % 2 else '#0'
    print(3*c)
    
# Ex f
for a in range(0,9):
    if a % 4 < 2:
        c = '#0'*a
    else:
        c = '0#' * a
    print(c[0:a])


    