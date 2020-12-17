# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
from .camera_light import *

camera = CameraLight()

class BrightpiPlugin(
          octoprint.plugin.AssetPlugin,
          octoprint.plugin.TemplatePlugin,
          octoprint.plugin.SimpleApiPlugin,
          octoprint.plugin.SettingsPlugin):

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        self._logger.info("Running get_assets.")
        return dict(
            js=["js/brightpi.js"],
            css=["css/brightpi.css"],
            less=["less/brightpi.less"]
        )

    ##~~ TemplatePlugin mixin

    def get_template_configs(self):
        self._logger.info("Running get_template_configs.")
        return [
            dict(type="settings", custom_bindings=False)
        ]

    ##~~ SimpleApiPlugin

    def get_api_commands(self):
        return dict(
            whitLight=["on"],
            irLight=["on"]
        )

    def on_api_command(self, command, data):
        if command == "whitLight":
            self._logger.info("whitLight called, parameter on is {}".format(data.get('on')))
            if data.get("on"):
                camera.white_light_on()
            else:
                camera.white_light_off()
        elif command == "irLight":
            self._logger.info("irLight called, parameter on is {}".format(data.get('on')))
            if data.get("on"):
                camera.ir_light_on()
            else:
                camera.ir_light_off()

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        # Create a plugin: brightpi: dictionary.
        # Changed values will be saved in file config.yaml
        self._logger.info("Running get_settings_defaults.")
        return dict(
            enableIR=False
        )

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        self._logger.info("Running get_update_information.")
        return dict(
            brightpi=dict(
                displayName="Brightpi Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="LarsGIF",
                repo="OctoPrint-Brightpi",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/LarsGIF/OctoPrint-Brightpi/archive/{target_version}.zip"
            )
        )

__plugin_name__ = "Bright Pi"
__plugin_pythoncompat__ = ">=2.7,<4"  # python 2 and 3

##~~ TODO: Activate this to check that the smbus2 package can be loaded
#def __plugin_check__():
#    try:
#        import smbus2
#    except ImportError:
#        return False
#    return True

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = BrightpiPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
