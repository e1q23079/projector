from kivy.config import Config
from kivy.app import App

from kivy.uix.label import Label

# Set fixed window size for the application
Config.set("graphics","width","435")
Config.set("graphics","height","245")

# Define the main application class
class ProjectorApp(App):
        def build(self):
            return Label(text="Projector App Running")

# Run the application
if __name__ == "__main__":
    ProjectorApp().run()