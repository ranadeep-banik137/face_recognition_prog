# from modules.face_identifier2 import encode_face
from modules.face_identifier import encode_face
from modules.database import insert_table_data, fetch_table_data_in_tuples
from modules.data_reader import read_file, convertToBinaryData


def run_app():
    encode_face(fetch_table_data_in_tuples())


def populate_database_with_local_config():
    for line in read_file():
        if 'id,name' in line:
            continue
        comma_separated_val = line.split(",")
        insert_table_data(int(comma_separated_val[0]), convertToBinaryData(f'img/{comma_separated_val[0]}.png'), comma_separated_val[1])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    populate_database_with_local_config()
    run_app()
