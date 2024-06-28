import json
from nicegui import ui


@ui.page('/')
def index():
    def load_user_info():
        try:
            with open('user_info.json', 'r') as data:
                return json.load(data)
        except FileNotFoundError:
            print('No file found...')

    user_data = load_user_info()

    # NAME
    user_name = ui.input(label='Full Name',
                         placeholder='John Doe',
                         value=user_data['name'] if user_data else '',
                         on_change=lambda name: user_name.set_value(name.value))

    # AGE
    ui.label('How old are you?')
    user_age = ui.slider(min=0,
                         max=100,
                         value=user_data['age'] if user_data else 50,
                         on_change=lambda age: user_age.set_value(age.value))
    ui.label().bind_text_from(user_age, 'value')

    # FAVOURITE COLOR
    ui.label('What is your favorite color?')
    user_color = ui.color_input(label='Color',
                                value=user_data['color'] if user_data else '#000000',
                                on_change=lambda color: user_color.set_value(color.value))

    with ui.dialog() as dialog, ui.card():
        ui.label('Are you sure?')
        with ui.row():
            ui.button('Yes', on_click=lambda: dialog.submit(True))
            ui.button('No', on_click=lambda: dialog.submit(False))

    async def submit():
        result = await dialog
        if result:
            user_info = {'name': user_name.value,
                         'age': user_age.value,
                         'color': user_color.value}

            info_json = json.dumps(user_info)

            with open('user_info.json', 'w') as info:
                info.write(info_json)
                ui.notify('Your information has been saved!')
                print('File created successfully!')

    ui.button('Submit', on_click=submit)


ui.run(native=True)
