import os
import sys
import logging
import argparse
import re

VARIABLE_DECL = r'^variable \"([\w_]+)\" {'
VARIABLE = r'var\.([\w_]+)'

log = logging.getLogger(__name__)
log.setLevel(level=logging.WARN)
loghandler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(levelname)-4s %(message)s')
loghandler.setFormatter(formatter)
log.addHandler(loghandler)


def main():
    """Find all unused variables."""
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('--debug', '-d', action='store_true', default=False)
    args = parser.parse_args()

    print('Finding unused variables...')
    found = 0

    # Walk the module tree
    for root, _, files in os.walk(args.path):
        # Skip .git and .terraform folders
        if '.git' in root or '.terraform' in root:
            continue
        log.info('Looking for Terraform files in %s', root)

        # Get all Terraform files
        terraform_files = [item for item in files if item.endswith('.tf')]
        log.info('Found files: %s', terraform_files)

        if terraform_files:
            defined_variables = []
            variables = []
            for terraform_file in terraform_files:
                log.info('Looking for variable definitions in %s',
                         terraform_file)
                path = '{}/{}'.format(root, terraform_file)
                with open(path, 'r') as stream:
                    data = stream.readlines()
                data = [line.strip() for line in data if line.strip()]
                for line in data:
                    if re.match(VARIABLE_DECL, line):
                        match = re.match(VARIABLE_DECL, line)
                        defined_variables.append(match.group(1))
                    elif re.search(VARIABLE, line):
                        match = re.findall(VARIABLE, line)
                        variables.extend(match)

            for variable in defined_variables:
                if variable not in variables:
                    log.warn('Found unused variable: %s', variable)
                    found = found + 1

    log.info('Finished looking for unused variables.')
    if found > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
