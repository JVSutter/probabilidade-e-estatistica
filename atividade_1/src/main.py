import csv

def main():
    with open('../assets/rym_clean1.csv', 'r') as file:
        reader = csv.reader(file)  # reader object, pode ser convertido em uma lista (de listas)
        # cada row é uma lista
        for row in reader:
            print(row)

if __name__ == '__main__':
    main()