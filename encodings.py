import face_recognition
import pickle 
import os
 
target_path = "./students_db/Photos/" 
students_encodings = list()
credentials = list()
for img in os.listdir(target_path):
    if img.endswith(".jpg") or img.endswith(".png"): # check for both jpg and png files
        image_path = os.path.join(target_path, img)
        image = face_recognition.load_image_file(image_path)
        print(image)
        print(type(image))
        encoding = face_recognition.face_encodings(image)[0]
        students_encodings.append(encoding)
        raw_name = (img.split(".")[0]).split("_")
        name = ""
        for _name in raw_name:
            name += _name
            name += " "
        
        credentials.append({
            "name": name
        })

print(students_encodings)
print(credentials)

with open("./students_db/Encodings/students_encodings.pkl", "wb") as file:
    pickle.dump(students_encodings, file)

with open("./students_db/Credentials/students_credentials.pkl", "wb") as file:
    pickle.dump(credentials, file)




