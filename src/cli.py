"""KBase Narrative Development CLI
You can set the log level with LOG_LEVEL

Usage:
  kbase-narrative serve
  kbase-narrative setup
  kbase-narrative update

Commands:
  serve        Start the Jupyter server
  setup        Install dependencies
  update       Update any code changes. Restart the Jupyter kernel after running this.

Options:
  -h --help    Show this screen.
"""

import os
import shutil
import tempfile
import logging
import subprocess
from docopt import docopt


logging.basicConfig(level=os.getenv('LOG_LEVEL', logging.WARNING))


def main():
    """Main entry-point function that gets called by the CLI."""
    args = docopt(__doc__, version='0.0.1', help=True)
    if args['serve']:
        serve()
    elif args['setup']:
        setup()
    elif args['update']:
        update()
    exit(0)


def serve():
    """Run the main Jupyter server."""
    _check_env()
    base_dir = _setup_env()
    logging.debug('Copying the config.json file into the extension directory')
    # Copy the config.json file into /kbase-extension/static/kbase/config/config.json
    shutil.copy2(
        os.path.join(base_dir, 'src', 'config.json'),
        os.path.join(base_dir, 'kbase-extension', 'static', 'kbase', 'config')
    )
    logging.debug('Starting the Jupyter server')
    command = ['jupyter', 'notebook', '--NotebookApp.base_url=/narrative']
    try:
        proc = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        proc.wait()
    except Exception as e:
        print('proc', dir(e))
        print('proc', e)
        print('proc', e.cmd)
        print('proc', e.message)


def update():
    """Update the app for any code changes."""
    logging.info('Installing pip dependencies')
    subprocess.check_call(['pip', 'install', '-e', 'src'])
    logging.info('Finished installing pip dependencies')


def setup():
    """Install all initial dependencies."""
    if not os.getenv('CONDA_DEFAULT_ENV') and not os.getenv('VIRTUAL_ENV'):
        logging.error('Please activate a Conda or Virtualenv environment berfore installing.')
        logging.error('Eg: source activate kbase-narrative')
        exit(1)
    logging.info('Installing Javascript dependencies')
    subprocess.check_call(['pip', 'install', '-e', 'src'])
    subprocess.check_call(['npm', 'install'])
    subprocess.check_call(['npm', 'run', 'bower'])  # bower install
    logging.info('Finished installing Javascript dependencies')
    base_dir = _setup_env()
    extension_names = [
        'viewCell', 'outputCell', 'dataCell', 'editorCell',
        'appCell2', 'advancedViewCell', 'codeCell'
    ]
    logging.info('Installing Jupyter notebook extensions (in /nbextensions)')
    for ext_name in extension_names:
        ext_dir = os.path.join(base_dir, 'nbextensions', ext_name)
        subprocess.check_call([
            'jupyter', 'nbextension',
            'install', ext_dir,
            '--symlink', '--sys-prefix'
        ])
        subprocess.check_call([
            'jupyter', 'nbextension',
            'enable', ext_name + '/main',
            '--sys-prefix'
        ])
    subprocess.check_call([
        'jupyter', 'nbextension', 'enable',
        '--py', '--sys-prefix',
        'widgetsnbextension'
    ])
    logging.info('Finished installing Jupyter extensions')
    exit(0)


def _check_env():
    """
    Make sure that a virtualenv is activated before doing any setup, installation, or serving.

    Logs and exits if there is no active env.
    """
    if not os.getenv('CONDA_DEFAULT_ENV') and not os.getenv('VIRTUAL_ENV'):
        logging.error('Please activate a Conda or Virtualenv environment berfore installing.')
        logging.error('Eg: source activate kbase-narrative')
        exit(1)


def _setup_env():
    """
    Set up all the environment variables that we need to run Jupyter.

    Returns the base directory of the project.
    """
    logging.info('Setting up Jupyter environment variables')
    dir_name = os.path.dirname(__file__)
    base_dir = os.path.abspath(os.path.join(dir_name, '..'))
    os.environ['NARRATIVE_DIR'] = base_dir
    os.environ['JUPYTER_CONFIG_DIR'] = os.path.join(base_dir, 'kbase-extension')
    os.environ['JUPYTER_RUNTIME_DIR'] = tempfile.mkdtemp()
    os.environ['JUPYTER_DATA_DIR'] = tempfile.mkdtemp()
    os.environ['JUPYTER_PATH'] = os.path.join(base_dir, 'kbase-extension')
    os.environ['IPYTHONDIR'] = os.path.join(base_dir, 'kbase-extension/ipython')
    return base_dir
