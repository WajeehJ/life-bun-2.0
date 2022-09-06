from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivymd.uix. floatlayout import MDFloatLayout
from kivymd.uix. behaviors import FakeRectangularElevationBehavior
from kivy.core.window import Window
import mysql.connector
#Window.size = (300, 500)
from kivymd.uix.label import MDLabel

Window.size = (350, 600)

class LoginScreen(Screen):

    user_id = 0

    def LoginButton(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="wajeeh786",
            database="life_bun"
        )

        c = mydb.cursor()

        inputted_username = (self.ids.user.text,)
        inputted_password = (self.ids.password.text,)
        sqlcommand = "SELECT password FROM users WHERE username = (%s)"
        c.execute(sqlcommand, inputted_username)
        correct_password = c.fetchall()
        sqlcommand = "SELECT id from users where username = (%s)"
        c.execute(sqlcommand, inputted_username)
        self.user_id = c.fetchall()



        if inputted_password == correct_password[0]:
            self.parent.current = "home"
            self.ids.user.text = ""
            self.ids.password.text = ""
        else:
            self.ids.welcome_label.text = "WRONG!!!!"
            self.ids.user.text = ""
            self.ids.password.text = ""


        mydb.commit()

        mydb.close()

    def getUserId(self):
        return self.user_id


class SignUpScreen(Screen):
    user_id = 0
    def create_user(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="wajeeh786",
            database="life_bun"
        )
        c = mydb.cursor();
        sqlcommand0 = "SELECT id FROM users WHERE username = (%s)"
        values0 = (self.ids.user.text,)
        c.execute(sqlcommand0, values0)
        taken_user = c.fetchall()
        if not taken_user:
            taken_user_status = False
        else:
            taken_user_status = True


        if ' ' in self.ids.user.text:
            self.ids.welcome_label.text = "No spaces in username allowed"
            self.ids.user.text = ""
            self.ids.password.text = ""
            self.ids.phonenumber.text = ""
        elif taken_user_status:
            self.ids.welcome_label.text = "Username taken"
            self.ids.user.text = ""
            self.ids.password.text = ""
            self.ids.phonenumber.text = ""
        else:
            sqlcommand = "INSERT INTO users (username, password, timezone, bunny_health, money) VALUES (%s, %s, %s, %s, %s)"
            values = (self.ids.user.text, self.ids.password.text, self.ids.time_zone.text, 20, 50)
            c.execute(sqlcommand, values)
            inputted_username = (self.ids.user.text,)
            sqlcommand = "SELECT id from users where username = (%s)"
            c.execute(sqlcommand, inputted_username)
            self.user_id = c.fetchall()
            self.ids.welcome_label.text = "Success"
            self.parent.current = "tutorialone"
            self.ids.user.text = ""
            self.ids.password.text = ""

        mydb.commit()

        mydb.close()

    def get_user_id(self):
        return self.user_id

class TutorialOne(Screen):
    def on_touch_move(self, touch):
        if touch.x < touch.ox:
            self.parent.current = "tutorialtwo"

class TutorialTwo(Screen):
    def on_touch_move(self, touch):
        if touch.x < touch.ox:
            self.parent.current = "customization"

class CustomizationScreen(Screen):
    def christmas(self):
        self.ids.bunny.source = "Images/christmas.png"

    def devil(self):
        self.ids.bunny.source = "Images/devil.png"

    def wedding(self):
        self.ids.bunny.source = "Images/wedding.png"

    def birthday(self):
        self.ids.bunny.source = "Images/birthday.png"

    def add_bunny(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="wajeeh786",
            database="life_bun"
        )
        c = mydb.cursor();
        id = self.parent.get_screen("signup").get_user_id()
        sqlcommand = "UPDATE users SET bunnylink = (%s) WHERE id = (%s)"
        c.execute(sqlcommand, (self.ids.bunny.source, id[0][0]))
        self.parent.current = "home"



        mydb.commit()

        mydb.close()

