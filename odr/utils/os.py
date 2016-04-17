from subprocess import call, Popen, PIPE


def output_from_cmd(cmd, strip_new_lines=True, join_result=None):
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    if stderr:
        raise Exception(stderr)

    if strip_new_lines:
        stdout = stdout.split('\n')

        if join_result is not None:
            return join_result.join(stdout)

    return stdout


def run_cmd(cmd):
    call(cmd)