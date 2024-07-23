import yaml
import os

from database import get_db_conn
from helpers import remove_consecutive_line_breaks
from model import Gemini
from models.openai.gpt import GPT

from logger import get_logger
from sandbox import Judge
from repository import Problem

from MapCoder.src.evaluations.api_comm import APICommunication
from MapCoder.src.constants.lang_mappings import LANGUAGE_MAPPING

limits_by_lang_cfg_file = "./models/gemini/limits_by_lang.yaml"

assert os.path.exists(
    limits_by_lang_cfg_file), "Need resource limit defaults for all runtimes, provide the path to default 'limits_by_lang.yaml' or to the modified one."

with open(limits_by_lang_cfg_file) as limit_cfg_rp:
    limits_by_lang = yaml.safe_load(limit_cfg_rp)

def get_editorials():
    connection = get_db_conn()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT c.name, c.description, c.editorial, c.solutions, c.split
        FROM cleaned_editorials c LEFT JOIN translated_editorials r ON c.name = r.name
        WHERE split in ('train', 'validate') AND r.name IS NULL
        ORDER BY c.name
    """)
    editorials = cursor.fetchall()
    cursor.close()
    connection.close()
    return editorials

def create_table_translated():
    connection = get_db_conn()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS translated_editorials (
        name TEXT PRIMARY KEY,
        code TEXT,
    )
""")
    connection.commit()
    cursor.close()
    connection.close()

def insert_translated_editorial(name, code, language, translated_code, follows_instructions, is_clean):
    connection = get_db_conn()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO translated_editorials VALUES (%s, %s, %s, %s, %s, %s)", (name, code, language, translated_code, follows_instructions, is_clean))
    connection.commit()
    cursor.close()
    connection.close()

def generate(model, logger, document):
    name, description, editorial, solutions, _ = document
    code = solutions[0].strip()
    language = solutions[0].strip().split('\n')[0]
    assert language == '```cpp' or language == '```py', f"{name} has invalid language"
    if language == '```cpp':
        language = 'C++'
        bad_language = 'C'
        input_output = 'cin, cout'
        bad_input_output = 'scanf, printf'
    else:
        language = 'Python'
        bad_language = 'Python 2'
        input_output = 'input(), print()'
        bad_input_output = 'raw_input(), print'

    system_prompt = f"""System: You are a legendary grandmaster on Codeforces. You are given the following problem, with its natural language solution and code solution in {language}.
# What to do:
- Read and understand the problem statement, natural language solution, and code solution carefully.
- Give an analysis whether the code solution is clean and follows the instructions in the natural language solution.
- If the code solution should be translated, refactor the code solution to make it more readable and follow the instructions in the natural language solution.
    - Split complicated logic into smaller functions (without compromising the efficiency).
    - Remove any template for custom input and output and use standard input and output (e.g., {input_output}).
    - If the code solution is in {bad_language}, refactor it to use {language}. For example, changing {bad_input_output} to {input_output}.
    - Add comments to explain the code.
    - Use meaningful variable names.
    - Remove any unused constants, variables, templates, and functions.

# Answer format:
You MUST answer in yaml format.
The root MUST be a dictionary with 4 keys:
- 'analysis': a multiline string that explains why the code solution is clean or not clean.
- 'follows_instructions': a boolean that indicates whether the code solution follows the instructions in the natural language solution.
- 'is_clean': a boolean that indicates whether the code solution is clean.
- 'translated_code': a multiline string that contains the translated code solution, null if the code solution is clean.

# Example:
```yaml
---
analysis: |
    The solution suggests that the optimal answer is simply the sum of the two integers. The code uses the correct formula to calculate the sum of the two integers.
    The code contains scanf and printf, which are not allowed. The code should use cin and cout instead.
follows_instructions: true
is_clean: false
translated_code: |
    #include <iostream>
    using namespace std;
    
    int main() {{
        int a, b;
        cin >> a >> b;
        cout << a + b << endl;
        return 0;
    }}
```

# Note:
- Do NOT change the correctness of the code solution.
- The answer MUST be a valid yaml format.
- Use | instead of > for multiline strings.
- Do NOT use bullet points, numbering, etc. in multiline strings to avoid yaml formatting issues.
"""
    user_prompt = f"""User: Help me refactor the following code solution in to Python 3.
<Description><![CDATA[
{description}
]]></Description>
<Editorial><![CDATA[
{editorial}
]]></Editorial>
<Code><![CDATA[
{code}
]]></Code>
"""
    init_assistant_prompt = "```yaml\n---\nanalysis: |"
    system_prompt = remove_consecutive_line_breaks(system_prompt)
    user_prompt = remove_consecutive_line_breaks(user_prompt)
    prompts = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": init_assistant_prompt}
    ]
    response = model.generate(prompts)
    response = response.strip()
    if not response.startswith(init_assistant_prompt):
        response = init_assistant_prompt + response
        response = response.strip()
    while response.startswith("```yaml"):
        response = response[len("```yaml"):]
        response = response.strip()
    while response.endswith("```"):
        response = response[:-len("```")]
        response = response.strip()
    response = response[response.index("follows_instructions:"):]
    response = yaml.safe_load(response)
    follows_instructions, is_clean, translated_code = response['follows_instructions'], response['is_clean'], response['translated_code']
    if not response['follows_instructions']:
        logger.warning(f"{name} does not follow instructions")
    if not response['is_clean']:
        translated_code = translated_code.strip()
        if translated_code.startswith("```"):
            translated_code = translated_code.split('\n')[1:]
            translated_code = '\n'.join(translated_code)
            translated_code = translated_code.strip()
        if translated_code.endswith("```"):
            translated_code = translated_code[:-len("```")]
            translated_code = translated_code.strip()
    else:
        translated_code = code
    return name, code, language, translated_code, follows_instructions, is_clean

