'use strict';
// Copyright © 2015 OnlineGroups.net and Contributors.
// All Rights Reserved.
//
// This software is subject to the provisions of the Zope Public License,
// Version 2.1 (ZPL). http://groupserver.org/downloads/license/
//
// THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
// WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
// FITNESS FOR A PARTICULAR PURPOSE.
jQuery.noConflict();

function GSEmailSettingsUpdate() {
}

function GSProfileEmailSettingsAdd(addId) {
    var add = null, input = null, button = null;

    function inputChanged(event) {
        if ((input.value.length > 0) && button.hasAttribute('disabled')) {
            button.removeAttribute('disabled');
        } else if ((input.value.length == 0) &&
                   !button.hasAttribute('disabled')) {
            button.setAttribute('disabled', 'disabled');
        }
    }// inputChanged

    function setup() {
        add = document.getElementById(addId);
        input = add.getElementsByTagName('input')[0];  // There is only one
        input.onkeyup = inputChanged;

        button = add.getElementsByTagName('button')[0];
        button.setAttribute('disabled', 'disabled');
    } // setup
    setup(); // Note the automatic execution
}

jQuery(window).load(function() {
    var scriptElement = null, addId = '', adder = null;
    scriptElement = document.getElementById('gs-profile-email-settings-script');
    addId = scriptElement.getAttribute('data-add');
    adder = GSProfileEmailSettingsAdd(addId);
});
