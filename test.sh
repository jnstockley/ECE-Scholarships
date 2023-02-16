#parallel -u ::: 'poetry run coverage run --source src -m streamlit run ./src/home.py' 'sleep 5 && poetry run pytest ./tests/feature/playwright*.py'
parallel -u ::: 'poetry run coverage run --source src -m unittest discover -s tests.unit -p "*.py" && poetry run coverage run --append --source src -m streamlit run ./src/home.py' 'sleep 5 && poetry run pytest ./tests/feature/playwright*.py'
