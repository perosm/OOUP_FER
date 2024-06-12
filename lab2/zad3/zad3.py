def mymax(iterable, key=lambda x: x): # omogucili pozivanje samo 1 argumentom
    # incijaliziraj maksimalni element i maksimalni ključ
    max_x=max_key=None

    # obiđi sve elemente
    for x in iterable:
        # ako je key(x) najveći -> ažuriraj max_x i max_key
        if max_x is None or key(x) > max_key:
            max_x = x
            max_key = key(x)
        
    # vrati rezultat
    return max_x

if __name__ == '__main__':
    maxint = mymax([1, 3, 5, 7, 4, 6, 9, 2, 0])
    print(f'maxint: {maxint}')
    maxchar = mymax("Suncana strana ulice")
    print(f'maxchar: {maxchar}')
    maxstring = mymax([
    "Gle", "malu", "vocku", "poslije", "kise",
    "Puna", "je", "kapi", "pa", "ih", "njise"]) #najdulju riječ
    print(f'maxstring: {maxstring}')
    D={'burek':8, 'buhtla':5}
    maxdict = mymax(D, lambda x: D.get(x)) # Objasnite kako i zašto metodu možemo koristiti kao slobodnu funkciju. 
    print(f'maxdict: {maxdict}')

    people = [('A', 'B'), ('K', 'Z'), ('C', 'D'), ('I', 'J'), ('K', 'L'), ('G', 'H')]
    maxlistoftuples = mymax(people)
    print(f'maxlistoftuples: {maxlistoftuples}') 
