import shutil
import os
from datetime import datetime

def backup_outcomes():
    if not os.path.exists('backup'):
        os.makedirs('backup')

    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'backup/outcomes_backup_{now}.json'
    
    if os.path.exists('outcomes.json'):
        shutil.copy('outcomes.json', backup_filename)
