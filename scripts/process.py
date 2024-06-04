import sys 
import subprocess

file_name = sys.argv[1]
tags = sys.argv[1:]

if 'formula' in tags:
    subprocess.run(['python', 'process_latex.py', file_name])
else:
    subprocess.run(['python', 'process_latex_no_formula.py', file_name])