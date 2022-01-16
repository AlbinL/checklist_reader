from gtts import gTTS
from playsound import playsound
from dataclasses import dataclass
import speech_recognition as sr


@dataclass
class Item:
    name: str
    checked: bool = False

    def is_checked(self) -> bool:
        return self.checked


@dataclass
class Checklist:
    name: str
    items: list

    def addItem(self, item: str) -> None:
        if item not in self.items:
            self.items.append(item)


def say_phrase(phrase):
    language = 'en'
    myobj = gTTS(text=phrase, lang=language, slow=False)
    myobj.save("phrase.mp3")
    playsound("./phrase.mp3")


def await_check():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Sphinx
    try:
        phrase = r.recognize_sphinx(audio, keyword_entries=[("check", 1.0), ("no", 1.0)])
        print("Sphinx thinks you said " + phrase)

        return phrase

    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))


def run_checklist(checklist: Checklist):
    say_phrase("Running checklist: {0}".format(checklist.name))
    for item in checklist.items:
        say_phrase("{0}".format(item.name))
        phrase = await_check()
        print(phrase)
        if "check" in phrase:
            print("hello")
            item.checked = True
            say_phrase("{0} {1}".format(item.name, "checked"))


if __name__ == '__main__':
    checklist = Checklist("Work gym checklist", [Item("Shoes"), Item("Pants")])
    run_checklist(checklist)