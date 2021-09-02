import sys
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-o", "--output", help="Output setup.py")
argv = parser.parse_args()

setup = [line for line in open('setup.py')]

def upgrade_version(setup_lines):
    text, version = setup_lines.split('=')
    beginning, main, end = version.split('"')
    first, second, third = [int(_) for _ in main.split('.')]
    if third < 99:
        third = third + 1
    elif third >= 99:
        third = 0
        if second < 9:
            second = second + 1
        elif second >= 9:
            second = 0
            first = first + 1
    main = ".".join((str(first), str(second), str(third)))
    version = '"'.join((beginning, main, end))
    setup_lines = '='.join((text, version))
    return setup_lines

def keyboard_interrupt(setup_file):
    print("Version upgrade failed. Exiting")
    with open("setup.py", "w+") as f:
        f.write(setup_file)
    input("Press any key to exit")

new_setup = []
for line in setup:
    if 'version' in line and '=' in line:
        print(f"Line: {line.encode()}")
        line = upgrade_version(line)
        print(f"Line: {line.encode()}")
        exit_program = False
        try:
            is_n = input("Continue with the change (Y/N)? ")
            if is_n.upper() == "N":
                exit_program = True
        except KeyboardInterrupt:
            exit_program = True
        if exit_program:
            print("Stopping setup.py upgrade")
            sys.exit(10)
    new_setup.append(line)
with open("setup.py", "w+") as f:
    for line in new_setup:
        f.write(line)
