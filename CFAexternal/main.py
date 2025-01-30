from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineAvatarListItem  
from kivymd.uix.pickers import MDDatePicker
import os
import shutil
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
import mysql.connector
from kivymd.uix.dialog import MDDialog
from plyer import filechooser
from kivy.core.text import LabelBase
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivymd.toast import toast
from kivymd.uix.list import OneLineIconListItem, IconRightWidget
from kivymd.icon_definitions import md_icons
LabelBase.register(name='Baltore', fn_regular='fonts/Baltore.ttf')

Window.size = (360, 700)


class ItemLostScreen(Screen):
    def on_enter(self, *args):
        bottom_nav = self.ids.bottom_nav
        bottom_nav.switch_tab('ItemLost')
        self.fetch_lost_items()
    def connect_to_db(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",       
                user="root",  
                password="",
                database="msg" 
            )
            print("Connection to the database established.")
            return connection
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            return None    
    def fetch_lost_items(self):
        connection = self.connect_to_db()
        if connection is None:
            print("Failed to connect to the database.")
            return
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM items WHERE item_type = 'LOST' AND status = 'available'")
            lost_items = cursor.fetchall()
            self.update_item_container(lost_items)
        except mysql.connector.Error as err:
            print(f"Error fetching items: {err}")
        finally:
            if cursor is not None:
                cursor.close()
            connection.close()
            
    def update_item_container(self, lost_items):
        item_container = self.ids.item_container
        item_container.clear_widgets()
        for item in lost_items:
            item_id, image, title, description, location, date, item_type, status, claimed_by, claimed_date, user_id = item
            # Create an MDCard for each lost item
            card = MDCard(size_hint_y=None, height="200dp", elevation=3, md_bg_color=(1, 1, 1, 1))
            card.add_widget(
                MDBoxLayout(orientation='vertical', padding=10, spacing=5)
            )
            
            box_layout = card.children[0]
            
            if image:
                img = Image(source=image, size_hint_y=None, height="100dp", allow_stretch=True, keep_ratio=True)
                box_layout.add_widget(img)
                
            box_layout.add_widget(MDLabel(text=title, font_style="H6", halign="center"))
            box_layout.add_widget(MDLabel(text=description, halign="center"))
            box_layout.add_widget(MDLabel(text=f"Location: {location}", halign="center"))
            box_layout.add_widget(MDLabel(text=f"Date: {date}", halign="center"))  

            item_container.add_widget(card)
            
    def clear_fields(self):
            self.ids.searchLost.text= ''    
    def perform_search(self, search_text):
        connection = self.connect_to_db()
        if connection is None:
            print("Failed to connect to the database.")
            return
        try:
            cursor = connection.cursor()
            query = """
                SELECT * FROM items 
                WHERE item_type = 'LOST' 
                AND (title LIKE %s OR description LIKE %s OR location LIKE %s)
            """
            search_pattern = f"%{search_text}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            lost_items = cursor.fetchall()
            self.update_item_container(lost_items)
        except mysql.connector.Error as err:
            print(f"Error fetching items: {err}")
        finally:
            cursor.close()
            connection.close()    
            
class LoadingScreen(Screen):
    
    def press_it(self):
        if self.ids.progress_bar.value < self.ids.progress_bar.max:
            self.ids.progress_bar.value += 10  # Increment progress
        else:
            
            self.manager.current = 'login'
            
class UserProfileScreen(Screen):
    def on_enter(self):
        MDApp.get_running_app().fetch_user_info()
      
class LoginScreen(Screen):
    def toggle_password_visibility(self):
        # Access the password input field in the LoginScreen
        password_input = self.root.ids.password_input  # Accessing via root (LoginScreen)
        
        # Toggle the visibility of the password
        password_input.password = not password_input.password
        
        # Toggle the icon between 'eye' and 'eye-off' based on the password visibility
        if password_input.password:
            password_input.icon_right = "eye-off"  # When password is hidden
        else:
            password_input.icon_right = "eye"  # When password is visible
    

class SignupScreen(Screen):
    pass

class NotificationScreen(Screen):
    def on_enter(self):
        # Mark all notifications as read when the screen is opened
        self.fetch_notifications()
        
        
    def fetch_notifications(self):
        app = MDApp.get_running_app()
        query = """
            SELECT message FROM notifications 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """
        
        app.cursor.execute(query, (app.current_user_id,))
        notifications = app.cursor.fetchall()
        
        # Clear and display notifications
        self.ids.notification_list.clear_widgets()
        for message in notifications:
            notification_item = OneLineListItem(text=message[0])
            self.ids.notification_list.add_widget(notification_item)
            
    def mark_notifications_as_read(self):
        app = MDApp.get_running_app()
        query = "UPDATE notifications SET is_read = %s WHERE user_id = %s"
        app.cursor.execute(query, (True, app.current_user_id))
        app.db.commit()


