import logging

import dearpygui.dearpygui as dpg

def start_UI(thr_name):
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    dpg.create_context()

    def button_callback(sender, app_data, user_data):
        print(f"sender is: {sender}")
        print(f"app_data is: {app_data}")
        print(f"user_data is: {user_data}")

    with dpg.window(label="Tutorial"):
        # user data set when button is created
        dpg.add_button(label="Print to Terminal", callback=button_callback, user_data="Some Data")

        # user data and callback set any time after button has been created
        dpg.add_button(label="Print to Terminal 2", tag="btn")
        dpg.set_item_callback("btn", button_callback)
        dpg.set_item_user_data("btn", "Some Extra User Data")

        dpg.add_text(str(1), tag="text")

    dpg.create_viewport(title='Custom Title', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    logging.info("Thread %s: starting", thr_name)
    dpg.start_dearpygui()
    dpg.destroy_context()
