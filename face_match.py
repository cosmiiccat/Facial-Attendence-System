from datetime import datetime
import face_recognition
import numpy as np
import pickle
import cv2
import send_mail
import pyfirmata
import time

comport = 'COM3'
board = pyfirmata.Arduino(comport)
buzzer = board.get_pin('d:13:o')

video_capture = cv2.VideoCapture(0)

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
attendence_done = list()

with open("student_attendence.csv", "w") as sheet:
    sheet.write(f"Name, Date, Time\n")

    with open("./students_db/Encodings/students_encodings.pkl", "rb") as file:
        students_encodings = pickle.load(file)

        with open("./students_db/Credentials/students_credentials.pkl", "rb") as file:
            students_credentials = pickle.load(file)
            
            while True:
                _,frame = video_capture.read()
                small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
                rgb_small_frame = small_frame[:,:,::-1]
                if True:
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    for face_location in face_locations:
                        top, right, bottom, left = face_location
                        face_image = rgb_small_frame[top:bottom, left:right]
                        cv2.imwrite('test.jpg', face_image)
                        face_image = face_recognition.load_image_file("test.jpg")
                        face_encodings = face_recognition.face_encodings(face_image)
                        if len(face_encodings) > 0:
                            face_encoding = face_encodings[0]
                            matches = face_recognition.compare_faces(students_encodings, face_encoding)
                            face_distance = face_recognition.face_distance(students_encodings,face_encoding)
                            best_match_index = np.argmin(face_distance)
                            if matches[best_match_index] and best_match_index not in attendence_done:
                                name = students_credentials[best_match_index]["name"]
                                mail_id = students_credentials[best_match_index]["mail"]
                                current_time = now.strftime("%H-%M-%S")
                                cur_attend = f"{name}, {current_date}, {current_time}\n"
                                sheet.write(cur_attend)
                                send_mail.mail(mail_id,name)
                                attendence_done.append(best_match_index)
                                buzzer.write(1)
                                time.sleep(1)
                                buzzer.write(0)


                cv2.imshow("attendence system",frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

video_capture.release()
cv2.destroyAllWindows()

