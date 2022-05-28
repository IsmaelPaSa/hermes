from plyer import notification

def notify(my_title, my_message, my_app_name, my_timeout, my_icon, my_toast):
    try:
        notification.notify(
            title=my_title,
            message=my_message,
            app_name=my_app_name,
            timeout=my_timeout,
            app_icon=my_icon,
            toast=my_toast
        )
    except:
        pass