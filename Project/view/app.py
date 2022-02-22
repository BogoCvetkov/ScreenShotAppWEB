import time
import os, sys
from kivy.resources import resource_add_path, resource_find
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from Project.model.pages_model import Model
from Project.legacy.controller import CaptureBot
from kivy.config import Config


"""
This is the main module used for managing the Graphical Interface (GUI). It is based on the kivy framework
It connects the User interface of the app with the controller module and it's CaptureBot class
"""

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('kivy','window_icon','resources/icons/1260673.png')
Config.write()

Builder.load_file("capture_menu.kv")
Builder.load_file("database.kv")
Builder.load_file("add_page.kv")
Builder.load_file("fast_flow.kv")


class MainMenuScreen(Screen):
    pass


class CaptureMenuScreen(Screen):
    
    pages_list = set()
    added_pages = ObjectProperty(None)

    def add_to_list(self):
        id = self.ids.id.text
        page = self.ids.page_name.text
        if id and page:
            check_id = self._check_id_input(input=id)
            if check_id:
                id = int(id)
                if len(self.pages_list)>0:
                    id_list = [id[1] for id in self.pages_list]
                    if id in id_list:
                        self.ids.scroll_two.text = "ID Already Added"
                        return None

                page_id = (page,id)
                self._add_page_button(page, id)
                self.pages_list.add(page_id)
                self._log_color("black")
                self.ids.scroll_two.text = "Added to List"

                print(page_id)
                print(self.pages_list)
        else:
            self.ids.scroll_two.text = "Must Fill Both Fields"

    def add_from_db(self):
        all_pages=Model.get_all_pages()
        all_pages = [page[1:] for page in all_pages ]
        for page in all_pages:
            self._add_page_button(page_name=page[0],
                                  page_id=page[1])
            self.pages_list.add(page)
        print(all_pages)

    def remove_button(self,btn):
        btn_id=int(btn.id)

        for item in self.pages_list:
            if btn_id in item:
                page = item
        self.pages_list.discard(page)
        self.added_pages.remove_widget(btn)
        print(self.pages_list)

    def clear_list(self):
        self.pages_list.clear()
        self.added_pages.clear_widgets()

    def capture_pages(self):
        check_options = self._check_options()
        if check_options:
            country = self.ids.country.text
            scrolls = int(self.ids.scroll.text)
            if len(self.pages_list)>0:
                self._log_color("black")
                self.ids.scroll_two.text = "Started Capturing...."
                pages=list(self.pages_list)
                res = CaptureBot.capture_pages(pages=pages,
                                               country=country,
                                               scrolls=scrolls)
                self.clear_list()
                self.ids.scroll_two.text = res
            else:
                self.ids.scroll_two.text = "Add a Page First"

    def capture_keyword(self):
        check_1 = self._check_keyword()
        check_2 = self._check_options_key()
        if check_1 and check_2 :
            country = self.ids.key_country.text
            scrolls = int(self.ids.key_scroll.text)
            keyword = str(self.ids.keyword.text)
            res = CaptureBot.capture_keyword(keyword=keyword,
                                                  country=country,
                                                  scrolls=scrolls)
            self._log_color("black")
            self.ids.scroll_two.text = res
            print(keyword)

    def convert_to_pdf(self):
        quality = int(self.ids.quality.text)
        if self.ids.folder.text == "":
            folder = None
            default = True
        else:
            folder = self.ids.folder.text
            default = False
            print(folder)
        try:
            res = CaptureBot.to_pdf(default=default,
                              quality=quality,
                              specify_folder=folder)
            self._log_color("black")
            self.ids.scroll_two.text = res[0]
            return res
        except:
            self.ids.scroll_two.text = res[0]
    
    def convert_send(self):
        res = self.convert_to_pdf()
        time.sleep(1)
        if res:
            try:
                CaptureBot.send_email(file=res[1])
                self._log_color("black")
                self.ids.scroll_two.text = "Email Sent"
            except:
                self._log_color("red")
                self.ids.scroll_two.text = "Email Failed"

    # Private methods used inside of the other methods
    def _add_page_button(self,page_name,page_id):
        page_button = Factory.ListButton(text=f"{page_name}")
        id_list = [id[1] for id in self.pages_list]
        if page_id not in id_list:
            page_button.id = page_id
            page_button.bind(on_press=self.remove_button)
            self.added_pages.add_widget(page_button)

    # Validating options chosen
    def _check_options(self):
        if self.ids.scroll.text == "Scrolls" or self.ids.country.text == "Country":
            self._log_color("red")
            self.ids.scroll_two.text = "Choose Scroll and Country Option"
            return False
        else:
            return True

    # Validating used for the same things but connected to another widget
    def _check_options_key(self):
        if self.ids.key_scroll.text == "Scrolls" or self.ids.key_country.text == "Country":
            self._log_color("red")
            self.ids.scroll_two.text = "Choose Scroll and Country Option"
            return False
        else:
            return True
    
    def _check_keyword(self):
        if self.ids.keyword.text == "":
            self._log_color("red")
            self.ids.scroll_two.text = "Enter a Keyword"
            return False
        else:
            return True

    def _check_id_input(self,input):
        if not input.isnumeric():
            self._log_color("red")
            self.ids.scroll_two.text = "Please Enter Only Numbers in the ID Field"
            return False
        else:
            return True

    def _check_quality(self):
        if self.ids.keyword.text == "":
            self._log_color("red")
            self.ids.scroll_two.text = "Choose quality percent"
            return False
        else:
            return True

    # Changing console message color
    def _log_color(self,color):
        if color == "red":
            self.ids.scroll_two.color = (1, 0, 0, 0.7)
        else:
            self.ids.scroll_two.color = (0, 0, 0, 0.7)


