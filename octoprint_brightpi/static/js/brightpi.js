/*
 * View model for OctoPrint-Brightpi
 *
 * Author: Lars Fransén
 * License: AGPLv3
 */

from brightpi import *

$(function() {
    function BrightpiViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        brightPi = BrightPi();
        self.dialog = undefined;

        self.onStartup = function() {
            self.dialog = $("#plugin_brightpi_generated");
            brightPi.reset()
        };

        self.showDialog = function(title, data) {
            if (self.dialog === undefined) return;
        // TODO: Implement your plugin's view model here.

        };

        self.lightOff = function() {
            // TODO: Implement lightOff here.
            //    if (!self.enableReload()) return;
            //    self.loadFile(self.loadedFilepath, self.loadedFileDate);
            brightPi.set_led_on_off((1 ,3), OFF)
        };

        self.lightOn = function() {
                // TODO: Implement lightOn here.
                // if (!self.enableReload()) return;
                // self.loadFile(self.loadedFilepath, self.loadedFileDate);
            brightPi.set_led_on_off((1 ,3), ON)
        }
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: BrightpiViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ /* "loginStateViewModel", "settingsViewModel" */ ],
        // Elements to bind to, e.g. #settings_plugin_brightpi, #tab_plugin_brightpi, ...
        elements: [ /* ... */ ]
    });
});
