'''
This script simplifies running the playwright and pyunit tests.
'''
import time
import subprocess
import typer

CMD = {
    'STREAMLIT_RUN': 'streamlit run src/home.py --server.port 9000 --server.headless true',
    'PLAYWRIGHT': 'pytest ./tests/feature/playwright*.py',
    'PYUNIT': 'unittest discover -s tests.unit -p "*.py"',
    'REPORT': 'poetry run coverage report && poetry run coverage html'
}

app = typer.Typer()

@app.command()
def run(test: str = 'all'):
    '''
    Main run command interface for cli
    '''
    if test == 'all':
        print('Running PyUnit tests:')
        poetry_pyunit_cmd =f"poetry run coverage run --source src -m {CMD['PYUNIT']}"
        subprocess.run(poetry_pyunit_cmd, check=False, shell=True)

        print('Launcing Streamlit server')
        streamlit_cmd =f"poetry run coverage run --append --source src -m {CMD['STREAMLIT_RUN']}"
        # pylint: disable-next=consider-using-with
        streamlit_process = subprocess.Popen(streamlit_cmd, stdout=subprocess.PIPE, shell=True)

        time.sleep(4)
        subprocess.run(CMD['PLAYWRIGHT'], check=False, shell=True)

        streamlit_process.terminate()

        print('COVERAGE REPORT:')
        subprocess.run(CMD['REPORT'], check= False, shell=True)

if __name__ == "__main__":
    app(prog_name='cli')
