import rumps
import clipboard
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
            "title": "كلب",
            "interval": 1500
        }

        self.interval = self.config["interval"]
        self.app = rumps.App(self.config["app_name"], self.config["title"])
        self.text_window = rumps.Window(default_text="", ok='Translate')
        self.text_window.icon = "icon.icns"
        self.translate_menu_button = rumps.MenuItem(title="Translate", callback=self.text_callback)
        self.clipboard_on_menu_button = rumps.MenuItem(title="Clipboard Translate On", callback=self.clipboard_on_callback)
        self.clipboard_off_menu_button = rumps.MenuItem(title="Clipboard Translate Off", callback=self.clipboard_off_callback)
        self.clipboard_timer = rumps.Timer(self.on_tick, 2)
        self.app.menu = [self.translate_menu_button, self.clipboard_on_menu_button, self.clipboard_off_menu_button]
        self.old_clipboard = ''
    def run(self):
        self.app.run()
    def clipboard_on_callback(self, sender):
        self.clipboard_timer.start()
    def clipboard_off_callback(self, sender):
        self.clipboard_timer.stop()

    def on_tick(self, sender):
        current_clipboard = str(clipboard.paste())
        if current_clipboard != self.old_clipboard:
            self.app.title = self.translate_text(self, text=current_clipboard)
            self.old_clipboard = current_clipboard
    def translate_text(self, sender, text):
        # this one is slightly different for menu bar so it doesn't have the \n, maybe find a way to consolidate this
        input_source_lang = translator.detect(text)
        if (input_source_lang[0]) == "fa" or input_source_lang[0] == "ar": #change to if it's in the list of specified languages (and have a list of MESA languages
            #print("it's doing the if statement")
            translation_en = translator.translate(text, lang_tgt="en", lang_src="ar")
            translation_es = translator.translate(text, lang_tgt="es", lang_src="ar")
            if type(translation_es) == list:
                translation_es = translation_es[0]
            translation_message = translation_en + " " + translation_es
        elif (input_source_lang[0]) == "es" or input_source_lang[0] == "fr":
            #print("it's doing the elif statement")
            translation_en = translator.translate(text, lang_tgt="en", lang_src="es")
            translation_ar = translator.translate(text, lang_tgt="ar", lang_src="es")
            translation_message = translation_en + " " + translation_ar
        else:
            #print("it's doing the else statement")
            translation_es = translator.translate(text, lang_tgt="es", lang_src="en")
            if type(translation_es) == list:
                translation_es = translation_es[0]
            translation_ar = translator.translate(text, lang_tgt="ar", lang_src="en")
            translation_message = translation_es + " " + translation_ar
        return translation_message


    def text_callback(self, sender): #for whatever reason, I need sender in the function for the function to callback
        self.request = str(self.text_window.run().text) #the run function returns the text and the button pressed
        input_source_lang = translator.detect(self.request)
        #print(input_source_lang[0]) #to test what language it's detecting it as
        if (input_source_lang[0]) == "fa" or input_source_lang[0] == "ar": #change to if it's in the list of specified languages (and have a list of MESA languages
            #print("it's doing the if statement")
            translation_en = translator.translate(self.request, lang_tgt="en", lang_src="ar")
            translation_es = translator.translate(self.request, lang_tgt="es", lang_src="ar")
            if type(translation_es) == list:
                translation_es = translation_es[0]
            translation_message = self.request + "\n" + translation_en + "\n" + translation_es
        elif (input_source_lang[0]) == "es" or input_source_lang[0] == "fr":
            #print("it's doing the elif statement")
            translation_en = translator.translate(self.request, lang_tgt="en", lang_src="es")
            translation_ar = translator.translate(self.request, lang_tgt="ar", lang_src="es")
            translation_message = self.request + "\n" + translation_en + "\n" + translation_ar
        else:
            #print("it's doing the else statement")
            translation_es = translator.translate(self.request, lang_tgt="es", lang_src="en")
            if type(translation_es) == list: #a fix for Spanish words being returned as a list if gendered.
                translation_es = translation_es[0]
            translation_ar = translator.translate(self.request, lang_tgt="ar", lang_src="en")
            translation_message = self.request + "\n" + translation_es + "\n" + translation_ar
            #print(translation_message)
        self.translation_alert = rumps.alert(str(translation_message))
        self.translation_alert()
        #self.translation_notification = rumps.notification(title="Translation", message=self.request)
        #self.translation_notification() this did not work (did not send notif)
        return self.request
if __name__ == '__main__':
    app = Translate_App()
    app.run()