def parse_result(results):
    verdict = 'PASSED'
    stdout = None
    test_input = None
    test_output = None
    for result in results[0]:
        if result['exec_outcome'] != 'PASSED':
            verdict = result['exec_outcome']
            stdout = result['result']
            test_input = result['input']
            if len(result['output']) > 0:
                test_output = result['output'][0]
            break
    return (verdict, stdout, test_input, test_output)

if __name__ == '__main__':
    # model = Gemini(temperature=1, top_p=0.5, top_k=10)
    model = GPT(model_name='gpt-3.5-turbo', temperature=0.5, top_p=0.8, max_tokens=4096, frequency_penalty=0, presence_penalty=0)
    editorials = get_editorials()
    logger = get_logger(type='file', config={'name': '', 'path': 'logs/clean_code-2.log', 'threadsafe': False})
    problem_repo = Problem(get_db_conn())
    create_table_translated()
    api = APICommunication(server_url = "http://localhost:5001")
    content = open('logs/clean_code.log', 'r').read()
    for editorial in editorials:
        name = editorial[0]
        print(name)
        if f'{name} original code failed' in content:
            continue
        solutions = editorial[3]
        code = '\n'.join(solutions[0].strip().split('\n')[1:-1])
        language = solutions[0].strip().split('\n')[0]
        assert language == '```cpp' or language == '```py', f"{name} has invalid language"
        language = language[3:]
        problem = problem_repo.get_problem(name)            
        assert problem is not None, f"{name} not found in the database"
        tests = problem.get_tests(public=True, private=True, generated=True)
        tests = [{"input": test[0], "output": [test[1]]} for test in tests]
        result = api.execute_code(
            language=LANGUAGE_MAPPING[language],
            source_code=code,
            unittests=tests,
            limits=limits_by_lang[LANGUAGE_MAPPING[language]],
            stop_on_first_fail=True
        )
        if any(result[0][i]['exec_outcome'] != 'PASSED' for i in range(len(result[0]))):
            logger.error(f"{name} original code failed")
            continue
        try:
            name, code, language, translated_code, follows_instructions, is_clean = generate(model, logger, editorial)
            if not is_clean:
                language = LANGUAGE_MAPPING[language]
                result = api.execute_code(
                    language=language,
                    source_code=translated_code,
                    unittests=tests,
                    limits=limits_by_lang[language],
                    stop_on_first_fail=True
                )
                # if any(result[0][i]['exec_outcome'] != 'PASSED' for i in range(len(result[0]))):
                #     logger.error(f"{name} failed")
                #     for _ in range(3):
                #         debugged_code = debug(model, logger, editorial, code, translated_code, result)
                #         debugged_result = api.execute_code(
                #             language=language,
                #             source_code=debugged_code,
                #             unittests=tests,
                #             limits=limits_by_lang[language],
                #             stop_on_first_fail=True
                #         )
                #         if any(debugged_result[0][i]['exec_outcome'] != 'PASSED' for i in range(len(debugged_result[0]))):
                #             logger.error(f"{name} failed {_ + 1} times")
                #         else:
                #             logger.info(f"{name} passed after {_ + 1} attempts")
                #             insert_translated_editorial(name, code, language, debugged_code, follows_instructions, is_clean)
                #             break
                # else:
                #     logger.info(f"{name} passed")
                #     insert_translated_editorial(name, code, language, translated_code, follows_instructions, is_clean)
            else:
                logger.info(f"{name} is clean")
                insert_translated_editorial(name, code, language, translated_code, follows_instructions, is_clean)
        except Exception as e:
            logger.error(f"{name} failed with error: {e}")
            continue
