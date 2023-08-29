import cv2
import sys
import os
import datetime
import numpy as np
import face_recognition as fr
from modules.face_identifier import encode_face, update_timer_for_user_in_background
from modules.database import insert_table_data, fetch_table_data_in_tuples
from modules.data_reader import convert_binary_to_img, read_file, convertToBinaryData, get_available_image
from modules.exportdb import export_db_to_excel, export_excel_to_json, export_db_to_json
from modules.date_time_converter import convert_into_epoch

def run_app():
    cascPath = sys.argv[1]
    faceCascade = cv2.CascadeClassifier(cascPath)

    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

def run():
    input_image = fr.load_image_file('../img/1.png')
    image_face_encoding = fr.face_encodings(input_image)[0]
    known_face_encoding = [image_face_encoding]
    known_face_names = ['Ranadeep Banik']
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()

        rgb_frame = frame[:, :, ::]
        face_locations = fr.face_locations(rgb_frame)
        face_encodings = fr.face_encodings(rgb_frame, face_locations)

        for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_face_encoding, face_encoding)

            default_name = 'Unknown Face'

            face_distances = fr.face_distance(known_face_encoding, face_encoding)
            match_index = np.argmin(face_distances)

            if matches[match_index]:
                name = known_face_names[match_index]
            else:
                name = default_name

            #play_speech(name)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

            font = cv2.FONT_ITALIC

            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('face detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    export_db_to_excel('users')
    json_body = export_excel_to_json('users.xlsx')
    for node in json_body:
        test = node['userImg']
        encoded = test.encode('ISO-8859-1')
        #Testing if encoding works
        #convert_binary_to_img(encoded, f'data/test{node["userID"]}.jpg')
    print(json_body)
    #run_app()
    #get_available_image(comma_separated_val[0])
    for line in read_file():
        if 'id,name' in line:
            continue
        comma_separated_val = line.split(",")
        insert_table_data(int(comma_separated_val[0]), convertToBinaryData(f'img/{comma_separated_val[0]}.png'), comma_separated_val[1])
    db_to_json = export_db_to_json('users')
    #for node in db_to_json:
        #test = node['userImg']
        #encoded = test.encode('ISO-8859-1')
        # Testing if encoding works
        #convert_binary_to_img(encoded, f'../pythonProject/data/test{node["userID"]}.jpg')
    for row in fetch_table_data_in_tuples():
        #convert_binary_to_img(row[2], f'data/{row[0]}.jpg')
        IMG_BLOB = row[2]
        decoded = IMG_BLOB.decode('ISO-8859-1')
        #Testing if encoding works
        convert_binary_to_img(decoded.encode('ISO-8859-1'), f'../pythonProject/data/test{row[0]}.jpg')
    ROOT_DIR = os.path.abspath(os.curdir)
    print(ROOT_DIR)
    test = convert_into_epoch('2023-08-28 21:28:35')
    encode_face(fetch_table_data_in_tuples())
    #update_timer_for_user_in_background('Ranadeep Banik', 100)
