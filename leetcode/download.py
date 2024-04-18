import datasets
import psycopg2
from huggingface_hub import login
from constants import *

login(HF_READ_TOKEN)

dataset_name = 'LimYeri/LeetCode_YT_CC_CoT_Summary'
split = 'train'
cache_dir = 'cache-leetcode'

dataset = datasets.load_dataset(dataset_name, split=split, cache_dir=cache_dir)

print(dataset)

def get_db_connection():
    return psycopg2.connect(database="thesis", user='postgres', password='1234', host='127.0.0.1', port= '5432')

def create_table():
    conn = get_db_connection()
    query = '''
        CREATE TABLE IF NOT EXISTS leetcode (
            cc_content TEXT,
            id INT,
            thumbnail TEXT,
            title TEXT,
            question_content TEXT,
            java TEXT,
            cpp TEXT,
            python TEXT,
            javascript TEXT,
            title_slug TEXT,
            level TEXT,
            success_rate FLOAT,
            total_submission FLOAT,
            total_accepted FLOAT,
            question_likes FLOAT,
            question_dislikes FLOAT,
            question_hints TEXT,
            similar_question_ids TEXT,
            num_tokens INT,
            summary TEXT
        );
    '''
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

if __name__ == '__main__':
    create_table()
    conn = get_db_connection()
    cur = conn.cursor()
    for sample in dataset:
        print(sample['id'])
        cur.execute('''
            INSERT INTO leetcode (
                cc_content,
                id,
                thumbnail,
                title,
                question_content,
                java,
                cpp,
                python,
                javascript,
                title_slug,
                level,
                success_rate,
                total_submission,
                total_accepted,
                question_likes,
                question_dislikes,
                question_hints,
                similar_question_ids,
                num_tokens,
                summary
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''', (
                sample["cc_content"],
                sample["id"],
                sample["thumbnail"],
                sample["title"],
                sample["question_content"],
                sample["java"],
                sample["c++"],
                sample["python"],
                sample["javascript"],
                sample["title_slug"],
                sample["level"],
                sample["success_rate"],
                sample["total_submission"],
                sample["total_accepted"],
                sample["question_likes"],
                sample["question_dislikes"],
                sample["question_hints"],
                sample["similar_question_ids"],
                sample["num_tokens"],
                sample["Summary"]
            )
        )
        conn.commit()
    conn.close()
