import os
import sys
import logging
import argparse
import re
import glob

VARIABLE_DECL = r'^variable\s+\"([\w_]+)\"\s+{'
VARIABLE = r'var\.([\w_]+)'
found = 0

log = logging.getLogger(__name__)
log.setLevel(level=os.environ.get("LOGLEVEL", logging.INFO))
loghandler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(levelname)-4s %(message)s')
loghandler.setFormatter(formatter)
log.addHandler(loghandler)


def find_tf_files(path):
    glob_path = path + '/*.tf'
    log.debug('Globbing: {}'.format(glob_path))
    return glob.glob(glob_path, recursive=True)


def get_tf_directories(file_list):
    tf_dirs = list(
        set(
            [os.path.dirname(item) for item in file_list]
        )
    )

    log.debug('Terraform Directories: {}'.format(tf_dirs))
    return tf_dirs


def find_unused_vars(file_list):
    log.info('Finding unused variables...')
    # Dictionary of variable name => filename where it is defined
    defined_variables = {}
    variables = []
    for tf_file in file_list:
        log.info(
            'Looking for variable definitions in %s',
            tf_file
        )
        with open(tf_file, 'r') as stream:
            data = stream.readlines()
        data = [line.strip() for line in data if line.strip()]
        for line in data:
            if re.match(VARIABLE_DECL, line):
                match = re.match(VARIABLE_DECL, line)
                defined_variables[match.group(1)] = tf_file
            elif re.search(VARIABLE, line):
                match = re.findall(VARIABLE, line)
                variables.extend(match)
    log.debug('''Defined vars:
        {}
    '''.format(defined_variables))
    for variable in defined_variables:
        if variable not in variables:
            log.warn(
                '[%s] Found unused variable: %s',
                defined_variables[variable], variable
            )
            global found
            found = found + 1


def main():
    """Find all unused variables."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--quiet', '-q', action='store_true', default=False,
        help='Enable WARN only logging'
    )
    parser.add_argument(
        '--debug', '-d', action='store_true', default=False,
        help='Enable DEBUG logging'
    )
    parser.add_argument(
        'path', nargs='*', metavar='path', default=['./**'],
        help='Path of directory or files to scan (supports unix globbing)'
    )
    args = parser.parse_args()

    if args.quiet:
        log.setLevel(level=logging.WARN)

    if args.debug:
        log.setLevel(level=logging.DEBUG)

    log.info('Finding terraform directories...')
    tf_files = []
    for path in args.path:
        if os.path.isfile(path):
            tf_files += [path]
        else:
            tf_files += find_tf_files(path)

    if not tf_files:
        log.info('Could not find any terraform files in: {}'.format(args.path))
        sys.exit(0)

    tf_dirs = get_tf_directories(tf_files)

    for tf_dir in tf_dirs:
        log.info('Looking for Terraform files in %s', tf_dir)
        files_for_dir = find_tf_files(tf_dir)
        find_unused_vars(files_for_dir)
        log.info('Finished looking for unused variables.')

    global found
    if found > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
