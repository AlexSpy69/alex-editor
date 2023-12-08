import subprocess

def execute_command(c: str, wd: str) -> str:
    command = f"gnome-terminal --working-directory={wd} -- {c}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    exitcode = process.returncode
    return stderr.decode("utf-8")

def run_py_code(command: str) -> str:
    try:
        exec(command)
        return ""
    except Exception as e:
        return str(e)

def get_file_type(filename: str) -> str:
    if filename.endswith(".py"):
        return "Python"
    elif filename.endswith(".c") or filename.endswith(".cpp") or \
        filename.endswith(".h") or filename.endswith(".hpp"):
        return "C/C++"
    elif filename.endswith(".sh"):
        return "sh"
    elif filename.endswith(".html"):
        return "HTML"
    elif filename.endswith(".txt"):
        return "Plain text"
    else:
        return filename.split(".")[-1]

def open_terminal(dir_: str) -> str:
    command = f"gnome-terminal --working-directory={dir_}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    exitcode = process.returncode
    return stderr.decode("utf-8")

def replace(string: str, words: dict) -> str:
    for k in words.keys():
        string = string.replace(k, words[k])
    return string