class HomeScreen(Screen):

    def on_touch_move(self, touch):
        if touch.x < touch.ox:
            self.parent.current = "main"

    def update_image(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="wajeeh786",
            database="life_bun"
        )
        c = mydb.cursor()
        id = self.parent.get_screen("login").getUserId()
        if not id:
            id = self.parent.get_screen("signup").get_user_id()
        sqlcommand = "SELECT bunnylink FROM users WHERE id = (%s)"
        values = (id[0][0],)
        c.execute(sqlcommand,values)
        link = c.fetchall()
        self.ids.bunny_pic.source = link[0][0]
        sqlcommand2 = "SELECT bunny_health FROM users WHERE id = (%s)"
        c.execute(sqlcommand2, values)
        health = c.fetchall()
        self.ids.health_bar.value = health[0][0]
        sqlcommand3 = "SELECT money FROM users WHERE id = (%s)"
        c.execute(sqlcommand3, values)
        money = c.fetchall()
        self.ids.money_bar.value = money[0][0]


        mydb.commit()

        mydb.close()

    def update_health_money(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="wajeeh786",
            database="life_bun"
        )
        c = mydb.cursor()
        id = self.parent.get_screen("login").getUserId()
        if not id:
            id = self.parent.get_screen("signup").get_user_id()
        sqlcommand = "UPDATE users SET bunny_health = (%s), money = (%s) WHERE id = (%s)"
        values = (self.ids.health_bar.value, self.ids.money_bar.value, id[0][0])
        c.execute(sqlcommand, values)

        mydb.commit()

        mydb.close()

    def feed(self):
        current = self.ids.money_bar.value
        health = self.ids.health_bar.value
        health += 10
        current -= 5
        self.ids.money_bar.value = current
        self.ids.health_bar.value = health
        self.update_health_money()
    def constant_health(self):
        Clock.schedule_interval(self.add_health, 120)
        self.update_health_money()
    def add_health(self, dt):
        health = self.ids.health_bar.value
        health -= 1
        self.ids.health_bar.value = health
        self.update_health_money()
    def show_bubbles(self, dt):
        self.ids.bubbles.opacity = 1
    def delete_bubbles(self, dt):
        self.ids.bubbles.opacity = 0
    def update_poop(self):
        if(self.ids.health_bar.value <= 20):
            self.ids.poop3.opacity = 1
        if(self.ids.health_bar.value <= 30):
            self.ids.poop2.opacity = 1
        if(self.ids.health_bar.value <= 40):
            self.ids.poop1.opacity = 1

    def take_bath(self):
        Clock.schedule_once(self.show_bubbles, .01)
        Clock.schedule_once(self.delete_bubbles, 1.5)
        current = self.ids.money_bar.value
        health = self.ids.health_bar.value
        current -= 10
        health += 20
        self.ids.money_bar.value = current
        self.ids.health_bar.value = health
        if(self.ids.health_bar.value > 40):
            self.ids.poop1.opacity = 0
        if(self.ids.health_bar.value > 30):
            self.ids.poop2.opacity = 0
        if(self.ids.health_bar.value > 20):
            self.ids.poop3.opacity = 0
        self.update_health_money()


class TodotaskCard(FakeRectangularElevationBehavior, MDFloatLayout):
    def completed_task(self, instance):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="wajeeh786",
            database="life_bun"
        )
        c = mydb.cursor()
        sqlcommand = "DELETE FROM tasks WHERE task_name = (%s)"
        values = (instance.ids.description.text,)
        c.execute(sqlcommand,values)
        self.parent.remove_widget(instance)
        mydb.commit()

        mydb.close()


class TodohabitCard(FakeRectangularElevationBehavior, MDFloatLayout):
    def completed_task(self, instance):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="wajeeh786",
            database="life_bun"
        )
        c = mydb.cursor()
        sqlcommand = "UPDATE habits SET completed_for_the_day = (%s) WHERE habit_name = (%s)"
        values = ("True", instance.ids.description.text)
        c.execute(sqlcommand, values)
        sqlcommand2 = "UPDATE habits SET days_completed = days_completed + 1 WHERE habit_name = (%s)"
        c.execute(sqlcommand2, (instance.ids.description.text,))

        self.parent.remove_widget(instance)
        mydb.commit()

        mydb.close()





