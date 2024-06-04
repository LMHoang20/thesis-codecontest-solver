import re
import os
import sys
import google.generativeai as genai
import time

from models import get_llm_model
from database import get_db_conn
from constants import *

print(GOOGLE_API_KEY)

genai.configure(api_key=GOOGLE_API_KEY)

for m in genai.list_models():
    print(m)

cnt = 0

defaults = {
    'model': 'models/text-bison-001',
    'temperature': 1,
    'candidate_count': 1,
    'top_k': 1,
    'top_p': 1,
    'max_output_tokens': 32768,
}

def correct(text):
    # Prompt for correcting the grammar
    prompt_correction = f"Correct the grammar and vocabulary of the following essay:\nOriginal: {text}\nFixed Grammar:"

    # Assuming the API call returns the corrected text
    response = genai.generate_text(**defaults, prompt=prompt_correction)
    corrected_text = response.result.strip()  # Extract the corrected sentence from the response

    return corrected_text

def get_problem_names():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('SELECT p.name, p.cf_contest_id, p.cf_index FROM problems p JOIN editorials e ON p.name = e.name')
    return cur.fetchall()

def get_editorial(name):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('SELECT content FROM editorials WHERE name = %s', (name,))
    return cur.fetchone()[0]

def correct_with_gemini(text):
    gemini = get_llm_model('gemini')
    prompts = ["""Correct the grammar and vocabulary of the following text.
Make the minimum number of changes necessary to correct the text.
Do NOT add extra formatting or change the meaning of the text.
A list MUST start with - instead of *.
""", """Original:
The solution consists of several steps.
*The first step.* Let's find out "does the first box contain stone or valuable gift" using random. Let's make $30$ queries to compare the weight of the first box with the weight of another random box. If the first box is lighter than we found an answer, otherwise the probability of the first box having stones is at least $1 - 2^{-30}$.
*The second step.* Let's compare the weights of the first box and the second one. If they are equal then let's compare the weights of boxes $[1, 2]$ and $[3,4]$. If they are equal then let's compare the boxes $[1 \dots 4]$ and $[5 \dots 8]$ and so on. In other words, let's find the minimum $k \ge 0$ such that $[1, 2^k]$ contains only boxes with stones but $[2^k + 1, 2^{k + 1}]$ contain at least one box with a valuable gift. It's easy to see that we'd spend no more than $10$ queries.
*The third step.* We have segment $[1, 2^k]$ with only stones and $[2^k + 1, 2^{k + 1}]$ with at least one gift. Let's just binary search the leftmost gift in the segment $[2^k + 1, 2^{k + 1}]$ using boxes from $[1, 2^k]$ as reference: if we need to know "does segment of boxes $[l, mid)$ have at least one gift", let's just compare it with segment $[0, mid - l)$ which have only stones. if $[l, mid)$ is lighter then it has, otherwise doesn't have. This part also requires no more than $10$ queries.
""", """Fixed:
The solution consists of several steps.

The first step: We can use randomness to determine whether the first box contains a stone or a valuable gift. We can make 30 queries to compare the weight of the first box with the weight of another random box. If the first box is lighter, then we have found an answer. Otherwise, the probability that the first box contains stones is at least $1 - 2^{-30}$.

The second step: We compare the weights of the first box and the second box. If they are equal, then we compare the weights of the boxes $[1, 2]$ and $[3,4]$. If they are equal, then we compare the boxes $[1 \dots 4]$ and $[5 \dots 8]$, and so on. In other words, we find the minimum $k \ge 0$ such that $[1, 2^k]$ contains only boxes with stones, but $[2^k + 1, 2^{k + 1}]$ contains at least one box with a valuable gift. It is easy to see that this process requires no more than 10 queries.

The third step: We have the segments $[1, 2^k]$ with only stones and $[2^k + 1, 2^{k + 1}]$ with at least one gift. We can simply perform a binary search on the leftmost gift in the segment $[2^k + 1, 2^{k + 1}]$ using the boxes from $[1, 2^k]$ as reference: if we need to know whether the segment of boxes $[l, mid)$ contains at least one gift, then we simply compare it with the segment $[0, mid - l)$, which contains only stones. If $[l, mid)$ is lighter, then it contains a gift; otherwise, it does not. This part also requires no more than 10 queries.
""", f"""Original:
{text}
""", f"""Fixed:
"""]
    corrected_text = gemini.generate(prompts)
    return corrected_text

