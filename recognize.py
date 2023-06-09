import cv2
import face_recognition
import pickle
import numpy as np
import imutils

#Initialize the Raspberry Pi camera
cap = cv2.VideoCapture(0)

#Load the encoding file
print("Loading encoding file…")
file = open('EncodeFile.p’, 'rb')
encodeListKnownWithNames = pickle.load(file)
file.close()
encodeListKnown, nameList = encodeListKnownWithNames
print("Encoding file loaded")

#Store results
detection = False
person = None

while True:

Read a frame from the camera
success, frame = cap.read()

if not success:
continue

Resize the frame
frame = imutils.resize(frame, width=400)

Convert BGR to RGB
rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

Find face locations in the current frame
face_locations = face_recognition.face_locations(rgb_frame)
encode_curr_frame = face_recognition.face_encodings(rgb_frame, face_locations)

for encode_face, face_loc in zip(encode_curr_frame, face_locations):
# Compare encode_face unknown to encode_face known
matches = face_recognition.compare_faces(encodeListKnown, encode_face)

# The lower the distance the better the match
face_distances = face_recognition.face_distance(encodeListKnown, encode_face)

# Getting the index of the least value
match_index = np.argmin(face_distances)

if matches[match_index]:
    detection = "Known Face Detected"
    person = nameList[match_index]

    top, right, bottom, left = face_loc
    top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
    # Draw a rectangle around the face
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
else:
    detection = "No face detected"
Display the resulting frame
cv2.imshow("Frame", frame)

if cv2.waitKey(1) & 0xFF == ord('q'):
print("Status: {}".format(detection))
print("Person: {}".format(person))
break
#When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
