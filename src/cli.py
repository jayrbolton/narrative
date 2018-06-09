"""KBase Narrative Development CLI

Usage:
  kbase-narrative serve

Options:
  -h --help    Show this screen.
"""
import subprocess
import os
import shutil
from docopt import docopt


def main():
    args = docopt(__doc__, version='0.0.1', help=True)
    if args['serve']:
        serve()


def serve():
    dir_name = os.path.dirname(__file__)
    base_dir = os.path.abspath(os.path.join(dir_name, '..'))
    os.environ['NARRATIVE_DIR'] = base_dir
    os.environ['JUPYTER_CONFIG_DIR'] = os.path.join(base_dir, 'kbase-extension')
    os.environ['JUPYTER_RUNTIME_DIR'] = os.path.join('/tmp', 'jupyter_runtime')
    os.environ['JUPYTER_DATA_DIR'] = os.path.join('/tmp', 'jupyter_data')
    os.environ['JUPYTER_PATH'] = os.path.join(base_dir, 'kbase-extension')
    os.environ['IPYTHONDIR'] = os.path.join(base_dir, 'kbase-extension/ipython')
    os.environ['IPYTHONDIR'] = os.path.join(base_dir, 'kbase-extension/ipython')
    # Copy the config.json file into /kbase-extension/static/kbase/config/config.json
    shutil.copy2(
        os.path.join(base_dir, 'src', 'config.json'),
        os.path.join(base_dir, 'kbase-extension', 'static', 'kbase', 'config')
    )
    proc = subprocess.Popen([
        'jupyter',
        'notebook',
        '--NotebookApp.base_url=/narrative'
    ])
    proc.wait()
