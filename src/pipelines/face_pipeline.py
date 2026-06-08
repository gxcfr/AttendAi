import dlib 
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students

@st.cache_resource
def load_dlib_models():

    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(face_recognition_models.pose_predictor_model_location())

    
    facerec = dlib.face_recognition_model_v1(face_recognition_models.face_recognition_model_location())

    return detector, sp, facerec

def get_face_embedding(image_np):
    detector, sp, facerec = load_dlib_models()

    faces = detector(image_np, 1)

    encodings = []

    for face in faces:
        shape = sp(image_np, face)

        #128 embedding for the face
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)

        encodings.append(np.array(face_descriptor))

    return encodings

@st.cache_resource
def get_trained_model():
    X = []
    y = []

    students_db =   get_all_students()

    if not students_db:
        return None
    
    for student in students_db:
        embeddings = student.get('face_embeddings')
        if embeddings:
            X.append(np.array(embeddings))
            y.append(student.get('student_id'))

    if len(X) == 0:
        return None
        
    clf = SVC(kernel='linear', probability=True, class_weight='balanced')
    
    try:
        clf.fit(X,y)
    except ValueError:
        pass

    return {"clf": clf, "X": X, "y": y}


def trained_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()

    return bool(model_data)

def predict_attendance(class_image_np):
    encodings = get_face_embedding(class_image_np)

    detected_students = []

    model_data = get_trained_model()

    if model_data is None:
        st.warning("No student data available for recognition.")
        return detected_students, [], len(encodings)
    
    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:
        if len(all_students)>= 2:
            predicted_id = int(clf.predict([encoding]) [0])
        else:
            predicted_id = int(all_students[0])

        student_embeddings = [X_train[y_train.index(predicted_id)]]

        best_match_score = np.linalg.norm(student_embeddings - encoding, axis=1).min()

        resembling_threshold = 0.6

        if best_match_score < resembling_threshold:
            detected_students.append(predicted_id)    

    return detected_students, all_students, len(encodings)

        



    
