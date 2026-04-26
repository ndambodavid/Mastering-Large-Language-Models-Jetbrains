import sys
import os

# Make task.py importable and give it access to envvars (NLPBasics/)
_TASK_DIR = os.path.dirname(os.path.abspath(__file__))
_LESSON_DIR = os.path.dirname(_TASK_DIR)
for _p in (_TASK_DIR, _LESSON_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
