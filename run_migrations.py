import os
import sys
import subprocess

base_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(base_dir, 'backend')
venv_python = os.path.join(base_dir, '.venv', 'Scripts', 'python.exe')

def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=backend_dir)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    return result.stdout + "\n" + result.stderr

with open('migration_output.txt', 'w') as f:
    f.write(run_cmd(f'"{venv_python}" manage.py makemigrations accounts'))
    f.write(run_cmd(f'"{venv_python}" manage.py migrate accounts'))