class UserListScreen(Screen):
    def on_enter(self, *args):
        # Reset the bottom navigation to the default state
        bottom_nav = self.ids.bottom_nav
        bottom_nav.switch_tab('message')
    

class MessagingScreen(Screen):
    pass

class AboutUsScreen(Screen):pass
class PostItemScreen(Screen):
    selected_type = None  # Variable to store the selected item type (LOST/FOUND)
    def connect_to_db(self):
        
        try:
            connection = mysql.connector.connect(
                host="localhost",       
                user="root",  
                password="",
                database="msg" 
            )
            print("Connection to the database established.")
            return connection
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            return None
    def on_enter(self, *args):
        # Reset the bottom navigation to the default state
        bottom_nav = self.ids.bottom_nav
        bottom_nav.switch_tab('PostItemScreen')
    def show_date_picker(self):
        date_picker = MDDatePicker()
        date_picker.bind(on_save=self.on_date_selected)
        date_picker.open()
    def on_date_selected(self, instance, value, date_range):
        self.ids.date.text = str(value)        
            
    def set_item_type(self, item_type):
        self.selected_type = item_type
        print(f"Selected item type: {self.selected_type}")
    def on_enter(self, *args):
        img_error_label = self.ids.img_error_label
        # Reset the bottom navigation to the default state
        self.reset_fields()
        bottom_nav = self.ids.bottom_nav
        bottom_nav.switch_tab('PostItemScreen')
        img_error_label.text = ""
    def post_item_notif(self, user_id):
        # Call validation method
        if self.validate_fields():
            # If validation passed, proceed with posting the item
            self.add_item_to_database(user_id)  # Add item to the database
            toast("Item Posted Successfully")
            self.reset_fields()  # Reset fields after posting
        else:
            toast("Please fill in all required fields")
            
    def validate_fields(self):
        # Get the text values of all the text fields
        img = self.ids.img
        title = self.ids.title
        desc = self.ids.desc
        loc = self.ids.loc
        date = self.ids.date
        img_error_label = self.ids.img_error_label
        # Initialize the validity flag as True
        is_valid = True

        
        # Check if the image is set
        if not img.source:
            img_error_label.text = "Please upload an image"
            is_valid = False
        else:
            img_error_label.text = ""  # Clear error message if an image is set
            
        # Check each field and show individual error messages
        if not title.text.strip():
            title.error = True  # Show error state
            title.helper_text = "Title is required"  # Set custom helper text
            title.helper_text_mode = "on_error"  # Show the helper text as an error
            is_valid = False
        else:
            title.error = False  # Remove error
            title.helper_text = ""
        if not desc.text.strip():
            desc.error = True
            desc.helper_text = "Description is required"
            desc.helper_text_mode = "on_error"
            is_valid = False
        else:
            desc.error = False
            desc.helper_text = ""
        if not loc.text.strip():
            loc.error = True
            loc.helper_text = "Location is required"
            loc.helper_text_mode = "on_error"
            is_valid = False
        else:
            loc.error = False
            loc.helper_text = ""

        if not date.text.strip():
            date.error = True
            date.helper_text = "Date is required"
            date.helper_text_mode = "on_error"
            is_valid = False
        else:
            date.error = False
            date.helper_text = ""
        
        # Return the validity status
        return is_valid
        
    def reset_img(self):
        self.ids.img.source = ""
        self.ids.img_error_label.text = ""
    def file_chooser(self):
            filechooser.open_file(on_selection=self.selected)  
    def selected(self, selection):
            print(selection[0])
            self.ids.img.source = selection[0]  
            self.ids.img.reload()  # Ensure the image widget updates to display the new image
    def reset_fields(self):
        self.ids.img.source=""
        self.ids.title.text = ''
        self.ids.desc.text = ''
        self.ids.loc.text = ''
        self.ids.date.text = ''
        
        for field in [self.ids.title, self.ids.desc, self.ids.loc, self.ids.date]:
            field.error = False
            field.helper_text = ""
        # Reset checkboxes (LOST/FOUND)
        self.selected_type = None  # Clear the selected type
        self.ids.lost_checkbox.active = False  # Uncheck the LOST checkbox
        self.ids.found_checkbox.active = False  # Uncheck the FOUND checkbox
        
        # Clear any checkbox error message
        #self.ids.checkbox_error_label.text = "" 
        
    def add_item_to_database(self, user_id):
        connection = self.connect_to_db()
        if connection is None:
            print("Failed to connect to the database.")
            return
        try:  
            cursor = connection.cursor()
            
            # Base path where images will be saved
            
            base_image_path = "C:/Users/user/Desktop/CFAFinal/CFAexternal/products"
            if not os.path.exists(base_image_path):
                os.makedirs(base_image_path)  # Create the directory if it doesn't exist
                
            # Extract the filename from the source
            image_filename = os.path.basename(self.ids.img.source)    
            # Create a new path for the image
            new_image_path = os.path.join(base_image_path, image_filename)
            # Move or copy the image to the new path
            shutil.copy(self.ids.img.source, new_image_path)
            sql_insert_query = """INSERT INTO items (image, title, description, location, date, item_type, status, user_id) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        
        
            data = (
                new_image_path,
                self.ids.title.text.strip(),
                self.ids.desc.text.strip(),
                self.ids.loc.text.strip(),
                self.ids.date.text.strip(),
                self.selected_type,  # Use the selected item type (LOST/FOUND/CLAIMED)
                'available',
                user_id
            )
            cursor.execute(sql_insert_query, data)
            connection.commit()
            
            
            item_id = cursor.lastrowid # Retrieve the item_id of the newly added item
            notification_message = f"Item '{self.ids.title.text.strip()}' was posted successfully."
            notification_query = """
                INSERT INTO notifications (user_id, item_id, message, created_at, is_read) 
                VALUES (%s, %s, %s, NOW(), %s)
            """
            notification_data = (user_id, item_id, notification_message, False)
            cursor.execute(notification_query, notification_data)
            connection.commit()
            print("Notification added successfully.")
            
            self.manager.get_screen('notif').fetch_notifications()
            toast("Item added successfully.")
        except mysql.connector.Error as err:
            print(f"Error while inserting to database: {err}")    
        
        finally:
            cursor.close()
            connection.close()      
class MainScreen(Screen):
    def close_drawer(self):
        # Close the navigation drawer
        nav_drawer = self.ids.nav_drawer
        if nav_drawer:
            nav_drawer.set_state('close')
    def on_enter(self, *args):
        bottom_nav = self.ids.bottom_nav
        bottom_nav.switch_tab('home')  # Set default tab to 'home'
        self.fetch_items()
        current_user_id = MDApp.get_running_app().current_user_id
        print(f"Current User ID in MainScreen: {current_user_id}")
        
    def connect_to_db(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",       
                user="root",  
                password="",
                database="msg" 
            )
            return connection    
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            return None
    def fetch_items(self):
        #Fetch all items (LOST and FOUND) from the database. 
        connection = self.connect_to_db()
        if connection is None:
            print("Failed to connect to the database.")
            return
        try:
            cursor = connection.cursor()
            
            query = """
                SELECT 
                    i.item_id, 
                    i.image, 
                    i.title, 
                    i.description, 
                    i.location, 
                    i.date, 
                    i.item_type, 
                    i.status, 
                    i.user_id, 
                    u.user_name 
                FROM 
                    items i
                JOIN 
                    users u ON i.user_id = u.user_id
                WHERE 
                    i.item_type IN ('LOST', 'FOUND');
            """
            cursor.execute(query)
            items = cursor.fetchall()
            self.update_item_grid(items)
        except mysql.connector.Error as err:
            print(f"Error fetching items: {err}")
        finally:
            cursor.close()
            connection.close()
    
    
    def update_item_grid(self, items):
        item_grid = self.ids.item_grid
        item_grid.clear_widgets()
        
        for item in items:
            item_id, image, title, description, location, date, item_type, status, user_id, user_name = item
            print(f"Processing item: ID={item_id}, Title={title}, Image={image}, Description={description}") ##debugging lang to para icheck if magrender correct info
          #  card = MDCard(size_hint_y=None, height="350dp", orientation="vertical", padding="1dp")
          #  card.md_bg_color = (0.9, 0.9, 0.9, 1)
               
            if item_type == 'LOST':
                
                outline_color = (1, 0, 0, 1) #red for LOSTT
                
            else: 
                
                outline_color = (0.7, 0.7, 0.7, 1)  # Light gray for FOUND items
            
            outline_layout = MDBoxLayout(
                size_hint_y=None, 
                height="350dp",
                padding="2dp",
                md_bg_color=outline_color,  # Border color
                orientation="vertical",
                radius=[18]
            )  
            card = MDCard(
                size_hint_y=None,
                height="346dp",  #  create outline effect
                orientation="vertical",
                padding="10dp",
                radius=[15],
                md_bg_color=(1, 1, 1, 1),  
                
            )
            
            
            #card = MDCard(size_hint_y=None, height="250dp", elevation=2, radius=[15])
            box_layout = MDBoxLayout(orientation='vertical', spacing=8, padding=(10, 0, 10, 10))  # Increased spacing and padding
            
            if image:
                
                image_path = os.path.join("C:/Users/user/Desktop/CFAFinal/CFAexternal/products", image)
                print(f"Image source: {image_path}")  # debugging img
                img = Image(source=image_path, size_hint_y=None, height="110dp", size_hint_x=1)
                box_layout.add_widget(img)
            
                
            #details ng each item below ng image
            box_layout.add_widget(MDLabel(text=title, halign='center', font_style="H6", size_hint_y=None, height="40dp", theme_text_color="Primary"))
            box_layout.add_widget(MDLabel(text=description, halign='left', size_hint_y=None, height=self.calculate_label_height(description) + 20, text_size=(self.width - 30, None), theme_text_color="Secondary"))
            box_layout.add_widget(MDLabel(text=location, halign='left', size_hint_y=None, height="20dp"))
            box_layout.add_widget(MDLabel(text=str(date), halign='left', size_hint_y=None, height="20dp"))
            
            card.bind(on_release=lambda x, item_id=item_id, title=title, description=description, item_type=item_type, location=location, date=date, image=image, status=status, user_id=user_id, user_name=user_name: self.show_item_details(item_id, title, description, item_type, location, date, image, status, user_id, user_name))
            
            claim_button = MDRaisedButton(
                text="CLAIM",
                size_hint_y=None,
                height="40dp",  # Set a fixed height for the button
                md_bg_color= [1, 0, 0, 0.9],
                pos_hint={"center_x": 0.5}  # Center the button horizontally
            )
            self.claim_button = claim_button
            
            claim_button.disabled = (status == 'already claimed') or (user_id == MDApp.get_running_app().current_user_id)
            
            claim_button.bind(on_release=lambda x, item_id=item_id, title=title: self.claim_item(item_id, title, claim_button))
            box_layout.add_widget(claim_button)
            card.add_widget(box_layout)  # Add the layout to the card
            
            outline_layout.add_widget(card)
            item_grid.add_widget(outline_layout)
    def show_item_details(self, item_id, title, description, item_type, location, date, image, status, user_id, user_name):
        
        content = MDBoxLayout(
            orientation='vertical', 
            spacing=5, 
            padding=0,
            size_hint_y=None,
            height= dp(450),
            )
        if image:
            image_path = os.path.join("C:/Users/user/Desktop/CFAFinal/CFAexternal/products", image)
            item_image = Image(source=image_path, size_hint_y=None, height="200dp", allow_stretch=True)
            content.add_widget(item_image)
            
        content.add_widget(MDLabel(text=title, halign="center", size_hint_y=None, height="30dp", font_style="H6", theme_text_color="Custom", text_color=(1, 0, 0, 1)))
        content.add_widget(MDLabel(text=f"Description: {description}", halign="left", size_hint_y=None, height="30dp"))
        content.add_widget(MDLabel(text=f"Item type: {item_type}", halign="left", size_hint_y=None, height="20dp"))
        content.add_widget(MDLabel(text=f"Location: {location}", halign="left", size_hint_y=None, height="20dp"))
        content.add_widget(MDLabel(text=f"Date: {date}", halign="left", size_hint_y=None, height="20dp"))
        
        post_id_text = "You" if user_id == MDApp.get_running_app().current_user_id else str(user_id)
        content.add_widget(MDLabel(text=f"Posted by userid: {post_id_text}", halign="left", size_hint_y=None, height="20dp")) 
        
        
        content.add_widget(MDLabel(text=f"Posted user: {user_name}", halign="left", size_hint_y=None, height="20dp"))
        content.add_widget(MDLabel(text=f"Status: {status}", halign="left", size_hint_y=None, height="20dp"))
        
        
        message_button = MDRaisedButton(
            text="Message User",
            size_hint_y=None,
            height="40dp",
            pos_hint={"center_x": 0.5, "y": 0},
            padding=15,
            md_bg_color= [1, 0, 0, 0.9],
            theme_text_color= "Custom",  # Allow custom text color
            text_color= [1, 1, 1, 1]
            
        )
        message_button.disabled = (user_id == MDApp.get_running_app().current_user_id)
        message_button.bind(on_release=lambda x: self.go_to_msguser(user_id))
        content.add_widget(message_button)
        
        
        
        self.dialog = MDDialog(
            title="Item Details",
            type="custom",
            content_cls=content,
            size_hint=(1, None),  # Width fills the screen, height is custom
            height="600dp",       
            auto_dismiss=False,   # Prevent dismissing by tapping outside
            buttons=[
                MDFlatButton(text="CLOSE", on_release=lambda x: self.dialog.dismiss())
            ],
        )
        self.dialog.pos_hint = {"center_x": 0.5, "y": 0}
        self.dialog.open()
        
    def closedialog(self, *args):
        self.dialog.dismiss()
            
    def go_to_msguser(self, user_id):
    
        MDApp.get_running_app().select_user(user_id)

        self.dialog.dismiss()
        
    def message_user(self, user_id):
        # Implement your messaging functionality here
        print(f"Messaging user with ID: {user_id}")    
        
    def calculate_label_height(self, text):
        # A simple approximation for the label height based on text length
        lines = text.split('\n')
        line_height = 20  # Approximate height for each line
        return len(lines) * line_height + 20
    def claim_item(self, item_id, title, claim_button):
        app = MDApp.get_running_app()
        cursor = app.cursor
        
        try:
            cursor.execute("SELECT claimed_by, user_id, status FROM items WHERE item_id = %s", (item_id,))
            result = cursor.fetchone()
            
            if result:
                claimed_by, item_owner_id, status = result
                # Check if claimed na yung item
                if claimed_by is not None:
                    toast(f"The item '{title}' has already been claimed by {claimed_by}.")
                    return
                
                cursor.execute("SELECT user_name FROM users WHERE user_id = %s", (app.current_user_id,))
                user_info = cursor.fetchone()
                if user_info:
                    user_name = user_info[0]# Assuming user_name is in the first column
                # Update the item's claimed_by column to the current user ID
                cursor.execute(
                    "UPDATE items SET claimed_by = %s, status = 'already claimed', claimed_date = NOW() WHERE item_id = %s",
                    (app.current_user_id, item_id)
                )
                app.db.commit()
                toast(f"You have successfully claimed '{title}'!")
                
                claim_button.disabled = True  # Disable the claim button after claiming
                self.fetch_items()  # Refresh 
                
                
                notification_message = f"{user_name} with User ID {app.current_user_id} has claimed your item '{title}'."
                notification_query = """
                    INSERT INTO notifications (user_id, item_id, message, created_at, is_read) 
                    VALUES (%s, %s, %s, NOW(), %s)
                """
                notification_data = (item_owner_id, item_id, notification_message, False)
                cursor.execute(notification_query, notification_data)
                app.db.commit()
                print("Owner notified of item claim.")
                app.root.get_screen('notif').fetch_notifications()


            else:
                toast("Item not found.")   
        except mysql.connector.Error as e:        
            print(f"Error claiming item: {e}")
            toast("An error occurred while claiming the item.")


class EditProfileFinalScreen(Screen):
    def show_date_picker(self):
        date_picker = MDDatePicker()
        date_picker.bind(on_save=self.on_date_selected)
        date_picker.open()
    def on_date_selected(self, instance, value, date_range):
        self.ids.edit_birthday.text = str(value)
    def on_enter(self):
        self.load_current_profile_picture()
    def file_chooser(self):
            filechooser.open_file(on_selection=self.selected)  
    def selected(self, selection):
        if selection: 
            image_path = selection[0]   
            print(f"Selected file: {image_path}")
            self.ids.edit_profile_picture.source = selection[0]  
            self.ids.edit_profile_picture.reload()  
            #self.update_profile_picture(image_path)
    def update_profile_picture(self, image_path):
        """Update the profile picture in the database."""
        app = MDApp.get_running_app()
        update_query = "UPDATE users SET profile_pic = %s WHERE user_id = %s"
        app.cursor.execute(update_query, (image_path, app.current_user_id))
        app.db.commit()
        print("Profile picture updated successfully!")                 
    def load_current_profile_picture(self):
        app = MDApp.get_running_app()
        query = "SELECT profile_pic FROM users WHERE user_id = %s"
        app.cursor.execute(query, (app.current_user_id,))
        result = app.cursor.fetchone()
        
        if result and result[0]:  # If there is a result and the profile_pic is not empty
            self.ids.edit_profile_picture.source = result[0]
        else:
            #  static default image if there's no profile picture
            self.ids.edit_profile_picture.source = 'default.png'  
        
        # Reload the image to ensure it displays
        self.ids.edit_profile_picture.reload()
            

class CrimsonFindsApp(MDApp):
    current_user_id = None
    current_receiver_id = None  # Initialize current_receiver_id

    def build(self):
        self.connect_to_db()
        self.theme_cls.theme_style ="Light"
        self.theme_cls.material_style = "M2"
        return Builder.load_file('layout.kv')

    def connect_to_db(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="msg"
        )
        self.cursor = self.db.cursor()

    def change_screen(self, screen_name):
        self.root.current = screen_name

    def login(self):
        username = self.root.get_screen('login').ids.username_input.text
        password = self.root.get_screen('login').ids.password_input.text

        
        self.cursor.execute("SELECT user_id, email FROM users WHERE user_name = %s AND password = %s",
                            (username, password))
        user = self.cursor.fetchone()

        if user:
            self.current_user_id = user[0]  # Store current user ID
            self.current_user = {
                'username': username,  # Store username
                'email': user[1]       # Store the user's email
            }

            print(f"Current User ID: {self.current_user_id}")
            
            
            self.fetch_user_info() 

            # Fetch other users to display
            self.fetch_users()  

            
            toast('You are now logged in')
            self.change_screen('main')
        else:
            toast('Invalid credentials')
    def fetch_user_info(self):

        query = "SELECT user_name, name, email, birthday, college, profile_pic FROM users WHERE user_id = %s"
        self.cursor.execute(query, (self.current_user_id,))
        user_info = self.cursor.fetchone()

        if user_info:
            
            self.root.get_screen('user_profile').ids.get_username.text = f"@{user_info[0]}"
            self.root.get_screen('user_profile').ids.get_name.text = user_info[1] if user_info[1] else "Not set"
            self.root.get_screen('user_profile').ids.email_label.text = f"Email: {user_info[2]}" if user_info[2] else "Email: Not set"
            self.root.get_screen('user_profile').ids.get_birthday.text = f"Birthday: {user_info[3]}" if user_info[3] else "Birthday: Not set"
            self.root.get_screen('user_profile').ids.get_college.text = f"College: {user_info[4]}" if user_info[4] else "College: Not set"
            
            
            profile_picture = user_info[5] if user_info[5] else "default.png"
            self.root.get_screen('user_profile').ids.profile_picture.source = profile_picture
            self.root.get_screen('user_profile').ids.profile_picture.reload()
            
    def switch_to_edit_profile(self):
        # Check if  information is available 
        user_data = self.root.get_screen('user_profile').ids
        edit_screen = self.root.get_screen('edit_profile')
        
        edit_screen.ids.edit_name.text = user_data.get_name.text.split(": ")[-1] if user_data.get_name.text else ""
        edit_screen.ids.edit_email.text = user_data.email_label.text.split(": ")[-1] if user_data.email_label.text else ""
        edit_screen.ids.edit_birthday.text = user_data.get_birthday.text.split(": ")[-1] if user_data.get_birthday.text else ""
        edit_screen.ids.edit_college.text = user_data.get_college.text.split(": ")[-1] if user_data.get_college.text else ""
        
        
        self.root.current = 'edit_profile'  # Switch to edit profile screen
        
    def save_profile_changes(self):
        edit_screen = self.root.get_screen('edit_profile').ids
        updated_name = edit_screen.edit_name.text
        updated_email = edit_screen.edit_email.text
        updated_birthday = edit_screen.edit_birthday.text
        updated_college = edit_screen.edit_college.text

        base_image_path = "C:/Users/user/Desktop/CFAFinal/CFAexternal"
        if not os.path.exists(base_image_path):
                os.makedirs(base_image_path)
        current_profile_pic_path = self.get_current_profile_picture_path()
        new_image_source = edit_screen.edit_profile_picture.source        
        if new_image_source and new_image_source != 'default.png':
            # If a new image is selected, copy it to the base path
            if new_image_source != current_profile_pic_path:
                image_filename = os.path.basename(new_image_source)
                new_image_path = os.path.join(base_image_path, image_filename)
            
        #    image_filename = os.path.basename(edit_screen['edit_profile_picture'].source) 
         #   new_image_path = os.path.join(base_image_path, image_filename)
                try:
                    shutil.copy(new_image_source, new_image_path)
                    profile_pic_path = new_image_path   
                except Exception as e:
                    toast(f"Failed to copy image: {e}")
                    return
           
            else:
                # If the image hasn't changed, use the current path
                profile_pic_path = current_profile_pic_path
        else:
            # If no new image is selected, use the current image
            profile_pic_path = current_profile_pic_path
            
        update_query = """
        UPDATE users
        SET name = %s, email = %s, birthday = %s, college = %s, profile_pic = %s
        WHERE user_id = %s
        """
        
        self.cursor.execute(update_query, (updated_name, updated_email, updated_birthday, updated_college, profile_pic_path, self.current_user_id))
        self.db.commit()
        toast("Profile updated successfully")
        self.root.current = 'user_profile'
        self.fetch_user_info()
    def get_current_profile_picture_path(self):
        app = MDApp.get_running_app()
        query = "SELECT profile_pic FROM users WHERE user_id = %s"
        app.cursor.execute(query, (app.current_user_id,))
        result = app.cursor.fetchone()
        return result[0] if result and result[0] else 'default.png'     
                
    def signup(self):
        username = self.root.get_screen('signup').ids.new_username_input.text
        password = self.root.get_screen('signup').ids.new_password_input.text
        confirm_password = self.root.get_screen('signup').ids.confirmpassword.text
        email = self.root.get_screen('signup').ids.email.text
        
        # Insert new user into the database
        if username and password and email:
            if password == confirm_password:  # Check if password and confirm password match
                self.cursor.execute("INSERT INTO users (user_name, password, email) VALUES (%s, %s, %s)",
                                    (username, password, email))
                self.db.commit()
                toast('Account created successfully')
                self.change_screen('login')  
            else:
                toast('Passwords do not match') 
        else:
            toast('Insert all required information')

    def fetch_users(self):
        self.cursor.execute("SELECT user_id, user_name, profile_pic FROM users WHERE user_id != %s", (self.current_user_id,))
        users = self.cursor.fetchall()
        user_list = self.root.get_screen('user_list').ids.user_list
        user_list.clear_widgets()

        for user_id, user_name, profile_pic in users:
            user_item = OneLineListItem(
                text=user_name,
                on_release=lambda x, uid=user_id: self.select_user(uid)# Pass the user_id to select_user
            )
            
            
            user_list.add_widget(user_item)
            
            
    def select_user(self, user_id):
        self.current_receiver_id = user_id
        self.root.current = 'messaging'
        self.fetch_messages()

    def send_message(self):
        message = self.root.get_screen('messaging').ids.message_input.text
        if message:
            self.cursor.execute(
                "INSERT INTO messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)",
                (self.current_user_id, self.current_receiver_id, message)
            )
            self.db.commit()
            self.root.get_screen('messaging').ids.message_input.text = ""
            self.fetch_messages()
            
             # kunin ung sender's username for the notification
            self.cursor.execute("SELECT user_name FROM users WHERE user_id = %s", (self.current_user_id,))
            sender_info = self.cursor.fetchone()
            if sender_info:
                sender_name = sender_info[0]
                
                #  notification pra sa receiver
                notification_message = f"{sender_name} (User ID {self.current_user_id}) sent you a message."
                notification_query = """
                    INSERT INTO notifications (user_id, item_id, message, created_at, is_read) 
                    VALUES (%s, %s, %s, NOW(), %s)
                """
                notification_data = (self.current_receiver_id, None, notification_message, False)
                self.cursor.execute(notification_query, notification_data)
                self.db.commit()
                print("Notification sent to the receiver about the new message.")
                
                self.root.get_screen('notif').fetch_notifications() ##REFRESHH
                
    def fetch_messages(self):
        self.cursor.execute(
            """
            SELECT 
                m.sender_id, 
                m.message, 
                m.timestamp, 
                u.user_name 
            FROM 
                messages m 
            JOIN 
                users u ON m.sender_id = u.user_id 
            WHERE 
                (m.sender_id = %s AND m.receiver_id = %s) 
                OR (m.sender_id = %s AND m.receiver_id = %s) 
            ORDER BY 
                m.timestamp ASC
            """,
            (self.current_user_id, self.current_receiver_id, self.current_receiver_id, self.current_user_id)
        )
        
        messages = self.cursor.fetchall()
        messages_list = self.root.get_screen('messaging').ids.messages_list
        messages_list.clear_widgets()

        for sender_id, message, timestamp, user_name in messages:
            item = OneLineListItem(text=f"{timestamp} - {user_name}: {message}")
            messages_list.add_widget(item)

    def on_stop(self):
        self.cursor.close()
        self.db.close()

    def show_dialog(self, title, message):
        from kivymd.uix.dialog import MDDialog
        dialog = MDDialog(title=title, text=message, size_hint=(0.8, 1))
        dialog.open()
    def logout(self):
        self.current_user_id = None  # Clear the current user ID
        login_screen = self.root.get_screen('login')
        login_screen.ids.username_input.text = ''
        login_screen.ids.password_input.text = ''
        self.change_screen('login')
    def set_home_screen(self):
        # Set default tab to 'home' when navigating back
        bottom_nav = self.root.get_screen('main').ids.bottom_nav
        bottom_nav.current = 'home'
    def go_back(self):
        self.root.current = 'main'
    def disconnect_from_db(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
        print("Database connection closed.")
    def upload_profile_picture(self):
        """Open a file chooser to select a profile picture."""
        filechooser = FileChooserIconView()
        filechooser.bind(on_submit=self.load_profile_picture)
        popup = Popup(title="Select a Profile Picture", content=filechooser, size_hint=(0.9, 0.9))
        popup.open()  
    def load_profile_picture(self, chooser, selection, *args):
        """Load the selected profile picture and update the UI and database."""
        if selection:
            # Assuming only one file is selected
            profile_picture_path = selection[0]
            # Update the image widget in the edit profile screen
            self.root.get_screen('edit_profile').ids.edit_profile_picture.source = profile_picture_path
            self.root.get_screen('edit_profile').ids.edit_profile_picture.reload()

            # Update the database with the new profile picture path
            update_query = "UPDATE users SET profile_picture = %s WHERE user_id = %s"
            self.cursor.execute(update_query, (profile_picture_path, self.current_user_id))
            self.db.commit()
            toast("Profile picture updated successfully!")
            
            ##NOTIFICATIONS FUNCTIONALITY##
    def create_notification(self, user_id, item_id, message):
        query = """
        INSERT INTO notifications (user_id, item_id, message, is_read)
        VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(query, (user_id, item_id, message, False))
        self.db.commit()        
    def insert_notification(self, user_id, item_id, message):
        insert_query = """
        INSERT INTO notifications (user_id, item_id, message) 
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(insert_query, (user_id, item_id, message))
        self.db.commit()
    def fetch_user_notifications(self, user_id):
        query = "SELECT message, created_at, item_id FROM notifications WHERE user_id = %s ORDER BY created_at DESC"
        self.cursor.execute(query, (user_id,))
        notifications = self.cursor.fetchall()
        return notifications  
    def mark_notifications_as_read(self):
        query = "UPDATE notifications SET is_read = %s WHERE user_id = %s"
        self.cursor.execute(query, (True, self.current_user_id))
        self.db.commit()  
    def fetch_notifications(self):
        query = "SELECT message, created_at FROM notifications WHERE user_id = %s AND is_read = %s"
        self.cursor.execute(query, (self.current_user_id, False))
        notifications = self.cursor.fetchall()
        
       
        notification_list = self.root.get_screen('notif').ids.notification_list
        notification_list.clear_widgets()
        
        for message, created_at in notifications:
            notification_item = OneLineListItem(text=f"{message} - {created_at}")
            notification_list.add_widget(notification_item) 
    def notify_item_claimed(self, item_id, claimer_user_id):
        # Fetch owner_id and item title for notification
        self.cursor.execute("SELECT user_id, title FROM items WHERE item_id = %s", (item_id,))
        owner_id, item_title = self.cursor.fetchone()
        
        # Fetch the claimant's username
        self.cursor.execute("SELECT user_name FROM users WHERE user_id = %s", (claimer_user_id,))
        claimer_name = self.cursor.fetchone()[0]
        
        # Create notification message
        message = f"{claimer_name} successfully claimed your item '{item_title}'"
        
        # Insert notification into the database
        self.cursor.execute("""
            INSERT INTO notifications (user_id, message, item_id, notification_type)
            VALUES (%s, %s, %s, 'claim')
        """, (owner_id, message, item_id))
        self.db.commit()
    def notify_user_message(self, sender_id, receiver_id):
        # Fetch sender's username
        self.cursor.execute("SELECT user_name FROM users WHERE user_id = %s", (sender_id,))
        sender_name = self.cursor.fetchone()[0]
        
        # Create notification message
        message = f"{sender_name} sent you a message"
        
        # Insert notification into the database
        self.cursor.execute("""
            INSERT INTO notifications (user_id, message, notification_type)
            VALUES (%s, %s, 'message')
        """, (receiver_id, message))
        self.db.commit()                             
if __name__ == "__main__":
    CrimsonFindsApp().run()
    