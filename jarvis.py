import os
import threading
import time
import datetime
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import customtkinter as ctk

# -------------------- Setup --------------------
GEMINI_API_KEY = "AIzaSyBkSROsLKINloe0DMsTSpDK4DEJU3z05nw"  # <-- put your key here
genai.configure(api_key=GEMINI_API_KEY)

engine = pyttsx3.init()
recognizer = sr.Recognizer()

# -------------------- Voice Functions --------------------
def speak(text):
    """Convert text to speech + print in console"""
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    """Listen from microphone and convert speech to text"""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None

def ask_jarvis(question):
    """Send user query to Gemini model"""
    if not question:
        return "I didn't catch that. Please try again."

    model_name = "gemini-2.0-flash"  # ✅ working model
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return "I'm having trouble connecting to my intelligence core right now."

# -------------------- GUI Class --------------------
class JarvisApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("J.A.R.V.I.S.")
        self.geometry("800x500")
        self.resizable(False, False)

        # Dark futuristic theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Title label
        self.label_title = ctk.CTkLabel(
            self,
            text="J.A.R.V.I.S. ONLINE",
            font=("Consolas", 28, "bold"),
            text_color="cyan"
        )
        self.label_title.pack(pady=20)

        # Conversation box
        self.textbox = ctk.CTkTextbox(
            self,
            width=750,
            height=350,
            font=("Consolas", 14),
            text_color="white"
        )
        self.textbox.pack(pady=10)

        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="Initializing systems...",
            font=("Consolas", 16),
            text_color="lightblue"
        )
        self.status_label.pack(pady=10)

        # Start Jarvis thread
        threading.Thread(target=self.run_jarvis, daemon=True).start()

    def run_jarvis(self):
        """Main loop running Jarvis inside a background thread"""

        # --- Dynamic Greeting ---
        hour = datetime.datetime.now().hour
        if hour < 12:
            greeting = "Good morning, sir."
        elif hour < 18:
            greeting = "Good afternoon, sir."
        else:
            greeting = "Good evening, sir."

        startup_lines = [
            greeting,
            "All systems have been booted successfully.",
            "Power levels are at one hundred percent.",
            "Jarvis is now online and ready for your command."
        ]

        for line in startup_lines:
            self.update_text(f"Jarvis: {line}\n")
            speak(line)
            time.sleep(1.5)  # small pause between lines

        self.status_label.configure(text="Listening...")

        # --- Main Listening Loop ---
        while True:
            command = listen_for_command()
            if command:
                self.update_text(f"You: {command}\n")

                if any(x in command for x in ["exit", "stop", "goodbye"]):
                    goodbye = "Deactivating systems. Goodbye!"
                    self.update_text(f"Jarvis: {goodbye}\n")
                    speak(goodbye)
                    break

                answer = ask_jarvis(command)
                self.update_text(f"Jarvis: {answer}\n")
                speak(answer)

    def update_text(self, msg):
        """Update GUI text area with new messages"""
        self.textbox.insert("end", msg)
        self.textbox.see("end")

# -------------------- Run --------------------
if __name__ == "__main__":
    app = JarvisApp()
    app.mainloop()