class ToDoScreen(Screen):

    updated_screen = True
    task_number = 0
    habit_number = 0

    def on_touch_move(self, touch):
        if touch.x < touch.ox:
            self.parent.current = "habit"

    def update_screen(self):
        if self.updated_screen:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="wajeeh786",
                database="life_bun"
            )
            c = mydb.cursor()

            id = self.parent.get_screen("login").getUserId()
            if not id:
                id = self.parent.get_screen("signup").get_user_id()
            sqlcommand = ("SELECT task_name FROM tasks WHERE user_id = (%s)")
            values = (id[0][0],)
            c.execute(sqlcommand, values)
            the_tasks = c.fetchall()
            for x in the_tasks:
                self.task_number += 1
                task_card = TodotaskCard()
                task_card.ids.task_number.text = f"Task #{self.task_number}"
                task_card.ids.description.text = x[0]
                self.ids.todo_list.add_widget(task_card)

            sqlcommand = ("SELECT habit_name FROM habits WHERE user_id = (%s)")
            values = (id[0][0],)
            c.execute(sqlcommand, values)
            the_habits = c.fetchall()
            for y in the_habits:
                sqlcommand2 = "SELECT completed_for_the_day FROM habits where habit_name = (%s)"
                values2 = (y[0],)
                c.execute(sqlcommand2, values2)
                z = c.fetchall()
                if z[0][0] == "False":
                    self.habit_number += 1
                    habit_card = TodohabitCard()
                    habit_card.ids.task_number.text = f"Habit #{self.habit_number}"
                    habit_card.ids.description.text = y[0]
                    self.ids.todo_list.add_widget(habit_card)
            self.updated_screen = False
            mydb.commit()

            mydb.close()

    def add_task_card(self, task_name):
        self.task_number += 1
        task_card = TodotaskCard()
        task_card.ids.task_number.text = f"Task #{self.task_number}"
        task_card.ids.description.text = task_name
        self.ids.todo_list.add_widget(task_card)

    def add_habit_card(self, habit_name):
        self.habit_number += 1
        habit_card = TodohabitCard()
        habit_card.ids.task_number.text = f"Habit #{self.habit_number}"
        habit_card.ids.description.text = habit_name
        self.ids.todo_list.add_widget(habit_card)




class AddScreen(Screen):
    a_task = True
    a_habit = False
    name_in_q = ""
    time = ""

    def task_button(self):
        self.a_task = True
        self.a_habit = False
        self.ids.task_button_display.background_color = (202/255, 162/255, 118/255, 1)
        self.ids.habit_button_display.background_color = (222/255, 182/255, 138/255, 1)

    def habit_button(self):
        self.a_habit = True
        self.a_task = False
        self.ids.habit_button_display.background_color = (202/255, 162/255, 118/255, 1)
        self.ids.task_button_display.background_color = (222/255, 182/255, 138/255, 1)

    def submit_button(self):
        self.name_in_q = self.ids.the_name.text
        self.time = f'{self.ids.time_spinner_1.text}:{self.ids.time_spinner_2.text} {self.ids.time_spinner_3.text}'

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="wajeeh786",
            database="life_bun"
        )
        c = mydb.cursor()

        id = self.parent.get_screen("login").getUserId()
        if not id:
            id = self.parent.get_screen("signup").get_user_id()

        if self.a_task:
            sqlcommand = "INSERT INTO tasks (task_name, user_id) VALUES (%s, %s)"
            values = (self.name_in_q, id[0][0])
            c.execute(sqlcommand,values)
            self.parent.get_screen("main").add_task_card(self.name_in_q)
        else:
            sqlcommand = "INSERT INTO habits (habit_name, days_completed, completed_for_the_day, time, user_id) VALUES (%s, %s, %s, %s, %s)"
            values = (self.name_in_q, 0, "False", self.time, id[0][0])
            c.execute(sqlcommand, values)
            self.parent.get_screen("main").add_habit_card(self.name_in_q)


        mydb.commit()

        mydb.close()

        self.ids.the_name.text = "Name"
        self.ids.time_spinner_1.text = "1"
        self.ids.time_spinner_2.text = "00"
        self.ids.time_spinner_3.text = "AM"


    def get_name(self):
        return self.name_in_q

    def get_time(self):
        return self.time

    def get_task_status(self):
        return self.a_task

    def get_habit_status(self):
        return self.a_habit

class HabitScreen(Screen):
    updated_screen = True

    def on_touch_move(self, touch):
        if touch.x < touch.ox:
            self.parent.current = "home"

    def update_screen(self):
        if self.updated_screen:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="wajeeh786",
                database="life_bun"
            )
            c = mydb.cursor()

            id = self.parent.get_screen("login").getUserId()
            if not id:
                id = self.parent.get_screen("signup").get_user_id()
        sqlcommand = ("SELECT habit_name FROM habits WHERE user_id = (%s)")
        values = (id[0][0],)
        c.execute(sqlcommand, values)
        the_habits = c.fetchall()
        for y in the_habits:
            habit_card = HabitThing()
            sqlcommand2 = "SELECT days_completed FROM habits where habit_name = (%s)"
            values2 = (y[0],)
            c.execute(sqlcommand2, values2)
            z = c.fetchall()
            habit_card.ids.habitname.text = f"{y[0]} \n {z[0][0]} days"
            self.ids.habit_list.add_widget(habit_card)
        self.updated_screen = False
        mydb.commit()

        mydb.close()




class HabitThing(MDFloatLayout):
    pass



class WindowManager(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "LightGreen"

        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "wajeeh786",
            database = "life_bun"
        )

        c = mydb.cursor()






        kv = Builder.load_file("login.kv")
        return kv




if __name__ == "__main__":
    MainApp().run()