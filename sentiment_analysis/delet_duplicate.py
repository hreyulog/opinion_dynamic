def delet_duplicate(filename):
    list_row = []
    with open(filename + 'new.txt', 'w', encoding='utf-8', newline='') as writer:
        with open(filename, 'r', encoding='utf-8') as reader:
            for row in reader:
                list_row.append(row)
        list_row=list(set(list_row))
        for row in list_row:
            writer.write(row)

if __name__=="__main__":
    delet_duplicate('neg.txt')
    delet_duplicate('pos.txt')