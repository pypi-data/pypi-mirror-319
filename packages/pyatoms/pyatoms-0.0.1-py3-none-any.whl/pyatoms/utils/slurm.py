import json
import os
import subprocess


def submit_scheduler(file_name, num_unit, task_id_start, command=('command', 'sbatch')):
    if not os.path.isfile(file_name):
        raise FileNotFoundError('utils.submit_scheduler: %s is not a file.' % (file_name))
    
    idx_start = task_id_start
    idx_end = idx_start + num_unit - 1
    
    command = list(command)
    command.extend(['--array=%d-%d' % (idx_start, idx_end), file_name])
    result = subprocess.run(
        command, 
        text=True, 
        capture_output=True, 
    )
    
    if (result.stderr!='') or (result.returncode!=0):
        return False, result.stderr, result.returncode
    else:
        return True, int(result.stdout.split()[3])


def submit(file_name, command=('command', 'sbatch')):
    if not os.path.isfile(file_name):
        raise FileNotFoundError('utils.submit: %s is not a file.' % (file_name))
    
    command = list(command)
    command.append(file_name)
    result = subprocess.run(
        command, 
        text=True, 
        capture_output=True, 
    )
    
    if (result.stderr!='') or (result.returncode!=0):
        return False, result.stderr, result.returncode
    else:
        return True, int(result.stdout.split()[3])


def get_squeue_info(command=('command', 'squeue')):
    command = list(command)
    command.extend(['--me', '--json'])
    result = subprocess.run(
        command, 
        text=True, 
        capture_output=True, 
    )
    
    if (result.stderr!='') or (result.returncode!=0):
        return False, result.stderr, result.returncode
    else:
        all_info = json.loads(result.stdout)
        
        important_info = []
        for i in all_info['jobs']:
            if int(i['array_job_id']['number']) != 0:
                job_id = int(i['array_job_id']['number'])
                task_id = int(i['array_task_id']['number'])
            else:
                job_id = int(i['job_id'])
                task_id = None
            
            if isinstance(i['job_state'], list):
                job_state = i['job_state'][0]
            else:
                job_state = i['job_state']
            
            if i['array_task_string'] == '':
                num_task = 1
            else:
                if '-' not in i['array_task_string']:
                    num_task = 1
                else:
                    start = int(i['array_task_string'].split('-')[0])
                    end = int(i['array_task_string'].split('-')[1])
                    num_task = end - start + 1
            
            important_info.append(
                {
                    'job_id': job_id, 
                    'task_id':  task_id, 
                    'job_state': job_state, 
                    'array_task_string': i['array_task_string'], 
                    'num_task': num_task, 
                }
            )
        
        return True, all_info, important_info
