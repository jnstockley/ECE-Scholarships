'''
Several merging functions needed for combining dataframes.
'''
import pandas as pd
from fuzzywuzzy import fuzz
from src.models.imported_sheet import ImportedSheet

def combine_data(_alignment_columns, _aligned_row, _dfs: list[pd.DataFrame]):
    '''
    Test
    '''

def find_duplicates(alignment_columns: list[str], alignment_row_data, sheets: list[ImportedSheet]) -> dict[str, pd.DataFrame]:
    '''
    Given alignment columns to reference and a set of dataframes which contains one of the alignment columns
    and atleast one dataframe that has the alignment row data provided within its alignment_column, this will check
    to see if any other dataframes containing that alignment row data in their alignment column has duplicate columns with varing data
    and if so, return a dataframe with those conflict rows.

    Returns
    -------
    Maping of duplicate column name -> dataframe containing columns for the filename, and associated value
    '''
    # (filename, cut dataset)
    matches = []

    for sheet in sheets:
        data = sheet.get_df()
        for col in alignment_columns:
            if col in data.columns:
                if data[col].tolist().count(alignment_row_data) == 1:
                    matches.append((sheet.file_name, data.loc[data[col] == alignment_row_data,:]))
                    #match found for given sheet, no need to check other alignment_columns.
                    break

    # Key = the column name, value = dataframe with file names as columns and value being different value ?
    common_columns = {}

    while len(matches) > 1:
        duplicates = set.intersection(*[set(match[1].columns) for match in matches])
        # Drop df references with no more duplicates
        for match in list(matches):
            local_duplicates = set.intersection(duplicates, set(match[1].columns))

            if len(local_duplicates) == 0:
                matches.remove(match)

        for duplicate in duplicates:
            # filename: value
            values = {}
            for match_i, match in enumerate(matches):
                filename = match[0]
                data = match[1]
                values[filename] = data[duplicate].tolist()[0]
                matches[match_i] = (match[0], match[1].loc[:, match[1].columns != duplicate])

            if not len(set(pair[1] for pair in values.items())) == 1:
                # Set contains unique elements, so if set length >1, then there are 2 or more
                # datasets with different values for the duplicate column.
                common_columns[duplicate] = pd.DataFrame(values, index=['Values'])

    return common_columns

def replace_alignment_row_duplicate_column_value(alignment_value, duplicate_col_value, duplicate_column_name:str, alignment_columns: list[str], sheets: list[ImportedSheet]):
    '''
    Will find the row containing the alignment_value in each sheet, and replace its duplicate column value with duplicate_col_value
    '''
    for dataset in [sheet.get_df() for sheet in sheets]:
        for ali_column in alignment_columns:
            if ali_column in dataset.columns:
                dataset.loc[dataset[ali_column] == alignment_value, duplicate_column_name] = duplicate_col_value

def merge_with_alignment_columns(alignment_col_name: str, alignment_columns: list[str], new_alignment_col: pd.Series, sheets: list[ImportedSheet]):
    '''
    Combines alignment columns into a column labeled alignment_col_name and merges other row data
    to be in order of alignment column values.
    '''
    def build_row_dict():
        col_map = {
            f"{alignment_col_name}": align_row
        }

        for sheet in sheets:
            for col in alignment_columns:
                if col in sheet.get_df().columns and sheet.get_df()[col].tolist().count(align_row) == 1:
                    # Found alignment_column name for this df.
                    row_ref = sheet.get_df().loc[sheet.get_df()[col] == align_row, :]
                    for ref_col in row_ref.columns:
                        if ref_col not in alignment_columns:
                            col_map[ref_col] = row_ref[ref_col].tolist()[0]
                    break
        return col_map

    output_columns = set.union(*[set(sheet.get_df()) for sheet in sheets])
    output_columns = [alignment_col_name] + [col for col in output_columns if col not in alignment_columns]

    rows = []
    for align_row in new_alignment_col:
        col_map = build_row_dict()
        build_row = pd.DataFrame(col_map, columns=output_columns, index=[0])
        rows.append(build_row)

    return pd.concat(rows, ignore_index=True)

def combine_columns(columns: list[pd.Series], drop_missing: bool) -> pd.Series:
    '''
    Combine several column series into 1. If drop_missing is flagged then only the values
    present in each column will be kept in output.
    '''
    sets = [set(col) for col in columns]
    if drop_missing:
        common_rows = set.intersection(*sets)
        return pd.Series(list(common_rows))

    all_unique_rows = set.union(*sets)
    return pd.Series(list(all_unique_rows))

def find_similar_columns(columns: list[str], similarity: int) -> list[tuple[str, list[str]]]:
    '''
    Given a list of dataframes, finds columns similar between two or more
    Parameters
    ----------
        dfs : list[str]
            List of dataframes to merge.
        similarity : int
            Value 0 - 100. 100 is most similar, 0 is least similar.
    Returns
    -------
        List of tuples with first element being desired column name, and second element being list of
        similar column names
    '''
    # Each will have dict with key: score, parent: merge_columns key
    has_been_matched = {}
    # column: list of associated columns
    merge_similar_columns = {}

    for i, column in enumerate(columns):
        if i == len(columns) - 1:
            break

        similar_columns = [val for val in find_similarity_scores(
            column, columns[0:i] + columns[i+1:]) if val[1] >= similarity]
        if len(similar_columns) == 0:
            # No similar columns can be ignored
            continue

        valid_matches = []

        for match_details in similar_columns:
            compare_column = match_details[0]
            score = match_details[1]

            if compare_column in has_been_matched:
                prev_max_score = has_been_matched[compare_column]["score"]
                if score <= prev_max_score:
                    # Column should be merged with column it has most similarity to.
                    continue

                parent = has_been_matched[compare_column]["parent"]
                # This shouldn't be necessary? See if fixable
                if compare_column in merge_similar_columns[parent]:
                    merge_similar_columns[parent].remove(compare_column)

            if column in has_been_matched:
                if has_been_matched[column] and has_been_matched[column]["parent"] == compare_column:
                    continue

            valid_matches.append(compare_column)
            has_been_matched[compare_column] = {
                "score": score,
                "parent": column,
            }

        if len(valid_matches) > 0:
            merge_similar_columns[column] = valid_matches

    # add data column statistical comparison (see if values match up)

    return [item for item in merge_similar_columns.items() if len(item[1]) > 0]

def find_similarity_scores(name: str, columns: pd.DataFrame | list[str]) -> list[tuple[str, float]]:
    '''
    Takes a column name and checks the columns of a dataframe to rank them on similarity
    to the column name.
    Parameters
    ----------
    name : str
        Column name to find similarity to
    columns : pd.Dataframe
        Checks df columns and finds similarity score to name.
    Returns
    -------
        List of tuples with first value being the column name from df, and second value being the
        associated similarity with name input.
    '''
    if isinstance(columns, pd.DataFrame):
        columns = columns.columns

    return [(column, fuzz.token_sort_ratio(name, column)) for column in columns]
