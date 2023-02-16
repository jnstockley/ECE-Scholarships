'''
This script simplifies running the playwright and pyunit tests.
'''
import time
import subprocess

CMD = {
    'STREAMLIT_RUN': 'streamlit run src/home.py --server.port 9000 --server.headless true',
    'PLAYWRIGHT': 'pytest ./tests/feature/playwright*.py',
    'PYUNIT': 'unittest discover -s tests.unit -p "*.py"',
    'REPORT': 'poetry run coverage report'
}

if __name__ == '__main__':
    print('Running PyUnit tests:')
    poetry_pyunit_cmd =f"poetry run coverage run --source src -m {CMD['PYUNIT']}"
    playwright_process = subprocess.run(poetry_pyunit_cmd, check=False, shell=True)

    print('Launcing Streamlit server')
    poetry_streamlit_cmd =f"poetry run coverage run --append --source src -m {CMD['STREAMLIT_RUN']}"
    # pylint: disable-next=consider-using-with
    streamlit_process = subprocess.Popen(poetry_streamlit_cmd, stdout=subprocess.PIPE, shell=True)

    time.sleep(3)
    playwright_process = subprocess.run(CMD['PLAYWRIGHT'], check=False, shell=True)

    streamlit_process.terminate()

    print('COVERAGE REPORT:')
    subprocess.run(CMD['REPORT'], check= False, shell=True)