class DataBaseScreen(Screen):
    

    def add_email(self):
        check = self._check_field()
        if check:
            self.ids.profile_log.text = ""
            email = self.ids.user_email.text
            body = self.ids.email_body.text
            res = CaptureBot.insert_user_to_db(email=email,
                                         email_body=body)
            self._log_color("black")
            self.ids.profile_log.text = res

    def _check_field(self):
        if self.ids.user_email.text == "" or self.ids.email_body.text == "":
            self._log_color("red")
            self.ids.profile_log.text = "Please fill Email and Default Body Fields"
            return False
        else:
            return True

    def _log_color(self,color):
        if color == "red":
            self.ids.profile_log.color = (1, 0, 0, 0.7)
        else:
            self.ids.profile_log.color = (0, 0, 0, 0.8)


class AddPagesScreen(Screen):

    def add_page(self):
        check = self._check_field()
        if check:
            id = self.ids.add_page_id.text
            page = self.ids.add_page_n.text
            check_id = self._check_id_input(input=id)
            if check_id:
                id = int(id)
                res = CaptureBot.insert_page_to_db(page_id=id,
                                                   page_name=page)
                self.ids.db_log.text = res
    
    def find_page(self):
        page_name = self.ids.find_page.text
        res = CaptureBot.find_page(page_name=page_name)
        output_text = ""
        for page in res:
            output_text += f"{page}\n"
        self.ids.db_console.text = output_text

    def delete_all(self):
        res = CaptureBot.delete_all_pages()
        self._log_color("black")
        self.ids.db_log.text = res

    def remove_page(self):
        id = self.ids.remove_page.text
        check_id = self._check_id_input(input=id)
        if check_id:
            id = int(id)
            res = CaptureBot.delete_page(page_id=id)
            self._log_color("black")
            self.ids.db_log.text = res

    def _check_field(self):
        if self.ids.add_page_n.text == "" or self.ids.add_page_id.text == "":
            self._log_color("red")
            self.ids.db_log.text = "Please fill Both Fields"
            return False
        else:
            return True

    def _check_id_input(self,input):
        if not input.isnumeric():
            self._log_color("red")
            self.ids.db_log.text = "Please Enter Only Numbers in the ID Field"
            return False
        else:
            return True

    def _log_color(self,color):
        if color == "red":
            self.ids.db_log.color = (1, 0, 0, 0.7)
        else:
            self.ids.db_log.color = (0, 0, 0, 0.7)


class FastFlowScreen(Screen):

    def fast_capture(self):
        page_num = len(Model.get_all_pages())
        res = CaptureBot.capture_from_database()
        self.ids.scroll_text.text = res
        if page_num <= 7:
            quality = 90
        elif 7 < page_num <= 14:
            quality = 80
        elif 14 < page_num <= 21:
            quality = 70
        elif page_num > 21:
            quality = 60
        res = CaptureBot.to_pdf(quality=quality)
        try:
            CaptureBot.send_email(file=res[1])
            self.ids.sent_label.text = "EMAIL SENT"
        except:
            self.ids.sent_label.color = (1,0,0,0.7)
            self.ids.sent_label.text = "EMAIL FAILED"


class ScreenSwitch(ScreenManager):
    pass


class XBotApp(App):
    def build(self):
        Window.clearcolor = (247/255,247/255,247/255,1)
        return ScreenSwitch()


if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    XBotApp().run()