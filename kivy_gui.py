
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import numpy as np
import cv2
import io
import main

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (1280, 720)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')


class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        captured_image = camera.export_as_image()

        stream = io.BytesIO()
        captured_image.save(stream, fmt='png')
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        img = cv2.imdecode(data, 1)
        print("Captured")
        main.init_tflite()
        main.solve('direct_test', img)


class TestCamera(App):

    def build(self):
        return CameraClick()


TestCamera().run()