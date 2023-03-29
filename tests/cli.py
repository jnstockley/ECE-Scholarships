'''
This script simplifies running the playwright and pyunit tests.
'''
import os
import signal
import time
import subprocess
import typer
from dotenv import dotenv_values

CONFIG = dotenv_values(".env")
if 'BROWSER' not in CONFIG:
    CONFIG['BROWSER'] = 'firefox'

CMD = {
    'STREAMLIT_RUN': 'streamlit run main.py --client.showErrorDetails false --server.port 9000 --server.headless true',
    'PLAYWRIGHT': f"pytest ./tests/feature/*.py --browser {CONFIG['BROWSER']}",
    'PYUNIT': 'unittest discover -s tests.unit -p "*.py"',
    'REPORT': 'poetry run coverage report && poetry run coverage html'
}

app = typer.Typer()

def start_streamlit_subprocess(coverage: bool = True):
    '''
    Launch the streamlit subprocess with or without coverage

    Parameters
    ----------
    coverage : bool, optional
        Whether to run the streamlit subprocess with coverage report, by default True
    '''
    print(f"Launching Streamlit Server with coverage: {coverage}")

    streamlit_cmd =f"poetry run coverage run --append --source src -m {CMD['STREAMLIT_RUN']}"
    if not coverage:
        streamlit_cmd =f"poetry run {CMD['STREAMLIT_RUN']}"

    # pylint: disable-next=subprocess-popen-preexec-fn,R1732
    process = subprocess.Popen(streamlit_cmd, shell=True, preexec_fn=os.setsid)

    # Give streamlit time to start
    time.sleep(5)
    return process

@app.command()
def run(test: str = 'all'):
    '''
    Main run command interface for cli
    '''
    if test == 'all':
        print('Running PyUnit tests:')
        poetry_pyunit_cmd =f"poetry run coverage run --source src -m {CMD['PYUNIT']}"
        subprocess.run(poetry_pyunit_cmd, check=False, shell=True)

        streamlit_process = start_streamlit_subprocess()

        try:
            subprocess.run(f"poetry run {CMD['PLAYWRIGHT']}", stderr=subprocess.STDOUT, check=True, shell=True)
        except subprocess.CalledProcessError as _exc:
            # Do no harm
            pass

        os.killpg(os.getpgid(streamlit_process.pid), signal.SIGTERM)

        print('COVERAGE REPORT:')
        subprocess.run(CMD['REPORT'], check= False, shell=True)
    elif test == 'playwright':
        streamlit_process = start_streamlit_subprocess(coverage = False)

        try:
            subprocess.run(f"poetry run {CMD['PLAYWRIGHT']}", stderr=subprocess.STDOUT, check=True, shell=True)
        except subprocess.CalledProcessError as _exec:
            # Do no harm
            pass

        os.killpg(os.getpgid(streamlit_process.pid), signal.SIGTERM)

    elif test == 'pyunit':
        print('Running PyUnit tests:')
        poetry_pyunit_cmd =f"poetry run python -m {CMD['PYUNIT']}"
        subprocess.run(poetry_pyunit_cmd, stderr=subprocess.STDOUT, check=True, shell=True)
    else:
        typer.echo('Invalid option, please pick from the following: [all/playwright/pyunit]')

if __name__ == "__main__":
    app(prog_name='cli')
