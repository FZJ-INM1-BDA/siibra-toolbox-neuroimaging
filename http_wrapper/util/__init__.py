import os

working_dir = os.getenv("SIIBRA_TOOLBOX_NIT_WORKING_DIR", "./workingdir")

def _get_task_workdir(task_id:str):
    path_to_dir = os.path.abspath(os.path.join(working_dir, task_id))
    os.makedirs(path_to_dir, exist_ok=True)
    return path_to_dir
    
def get_task_inputdir(task_id:str):
    task_working_dir = _get_task_workdir(task_id)
    input_dir = os.path.join(task_working_dir, "input")
    os.makedirs(input_dir, exist_ok=True)
    return input_dir

def get_task_outputdir(task_id:str):
    task_working_dir = _get_task_workdir(task_id)
    output_dir = os.path.join(task_working_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir
