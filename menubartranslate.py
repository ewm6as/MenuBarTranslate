import rumps
from google_trans_new import google_translator
"""
To do:
* Revise languages to include a list of all MESA/Romance languages
* Have it display from my clipboard in the top menu bar
* Maybe have a mac shortcut too?
"""
translator = google_translator()
class Translate_App(object):
    def __init__(self):
        self.config = {
            "app_name": "Translate",
            "icon": "ب",
            "interval": 1500
        }

        self.interval = self.config["interval"]
        self.app = rumps.App(self.config["app_name"], self.config["icon"])
        self.text_window = rumps.Window(default_text="", ok='Translate')
        self.text_window.icon = "icon.icns"
        #self.text_window.add_button("Done")
        self.translate_menu_button = rumps.MenuItem(title="Translate", callback=self.text_callback)
        self.app.menu = [self.translate_menu_button]
    def run(self):
        self.app.run()
    def text_callback(self, sender): #for whatever reason, I need sender in the function for the function to callback
        self.request = str(self.text_window.run().text) #the run function returns the text and the button pressed
        input_source_lang = translator.detect(self.request)
        print(input_source_lang[0])
        if (input_source_lang[0]) == "fa" or input_source_lang[0] == "ar": #change to if it's in the list of specified languages (and have a list of MESA languages
            #print("it's doing the if statement")
            translation_en = translator.translate(self.request, lang_tgt="en", lang_src="ar")
            translation_es = translator.translate(self.request, lang_tgt="es", lang_src="ar")
            translation_message = self.request + "\n" + translation_en + "\n" + translation_es
        elif (input_source_lang[0]) == "es" or input_source_lang[0] == "fr":
            #print("it's doing the elif statement")
            translation_en = translator.translate(self.request, lang_tgt="en", lang_src="es")
            translation_ar = translator.translate(self.request, lang_tgt="ar", lang_src="es")
            translation_message = self.request + "\n" + translation_en + "\n" + translation_ar
        else:
            #print("it's doing the else statement")
            translation_es = translator.translate(self.request, lang_tgt="es", lang_src="en")
            translation_ar = translator.translate(self.request, lang_tgt="ar", lang_src="en")
            translation_message = self.request + "\n" + translation_es + "\n" + translation_ar
        #self.translation_alert = rumps.alert(self.request + "\n" + translation_en + "\n" + translation_ar + "\n" + translation_es) #alert method (pop up box) # this works
        self.translation_alert = rumps.alert(translation_message)
        self.translation_alert()
        #self.translation_notification = rumps.notification(title="Translation", message=self.request)
        #self.translation_notification() this did not work (did not send notif)
        return self.request
if __name__ == '__main__':
    app = Translate_App()
    app.run()

