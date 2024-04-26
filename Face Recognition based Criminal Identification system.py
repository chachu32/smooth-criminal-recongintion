import os
import cv2
import face_recognition
from tkinter import Tk, Label, Button, filedialog, simpledialog
import pygame

known_criminals_folder = r"C:\Users\91907\Desktop\smooth criminial\criminals"
known_encodings = []
known_names = []

pygame.init()

# Set the path to the default alert sound file and known criminals folder
default_alert_sound_path = r"C:\Users\91907\Desktop\smooth criminial\young-fly-on-the-track-made-with-Voicemod-technology (1).mp3"
alert_sound_path = default_alert_sound_path

# Load the default alert sound
alert_sound = pygame.mixer.Sound(alert_sound_path)

def load_known_criminals():
    for file_name in os.listdir(known_criminals_folder):
        image_path = os.path.join(known_criminals_folder, file_name)
        name = os.path.splitext(file_name)[0]
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)
        if len(encoding) > 0:
            known_encodings.extend(encoding)  # Allow multiple photos for the same criminal
            known_names.extend([name] * len(encoding))

def play_alert_sound():
    pygame.mixer.Channel(0).play(alert_sound)

def match_criminal():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"
            for match, known_name in zip(matches, known_names):
                if match:
                    name = known_name
                    break

            cv2.rectangle(frame, (left, top), (right, bottom), (237, 255, 32), 2)
            if name != "Unknown":
                play_alert_sound()  # Play alert sound only for known criminals
            cv2.putText(frame, f"{name}", (left - 40, top - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (158, 49, 255), 2)

        cv2.imshow('Criminal Identification System', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def add_criminal():
    file_paths = filedialog.askopenfilenames(initialdir="/", title="Select Image Files",
                                              filetypes=(("Image Files", "*.jpg;*.jpeg;*.png"), ("All Files", "*.*")))
    if file_paths:
        name = simpledialog.askstring("Criminal Name", "Enter the name of the criminal:")
        if name:
            for file_path in file_paths:
                image = face_recognition.load_image_file(file_path)
                encoding = face_recognition.face_encodings(image)
                if len(encoding) > 0:
                    known_encodings.extend(encoding)  # Allow multiple photos for the same criminal
                    known_names.extend([name] * len(encoding))
            print(f"Criminal '{name}' added successfully!")

def set_alert_sound_path():
    global alert_sound_path
    alert_sound_path = filedialog.askopenfilename(initialdir="/", title="Select Audio File",
                                                   filetypes=(("Audio Files", "*.wav;*.mp3"), ("All Files", "*.*")))
    if alert_sound_path:
        pygame.mixer.stop()  # Stop the current alert sound
        pygame.mixer.init()  # Initialize the mixer with the new alert sound
        alert_sound = pygame.mixer.Sound(alert_sound_path)
        print(f"Alert sound path set to: {alert_sound_path}")

load_known_criminals()

root = Tk()
root.title("Criminal Identification System")
root.geometry("500x300")

label = Label(root, text="Welcome to the Criminal Identification System ")
label.pack()

match_button = Button(root, text="Start Matching", command=match_criminal)
match_button.pack()

add_criminal_button = Button(root, text="Add Criminal", command=add_criminal)
add_criminal_button.pack()

root.mainloop()
