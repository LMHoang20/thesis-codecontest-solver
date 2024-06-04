import datasets
import re

from huggingface_hub import login
from download_code import get_db_conn
from constants import *

def get_summaries():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, s.contest_id, s.problem_id, s.summary, p.name, p.description, p.cf_tags, p.cf_rating
        FROM summaries s JOIN problems p ON s.contest_id::int8 = p.cf_contest_id AND s.problem_id = p.cf_index
        ORDER BY id
    ''')
    summaries = cursor.fetchall()
    cursor.close()
    return summaries

black_list = [
    69, 78, 192, 217, 260, 300, 321, 343, 377, 407, 484, 485, 515, 568, 582, 605, 
    695, 710, 711, 753, 855, 1078, 1163, 1212, 1217, 1229, 1318, 1400, 1729, 1844,
    1853, 1900, 2022
]

white_list = [
    9, 159, 194, 283, 541, 692, 731, 758, 778, 801, 818, 871, 897, 899, 939, 
    1029, 1066, 1104, 1145, 1164, 1170, 1208, 1238, 1261, 1267, 1284, 1344, 1346,
    1366, 1368, 1369, 1370, 1398, 1469, 1483, 1484, 1486, 1517, 1529, 1540, 1547,
    1584, 1594, 1607, 1635, 1666, 1672, 1720, 1731, 1768, 1769, 1778, 1812, 1814,
    1815, 1876, 1880, 1886, 1940, 1941, 1947, 2000, 2003, 2008, 2009, 2024, 2030,
    2033, 2065, 2069, 2090, 2099
]

def not_good(summary):
    if '</META-REASONING>' in summary:
        return '</META-REASONING>\n<OBSERVATION>' not in summary \
            or '<PLANNING>' not in summary \
            or '</OBSERVATION>\n<PLANNING>' not in summary \
            or '</PLANNING>' not in summary
    return '</OBSERVATION>' not in summary \
        or '<PLANNING>' not in summary \
        or '</OBSERVATION>\n<PLANNING>' not in summary \
        or '</PLANNING>' not in summary

stepRe = re.compile(r'- \*\*[Ss]tep (?:[\d\.]+):\*\*')
observationRe = re.compile(r'- \*\*[Oo]bservation (?:[\d\.]+):\*\*')
planningRe = re.compile(r'- \*\*[Pp]lanning (?:[\d\.]+):\*\*')

if __name__ == '__main__':
    summaries = get_summaries()
    dataset = {
        'contest_id': [],
        'problem_id': [],
        'name': [],
        'description': [],
        'tags': [],
        'rating': [],
        'observation': [],
        'planning': [],
    }
    for summary in summaries:
        id, contest_id, problem_id, summary, name, description, tags, rating = summary
        if id in white_list:
            if not summary.endswith('\n</PLANNING>'):
                summary += '\n</PLANNING>'
        if id in black_list:
            continue
        # print(f'{id}, {contest_id}, {problem_id}')
        observation = ""
        if '</META-REASONING>' in summary:
            if summary.startswith('<META-REASONING>'):
                summary = summary[len('<META-REASONING>'):]
            observation = summary.split('</META-REASONING>\n<OBSERVATION>')[1].split('</OBSERVATION>')[0]
        else:
            if summary.startswith('<OBSERVATION>'):
                summary = summary[len('<OBSERVATION>'):]
            observation = summary.split('</OBSERVATION>')[0].strip()
        assert not observation.startswith('<OBSERVATION>'), f'{contest_id}, {problem_id}, {id}, {summary}, {observation}'
        assert not observation.endswith('</OBSERVATION>'), f'{contest_id}, {problem_id}, {id}, {summary}, {observation}'
        if '<PLANNING>\n<PLANNING>' in summary:
            summary = summary.replace('<PLANNING>\n<PLANNING>', '<PLANNING>\n')
        planning = summary.split('</OBSERVATION>\n<PLANNING>')[1].split('</PLANNING>')[0].strip()
        assert not planning.startswith('<PLANNING>'), f'{contest_id}, {problem_id}, {id}, {summary}, {planning}'
        assert not planning.endswith('</PLANNING>'), f'{contest_id}, {problem_id}, {id}, {summary}, {planning}'

        stepMatches = stepRe.findall(planning)
        if len(stepMatches) > 0:
            for match in stepMatches:
                planning = planning.replace(match, '-')
        
        observationMatches = observationRe.findall(observation)
        if len(observationMatches) > 0:
            for match in observationMatches:
                observation = observation.replace(match, '-')
        
        planningMatches = planningRe.findall(planning)
        if len(planningMatches) > 0:
            for match in planningMatches:
                planning = planning.replace(match, '-')

        dataset['contest_id'].append(contest_id)
        dataset['problem_id'].append(problem_id)
        dataset['name'].append(name)
        dataset['description'].append(description)
        dataset['tags'].append(tags)
        dataset['rating'].append(rating)
        dataset['observation'].append(observation)
        dataset['planning'].append(planning)
    dataset = datasets.Dataset.from_dict(dataset)
    login(HF_WRITE_TOKEN)
    dataset.push_to_hub('HoangLe1312/codeforces-reasoning')