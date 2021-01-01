import rumps
import clipboard
from google_trans_new import google_translator
"""
To do:
* Revise languages to include a list of all MESA/Romance languages
"""
translator = google_translator()


class TranslateApp(object):
    def __init__(self):
        self.config = {
            "app_name": "Translate",
            "title": "ب",
            "interval": 1500
        }

        #self.interval = self.config["interval"]
        self.app = rumps.App(self.config["app_name"], self.config["title"])
        self.text_window = rumps.Window(default_text="", ok='Translate')
        self.text_window.icon = "icon.icns"
        self.translate_menu_button = rumps.MenuItem(title="Translate", callback=self.text_callback)
        self.clipboard_on_menu_button = rumps.MenuItem(title="Clipboard Translate On", callback=self.clipboard_on_callback)
        self.clipboard_off_menu_button = rumps.MenuItem(title="Clipboard Translate Off", callback=self.clipboard_off_callback)
        self.clipboard_timer = rumps.Timer(self.on_tick, 0.5)
        self.app.menu = [self.translate_menu_button, self.clipboard_on_menu_button, self.clipboard_off_menu_button]
        self.old_clipboard = ''
        self.arabic_alphabet_langs = ['ar', 'fa', 'ps', 'ku', 'ur', 'sd', 'pa', 'so', 'ug', 'kk']

    def run(self):
        self.app.run()

    def clipboard_on_callback(self, sender):
        self.clipboard_timer.start()

    def clipboard_off_callback(self, sender):
        self.clipboard_timer.stop()
        self.app.title = "ب"

    def on_tick(self, sender):
        current_clipboard = str(clipboard.paste())
        if current_clipboard != self.old_clipboard:
            self.app.title = self.translate_text(self, text=current_clipboard)
            self.old_clipboard = current_clipboard

    def translate_text(self, sender, text):
        # this one is slightly different for menu bar so it doesn't have the \n, maybe find a way to consolidate this
        input_source_lang = translator.detect(text)
        print(input_source_lang[1])
        if (input_source_lang[0]) in self.arabic_alphabet_langs:
            translation_en = translator.translate(text, lang_tgt="en", lang_src="ar")
            translation_es = translator.translate(text, lang_tgt="es", lang_src="ar")
            if type(translation_es) == list:
                translation_es = translation_es[0]
            translation_message = translation_en + " " + translation_es
        elif (input_source_lang[0]) == "es" or input_source_lang[0] == "fr":
            translation_en = translator.translate(text, lang_tgt="en", lang_src="es")
            translation_ar = translator.translate(text, lang_tgt="ar", lang_src="es")
            translation_message = translation_en + " " + translation_ar
        else:
            translation_es = translator.translate(text, lang_tgt="es", lang_src="en")
            if type(translation_es) == list:
                translation_es = translation_es[0]
            translation_ar = translator.translate(text, lang_tgt="ar", lang_src="en")
            translation_message = translation_es + " " + translation_ar
        return translation_message

    def text_callback(self, sender):
        self.request = str(self.text_window.run().text) #the run function returns the text and the button pressed
        input_source_lang = translator.detect(self.request)
        if (input_source_lang[0]) in self.arabic_alphabet_langs:
            translation_en = translator.translate(self.request, lang_tgt="en", lang_src="ar")
            translation_es = translator.translate(self.request, lang_tgt="es", lang_src="ar")
            if type(translation_es) == list:
                translation_es = translation_es[0]
            translation_message = self.request + "\n" + translation_en + "\n" + translation_es
        elif (input_source_lang[0]) == "es" or input_source_lang[0] == "fr":
            translation_en = translator.translate(self.request, lang_tgt="en", lang_src="es")
            translation_ar = translator.translate(self.request, lang_tgt="ar", lang_src="es")
            translation_message = self.request + "\n" + translation_en + "\n" + translation_ar
        else:
            translation_es = translator.translate(self.request, lang_tgt="es", lang_src="en")
            if type(translation_es) == list: #a fix for Spanish words being returned as a list if gendered.
                translation_es = translation_es[0]
            translation_ar = translator.translate(self.request, lang_tgt="ar", lang_src="en")
            translation_message = self.request + "\n" + translation_es + "\n" + translation_ar
        self.translation_alert = rumps.alert(str(translation_message))
        self.translation_alert()
        return self.request


if __name__ == '__main__':
    app = TranslateApp()
    app.run()
