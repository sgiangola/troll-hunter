import os
import pandas as pd
import sqlalchemy as sa

def main():
    '''Loads sqlite database with text samples within texts/ directory.'''
    # declare a list to collect our sample data
    text = []

    # recursively access the text directory and grab the contents of each file
    # and append them to the text list
    for file in os.scandir('texts'):
        with open(file.path, 'r') as f:
            text.append(f.read().splitlines()[0])

    # utilizing a pandas dataframe will allow simple insertion into the db
    # and allow optimal transformations, if necessary
    sample_text = pd.DataFrame({'samples' : text})

    # connect to db via sqlalchemy
    engine = sa.create_engine('sqlite:///local_db.db')

    # by using pandas handy to_sql text we can avoid having to
    # manually create insert statements
    sample_text.to_sql('sample_text', engine, if_exists='append')

if __name__ == '__main__':
    main()
