import sql
import cv2
from simple_facerec import SimpleFacerec
# Load Camera
def run(subject,date):
    cap = cv2.VideoCapture(0)
    # Encode faces from a folder
    sfr = SimpleFacerec()
    sfr.load_encoding_images("instance//images//")
    my_list=[]
    while True:
        ret, frame = cap.read()

        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
            if name not in my_list:
                my_list.append(name)
            

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    for i in my_list:
        if i=='Unknown':
            continue
        else:
            sql.create_data(subject,i,date)
    cv2.destroyAllWindows()
