import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import pywhatkit
import wikipedia
import pyautogui

recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 175)

ques_ans = {"how are you": "i'm doing well, thanks for asking sir! ",
            "who are you": "i'm jarvis your virtual assistant. ",
            "who created you": "i was created by mr. ahmed."}


def talk(text):
    engine.say(text)
    engine.runAndWait()
    print(text)


def recognize_speech():
    try:
        with sr.Microphone() as source:
            print("Say something:")
            audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)
        text = text.lower()
        print("You asked:", text)
        command = text
        if command.lower().startswith("jarvis"):
            command = command[len("jarvis"):].strip()
            if "search" in command:
                query = command.replace("search", "").strip()
                talk("result based on search")
                search_url = f"https://www.google.com/search?q={query}"
                webbrowser.open(search_url)
            elif "play" in command:
                song = command.replace("play", "")
                talk("playing" + song)
                pywhatkit.playonyt(song).strip()
            elif "go to sleep" in command:
                talk("its good to assist you sir, call me whenever you need ")
                exit()
            elif "time now" in command:
                time = datetime.datetime.now().strftime("%I:%M %p")
                print(time)
                talk("its " + time + " now sir")
            elif "open" in command:
                pyautogui.press('super')
                pyautogui.press('Cortana Search')
                command = command.replace("open", "")
                pyautogui.typewrite(command)
                pyautogui.sleep(1)
                pyautogui.press("enter")
                talk("opening" + command + " sir")
            elif "close" in command:
                command = command.replace("close", "")
                talk("closing" + command)
                pyautogui.hotkey('alt', 'f4')
            elif command.lower().startswith("tell me"):
                query = command[len("tell me"):].strip()
                answer = ques_ans.get(query, "Sorry, I don't know the answer to that.")
                talk(answer)
            elif "what" in command or "who" in command:
                detail = command.replace("what", "").replace("who", "")
                try:
                    info = wikipedia.summary(detail, 1)
                    talk(info)
                except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError) as e:
                    if isinstance(e, wikipedia.exceptions.DisambiguationError):
                        talk(f"Multiple options found. Please provide a more specific query.")
                    else:
                        talk(f"Sorry, I couldn't find information on '{command}'. Can you ask something else?")
                except Exception as e:
                    talk(f"An error occurred: {str(e)}. Please try again.")
            else:
                talk("sorry i don't understand")

    except sr.UnknownValueError:
        engine.say("Sorry, could not understand audio.")
        engine.runAndWait()
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        engine.say(f"Could not request result from google speech recognition service. {e}")
        engine.runAndWait()
        print(f"Could not request result from google speech recognition service. {e}")


if __name__ == "__main__":
    talk("hi, i'm jarvis, your virtual assistant, how can i help you.")
while True:
    recognize_speech()
