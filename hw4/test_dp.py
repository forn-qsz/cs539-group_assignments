import os
import sys
import linecache

def get_line_context(file_path, line_number):
    return linecache.getline(file_path, line_number).strip()

def main():
    args = sys.argv[1:]
    file_path = './epron-jpron.data'
    command = []

    for arg in args:
        ep, jp = get_line_context(file_path, int(arg)), get_line_context(file_path, int(arg)+1)
        command.append(ep + r'\n' + jp)

    print('echo "{}" | python3 ./em_dp.py 5'.format(r'\n'.join(command)))
    os.system('echo "{}" | python3 ./em_dp.py 5'.format(r'\n'.join(command)))

if __name__ == "__main__":
    main()