def main():
    problems = get_problem_names()
    problems = list(problems)
    while len(problems) > 0:
        try:
            name, contest_id, index = problems[0]
            problems = problems[1:]
            if name.startswith('708'):
                continue
            path = f'data/corrected/{contest_id}-{index}.md'
            corrected_path = f'data/corrected/{contest_id}-{index}-corrected.md'
            corrected_path_gemini = f'data/corrected/{contest_id}-{index}-corrected-gemini.md'
            if os.path.exists(corrected_path):
                with open(corrected_path, 'r') as f:
                    content = f.read()
                token_count = genai.count_message_tokens(prompt=content)['token_count']
                time.sleep(60/90 + 0.1)
                if token_count > 1000:
                    print(corrected_path, token_count)
                    continue
                    editorial = get_editorial(name)
                    corrected_text = correct_with_gemini(editorial)
                    print(corrected_path, token_count)
                    with open(corrected_path_gemini, 'w') as f:
                        f.write(corrected_text)
                    print('Gemini corrected', corrected_path_gemini)
                continue
            else:
                print('not found', corrected_path)
                continue
                editorial = get_editorial(name)
                corrected_text = correct_with_gemini(editorial)
                print(corrected_path, len(corrected_text))
                with open(corrected_path_gemini, 'w') as f:
                    f.write(corrected_text)
                print('Gemini corrected', corrected_path_gemini)
            # editorial = get_editorial(name)
            # print(f'Correcting {path}')
            # with open(path, 'w') as f:
            #     f.write(editorial)
            # corrected_text = correct(editorial)
            # print(f'Corrected {corrected_path}')
            # with open(corrected_path, 'w') as f:
            #     f.write(corrected_text)
            # time.sleep(60/90 + 0.1)
        except Exception as e:
            print(e)
            problems.append((name, contest_id, index))

if __name__ == '__main__':
    main()

# XXX = set()
# file_to_correct = []
# for root, dirs, files in os.walk('data/contests-extra'):
#     # for file in files:
#     #     if 'corrected' in file:
#     #         print(file)
#     #         os.remove(f'{root}/{file}')
#     for dir in dirs:
#         if '-' in dir:
#             continue
#         for root, _, files in os.walk(f'data/contests-extra/{dir}'):
#             for file in files:
#                 if '-' in file:
#                     continue
#                 if 'editorial' in file:
#                     continue
#                 if 'corrected' in file:
#                     continue
#                 if os.path.exists(f'{root}/{file[:-3]}-corrected.md'):
#                     continue
#                 file_to_correct.append((root, file))

# while len(file_to_correct) > 0:
#     root, file = file_to_correct[0]
#     file_to_correct = file_to_correct[1:]
#     try:
#         print(f'Correcting {root}/{file}')
#         with open(f'{root}/{file}', 'r') as f:
#             text = f.read()
#             if 'TUTORIAL CODE XXX' in text:
#                 content = text.split('TUTORIAL CODE XXX')[0]
#                 code = text.split('TUTORIAL CODE XXX')[1]
#             else:
#                 content = text
#                 code = ''
#             corrected_text = correct(content)
#             with open(f'{root}/{file[:-3]}-corrected.md', 'w') as f:
#                 f.write(corrected_text)
#                 if code:
#                     f.write(f'\n\nTUTORIAL CODE XXX{code}')
#             time.sleep(60/90 + 0.1)
#     except Exception as e:
#         file_to_correct.append((root, file))
#         print(e)
#         time.sleep(60/90 + 0.1)
# print(XXX)