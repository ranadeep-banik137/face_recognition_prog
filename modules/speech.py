import os
from gtts import gTTS
from playsound import playsound
from modules.database import fetch_table_data_in_tuples, populate_identification_record
from constants.db_constansts import query_data


def play_speech(input=''):
    # It is a text value that we want to convert to audio
    if input == 'None' or input is None or input == '':
        pass
    else:
        text_val = f'Sorry, I cannot identify your face currently. Please stand in front of the camera for a while' if input == 'Unknown Face' else f'Welcome {input}. I am AI robot identified your face and authenticated'
        print(f'User identified as {input}' if input != "Unknown Face" else '')
        # Here are converting in English Language
        language = 'en'

        # Passing the text and language to the engine,
        # here we have assign slow=False. Which denotes
        # the module that the transformed audio should
        # have a high speed
        obj = gTTS(text=text_val, lang=language, slow=False)

        # Here we are saving the transformed audio in a mp3 file
        obj.save("C:/Users/ranad/PycharmProjects/pythonProject/data/google_speech.mp3")

        # Play the exam.mp3 file
        try:
            if not is_user_already_identified(input):
                print(f'Playing audio for {input}' if input != "Unknown Face" else '')
                playsound("../pythonProject/data/google_speech.mp3")
        except Exception as err:
            error = err
            # print(err)
        finally:
            #time.sleep(1)
            os.remove('../pythonProject/data/google_speech.mp3')
            return True if input != 'Unknown Face' else False


def is_user_already_identified(name):
    bool_value = True
    if name == 'Unknown Face' or name == '' or name is None:
        return bool_value
    else:
        _id = fetch_table_data_in_tuples('', query_data.ID_FOR_NAME % name)[0][0]
        check = False
        try:
            fetch_table_data_in_tuples('', query_data.ALL_FOR_ID % _id)[0][0]
            check = True
        except Exception as err:
            print(f'ignore {err}')
        if check:
            is_valid_for_call = fetch_table_data_in_tuples('', query_data.IS_IDENTIFIED_FOR_ID % _id)[0][0]
            check = True if str(is_valid_for_call) == '1' else False
        bool_value = check
        return bool_value
