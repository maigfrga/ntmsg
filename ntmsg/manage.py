import os
import sys
import argparse

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(BASE_DIR, '../'))


def main():
    from flaskutils import init_app, execute_command
    description = 'Manage flask MIR application'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('command', help='command to execute')

    parser.add_argument(
        '--settings', help='config file path', default='config.test')

    args, extra_params = parser.parse_known_args()
    os.environ.setdefault('FLASKUTILS_SETTINGS_MODULE', args.settings)
    os.environ.setdefault('CHORD_EXTRACTOR_BASE_DIR', BASE_DIR)

    init_app(__name__, BASE_DIR)
    execute_command(args.command)


if __name__ == '__main__':
    main()
