import cv2
import os
import re
import sys
import time
import datetime
import numpy as np
import face_recognition as fr
from modules.speech import play_speech
from modules.database import fetch_table_data_in_tuples, populate_identification_record, update_table, fetch_table_data
from modules.data_reader import convert_binary_to_img, remove_file
from constants.db_constansts import query_data, update_data, Tables
from modules.date_time_converter import convert_into_epoch


def encode_face(tuple_data=None):
    while True:
        update_valid_till_for_expired()
        input_video_src = 0 if os.getenv('CAMERA_INDEX') is None else os.getenv('CAMERA_INDEX')
        input_video_src = int(input_video_src) if re.fullmatch(r"\d+", str(input_video_src)) else input_video_src
        video_capture = cv2.VideoCapture(input_video_src or 0)
        name = None
        identified = None
        ret, frame = video_capture.read()
        if not (video_capture.isOpened() or frame or ret):
            encode_face()
        rgb_frame = frame[:, :, ::]
        face_locations = fr.face_locations(rgb_frame)
        face_encodings = fr.face_encodings(rgb_frame, face_locations)

        # for line in read_file():
        for row in tuple_data:
            IMG_BLOB = row[2]
            img = convert_binary_to_img(IMG_BLOB, f'{sys.path[1]}/data/test{row[0]}.jpg')
            input_image = fr.load_image_file(img)
            image_face_encoding = fr.face_encodings(input_image)[0]
            known_face_encoding = [image_face_encoding]
            known_face_names = [row[1]]

            for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = fr.compare_faces(known_face_encoding, face_encoding)

                default_name = 'Unknown Face'
                face_distances = fr.face_distance(known_face_encoding, face_encoding)
                match_index = np.argmin(face_distances)

                if matches[match_index]:
                    name = known_face_names[match_index]
                    identified = play_speech(name)
                    update_timer_for_user_in_background(name)
                else:
                    capture_unknown_face_img(frame)
                    name = default_name

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

                font = cv2.FONT_ITALIC

                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow('face detection', frame)
            remove_file(img)
            if identified:
                break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #play_speech(name)

        video_capture.release()
        # cv2.destroyAllWindows()


def update_timer_for_user_in_background(name, valid_for_seconds=os.getenv('VOICE_EXPIRY_SECONDS') or 30):
    current_time = time.time()
    timestamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
    valid_till_timestamp = datetime.datetime.fromtimestamp(int(current_time) + valid_for_seconds).strftime('%Y-%m-%d %H:%M:%S')
    _id = fetch_table_data_in_tuples('', query_data.ID_FOR_NAME % name)[0][0]
    check = False
    try:
        fetch_table_data_in_tuples('', query_data.ALL_FOR_ID % _id)[0][0]
        check = True
    except Exception as err:
        print(f'ignore {err}')
    if not check:
        populate_identification_record(_id, True, timestamp, valid_till_timestamp)
    elif not int(current_time) <= convert_into_epoch(str(fetch_table_data_in_tuples('', query_data.VALID_TILL_FOR_ID % _id)[0][0])):
        update_table(update_data.UPDATE_TIMESTAMP_WITH_IDENTIFIER % (0, valid_till_timestamp, _id))


def update_valid_till_for_expired():
    try:
        header, rows = fetch_table_data(Tables.IDENTIFICATION_RECORDS)
        for row in rows:
            update_table(update_data.UPDATE_BOOL_FOR_ID % (0 if int(time.time()) >= convert_into_epoch(str(row[3])) else 1, int(row[0])))
    except Exception as err:
        print(err)


def capture_unknown_face_img(frame, filepath=f'{sys.path[1]}/captured/'):
    file_name = re.sub("[^\w]", "_", datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    cv2.imwrite(f"{filepath}NewPicture_{file_name}.jpg", frame)
