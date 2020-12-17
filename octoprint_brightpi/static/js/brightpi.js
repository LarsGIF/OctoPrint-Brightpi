/*
 * View model for OctoPrint-Brightpi
 *
 * Author: Lars Fransén
 * License: AGPLv3
 */

$(function() {
    function BrightpiViewModel(parameters) {
        var self = this;

        // Assign the injected parameters.
        // See OCTOPRINT_VIEWMODELS.push({ dependencies: [...] }) below.
        self.loginState = parameters[0];
        self.settings = parameters[1];

        // This will hold the URL currently displayed by the iframe
        self.currentUrl = ko.observable();

        self.lightOff = function() {
            // Send a whitLight off command to the server
            OctoPrint.simpleApiCommand("brightpi", "whitLight", {"on": false});
        };

        self.lightOn = function() {
            // Send a whitLight on command to the server
            OctoPrint.simpleApiCommand("brightpi", "whitLight", {"on": true});
        };

        self.irLightOff = function() {
            // Send a brightpi off command to the server
            OctoPrint.simpleApiCommand("brightpi", "irLight", {"on": false});
        };

        self.irLightOn = function() {
            // Send a brightpi on command to the server
             OctoPrint.simpleApiCommand("brightpi", "irLight", {"on": true});
        };
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels
     * for more details and a full list of the available options. */
    OCTOPRINT_VIEWMODELS.push({
        construct: BrightpiViewModel,
        // ViewModels your plugin depends on,
        dependencies: [ "loginStateViewModel", "settingsViewModel" ],
        // Elements to bind to, e.g. #settings_plugin_brightpi, #tab_plugin_brightpi, ...
        elements: [ "#tab_plugin_brightpi" ]
    });
});
