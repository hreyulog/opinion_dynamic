with open('test_weibo.txt', 'r', encoding='utf-8') as reader:
    with open('test_weibo_new.txt','w',encoding='utf-8') as writer:
        for row in reader:
            row_list=row.strip().split(',')
            print(str(row_list[2])+','+row_list[1])
            writer.write(str(row_list[2])+'\t'+row_list[1]+'\n')