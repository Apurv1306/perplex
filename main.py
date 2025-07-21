import threading
import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.clock import Clock

class Root(BoxLayout):
    pass

class FaceAppServerApp(App):
    def build(self):
        self.title = "FaceApp Attendance Backend"
        # Request Android permissions
        if platform == 'android':
            self._request_android_permissions()
        root = Root(orientation='vertical', padding=20, spacing=15)
        self.status_label = Label(text="Flask Server: STOPPED
Tap to start the attendance system", size_hint_y=0.3, halign='center', valign='middle')
        self.status_label.bind(size=self.status_label.setter('text_size'))
        self.toggle_btn = ToggleButton(text='START SERVER', size_hint_y=0.2, on_press=self.toggle_server)
        self.info_label = Label(text="Ready to start attendance system
Once started, server runs on port 5000", size_hint_y=0.5, halign='center', valign='top')
        self.info_label.bind(size=self.info_label.setter('text_size'))
        root.add_widget(self.status_label); root.add_widget(self.toggle_btn); root.add_widget(self.info_label)
        self.flask_thread = None; self.flask_running = False
        return root

    def _request_android_permissions(self):
        try:
            from android.permissions import request_permissions, Permission
            permissions = [Permission.CAMERA, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET, Permission.ACCESS_NETWORK_STATE, Permission.ACCESS_WIFI_STATE]
            request_permissions(permissions)
        except ImportError:
            print('[INFO] Not on Android, skipping permission requests')

    def toggle_server(self, instance):
        if instance.state == 'down':
            self.start_flask_server()
        else:
            self.stop_flask_server()

    def start_flask_server(self):
        if self.flask_running:
            return
        try:
            import python_app as backend
            self.backend_app = backend.app
            def run_flask():
                try:
                    self.backend_app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
                except Exception as e:
                    print(f'[ERROR] Flask server error: {e}')
                    self.flask_running = False
                    Clock.schedule_once(self.update_ui_stopped, 0)
            self.flask_thread = threading.Thread(target=run_flask, daemon=True)
            self.flask_thread.start(); self.flask_running = True
            self.status_label.text = 'Flask Server: RUNNING
Attendance system is active'
            self.toggle_btn.text = 'STOP SERVER'
            self.info_label.text = '✓ Server running on port 5000
✓ Face recognition active
✓ Email notifications enabled
✓ Google Forms integration ready'
        except Exception as e:
            print(f'[ERROR] Failed to start Flask server: {e}')
            self.status_label.text = f'ERROR: {e}'; self.toggle_btn.state = 'normal'

    def stop_flask_server(self):
        try:
            import requests
            requests.get('http://127.0.0.1:5000/shutdown', timeout=2)
        except Exception:
            pass
        self.flask_running = False
        self.update_ui_stopped()

    def update_ui_stopped(self, *args):
        self.status_label.text = 'Flask Server: STOPPED
Tap to start the attendance system'
        self.toggle_btn.text = 'START SERVER'; self.toggle_btn.state = 'normal'
        self.info_label.text = 'Ready to start attendance system
Once started, server runs on port 5000'

if __name__ in ('__main__', '__android__'):
    FaceAppServerApp().run()
