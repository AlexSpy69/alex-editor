import subprocess

def execute_command(c, wd) -> str:
    command = f"gnome-terminal --working-directory={wd} -- {c}"
    print(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    exitcode = process.returncode
    if exitcode == 0:
        return "Success"
    else:
        return stderr.decode("utf-8")

def run_py_code(command) -> str:
    try:
        exec(command)
        return ""
    except Exception as e:
        return str(e)
