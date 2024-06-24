import yaml
import os

from database import get_db_conn
from helpers import remove_consecutive_line_breaks
from model import Gemini

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
        FROM cleaned_editorials c LEFT JOIN refactored_editorials r ON c.name = r.name
        WHERE split in ('train', 'validate') AND r.name IS NULL
        ORDER BY c.name
    """)
    editorials = cursor.fetchall()
    cursor.close()
    connection.close()
    return editorials

def create_table_refactored():
    connection = get_db_conn()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS refactored_editorials (
        name TEXT PRIMARY KEY,
        code TEXT,
        language TEXT,
        refactored_code TEXT,
        follows_instructions BOOLEAN,
        is_clean BOOLEAN
    )
""")
    connection.commit()
    cursor.close()
    connection.close()

def insert_refactored_editorial(name, code, language, refactored_code, follows_instructions, is_clean):
    connection = get_db_conn()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO refactored_editorials VALUES (%s, %s, %s, %s, %s, %s)", (name, code, language, refactored_code, follows_instructions, is_clean))
    connection.commit()
    cursor.close()
    connection.close()

def generate(model, logger, document):
    name, description, editorial, solutions, _ = document
    code = solutions[0].strip()
    language = solutions[0].strip().split('\n')[0]
    assert language == '```cpp' or language == '```py'
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

    prompt = f"""System: You are a legendary grandmaster on Codeforces. You are given the following problem, with its natural language solution and code solution in {language}.
# What to do:
- Read and understand the problem statement, natural language solution, and code solution carefully.
- Give an analysis whether the code solution is clean and follows the instructions in the natural language solution.
- If the code solution should be refactored, refactor the code solution to make it more readable and follow the instructions in the natural language solution.
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
- 'refactored_code': a multiline string that contains the refactored code solution, null if the code solution is clean.

# Example:
```yaml
---
analysis: |
    The solution suggests that the optimal answer is simply the sum of the two integers. The code uses the correct formula to calculate the sum of the two integers.
    The code contains scanf and printf, which are not allowed. The code should use cin and cout instead.
follows_instructions: true
is_clean: false
refactored_code: |
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
- Do not change the correctness of the code solution.
- Use | instead of > for multiline strings.
- Bullet points in multiline strings MUST begin with star (*) instead of - (dash) to avoid yaml parsing issues.

User: Help me refactor the following code solution in {language}.
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
    prompt = remove_consecutive_line_breaks(prompt)
    print(prompt)
    init_model_prompt = "```yaml\n---\nanalysis: |\n"
    prompts = [prompt, init_model_prompt]
    response = model.generate(prompts)
    print(response)
    if not response.startswith(init_model_prompt):
        response = init_model_prompt + response
        response = response.strip()
    if response.startswith("```yaml"):
        response = response[len("```yaml"):]
        response = response.strip()
    if response.endswith("```"):
        response = response[:-len("```")]
        response = response.strip()
    response = yaml.safe_load(response)
    follows_instructions, is_clean, refactored_code = response['follows_instructions'], response['is_clean'], response['refactored_code']
    if not response['follows_instructions']:
        logger.warning(f"{name} does not follow instructions")
    if not response['is_clean']:
        refactored_code = refactored_code.strip()
        if refactored_code.startswith("```"):
            refactored_code = refactored_code.split('\n')[1:]
            refactored_code = '\n'.join(refactored_code)
            refactored_code = refactored_code.strip()
        if refactored_code.endswith("```"):
            refactored_code = refactored_code[:-len("```")]
            refactored_code = refactored_code.strip()
    else:
        refactored_code = code
    return name, code, language, refactored_code, follows_instructions, is_clean

if __name__ == '__main__':
    model = Gemini(temperature=1, top_p=0.5, top_k=10)
    editorials = get_editorials()
    logger = get_logger(type='file', config={'name': '', 'path': 'logs/clean_code.log', 'threadsafe': False})
    problem_repo = Problem(get_db_conn())
    create_table_refactored()
    api = APICommunication(server_url = "http://localhost:5001")
    for editorial in editorials:
        name = editorial[0]
        print(name)
        try:
            name, code, language, refactored_code, follows_instructions, is_clean = generate(model, logger, editorial)
            if not is_clean:
                problem = problem_repo.get_problem(name)            
                assert problem is not None
                tests = problem.get_tests(public=True, private=True, generated=True)
                tests = [{"input": test[0], "output": [test[1]]} for test in tests]
                language = LANGUAGE_MAPPING[language]
                result = api.execute_code(
                    language=language,
                    source_code=refactored_code,
                    unittests=tests,
                    limits=limits_by_lang[language],
                    stop_on_first_fail=True
                )
                if any(result[0][i]['exec_outcome'] != 'PASSED' for i in range(len(result[0]))):
                    logger.error(f"{name} failed")
                else:
                    logger.info(f"{name} passed")
                    insert_refactored_editorial(name, code, language, refactored_code, follows_instructions, is_clean)
            else:
                logger.info(f"{name} is clean")
                insert_refactored_editorial(name, code, language, refactored_code, follows_instructions, is_clean)
        except Exception as e:
            logger.error(f"{name} failed with error: {e}")
            continue
