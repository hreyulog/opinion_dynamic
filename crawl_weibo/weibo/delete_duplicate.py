import pandas as pd
def delete_dup(user_id):
    df = pd.read_csv(f'{user_id}.csv')
    df = df.drop_duplicates()
    df = df[~df.isin(['微博id']).any(axis=1)]
    df.to_csv(f'{user_id}_clean.csv', index=False)

if __name__=="__main__":
    # delete_dup('2022252207')
    with open('list_crawler.txt', 'r', encoding='utf-8') as reader:
        for row in reader:
            id = row.split()[1]
            delete_dup(id)