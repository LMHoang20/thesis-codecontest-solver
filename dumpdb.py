import os

from database import get_db_conn

def get_editorials():
    connection = get_db_conn()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT c.name, c.description, c.editorial, c.solutions, c.split, r.note
        FROM cleaned_editorials c 
        LEFT JOIN editorials_raw r ON c.name = r.name
    """)
    editorials = cursor.fetchall()
    cursor.close()
    connection.close()
    return editorials

editorials = get_editorials()

dataset = {
    'train': {
        'name': [],
        'description': [],
        'editorial': [],
        'solution': [],
        'note': []
    },
    'validate': {
        'name': [],
        'description': [],
        'editorial': [],
        'solution': [],
        'note': []
    },
    'test': {
        'name': [],
        'description': [],
        'editorial': [],
        'solution': [],
        'note': []
    },
    'leetcode': {
        'name': [],
        'description': [],
        'editorial': [],
        'solution': [],
        'note': []
    }
}

for editorial in editorials:
    split = editorial[4]
    assert split in dataset.keys()
    dataset[split]['name'].append(editorial[0])
    dataset[split]['description'].append(editorial[1])
    dataset[split]['editorial'].append(editorial[2])
    dataset[split]['solution'].append(editorial[3][0])
    dataset[split]['note'].append(editorial[5] if editorial[5] else '')

from huggingface_hub import login
import datasets
from constants import HF_WRITE_TOKEN

login(HF_WRITE_TOKEN)

# push dataset to hub

for split, data in dataset.items():
    dataset = datasets.Dataset.from_dict(data)
    dataset.push_to_hub('editorials', split=split, private=True)
