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

/** Calculate a hash so we can create IDs for email addresses.
    @return {Int32}
*/
String.prototype.hashCode = function() {
    // http://stackoverflow.com/a/7616484
    // Modified to make Dijkstra happy
    var hash = 0, i = null, chr = null, len = null;
    if (this.length != 0) {
        for (i = 0, len = this.length; i < len; i++) {
            chr = this.charCodeAt(i);
            hash = ((hash << 5) - hash) + chr;
            hash |= 0; // Convert to 32bit integer
        }
    }
    return hash;
};


function GSProfileEmailSettingsUpdate(modelSelector, preferredSelector,
                                      extraSelector, unverifiedSelector) {
    var model = null, preferred = null, extra = null, unverified = null,
        addresses = null;

    function findItem(element) {
        var retval = null;
        retval = element;
        while (retval != null) {
            if (retval.tagName.toLowerCase() == 'li') {
                break;
            }
            retval = retval.parentElement;
        }
        return retval;
    } // findItem

    function removeClicked(event) {
        var button = null, listItem = null, email = null, formData = null,
            request = null;
        button = event.target;
        listItem = findItem(button);
        email = listItem.querySelector('code.email').textContent;

        formData = new FormData();
        formData.append('email', email);
        formData.append('delete', 'Delete');

        request = new XMLHttpRequest();
        request.addEventListener('load', removed);
        request.open('POST', 'gs-profile-email-settings-delete.json');
        request.send(formData);
        console.log(email);
    } // removeClicked

    function removed(event) {
        var jsonResponse = null;
        jsonResponse = JSON.parse(this.responseText);
        // TODO: message, error
        setAll(jsonResponse.email);
    }// removed


    function preferredClicked(event) {
        var button = null, listItem = null, email = null, formData = null,
            request = null;
        button = event.target;
        listItem = findItem(button);
        email = listItem.querySelector('code.email').textContent;

        formData = new FormData();
        formData.append('email', email);
        formData.append('prefer', 'Prefer');

        request = new XMLHttpRequest();
        request.addEventListener('load', preferredLoaded);
        request.open('POST', 'gs-profile-email-settings-prefer.json');
        request.send(formData);
    } // preferredClicked

    function preferredLoaded(event) {
        var jsonResponse = null;
        jsonResponse = JSON.parse(this.responseText);
        // TODO: message, error
        setAll(jsonResponse.email);
    } // preferredLoaded

    function demoteClicked(event) {
        var button = null, listItem = null, email = null, formData = null,
            request = null;
        button = event.target;
        listItem = findItem(button);
        email = listItem.querySelector('code.email').textContent;

        formData = new FormData();
        formData.append('email', email);
        formData.append('demote', 'Demote');

        request = new XMLHttpRequest();
        request.addEventListener('load', demoteLoaded);
        request.open('POST', 'gs-profile-email-settings-demote.json');
        request.send(formData);
    } // demoteClicked

    function demoteLoaded(event) {
        var jsonResponse = null;
        jsonResponse = JSON.parse(this.responseText);
        // TODO: message, error
        setAll(jsonResponse.email);
    } // demoteLoaded

    function createPreferredItem(addr, multiple) {
        var retval = null, toolbar = null;
        retval = model.querySelector('.preferred-address').cloneNode(true);
        retval.setAttribute('id', 'email' + addr.hashCode());
        retval.querySelector('.email').textContent = addr;
        if (multiple) {
            retval.querySelector('.demote').addEventListener(
                'click', demoteClicked);
            retval.querySelector('.remove').addEventListener(
                'click', removeClicked);
        } else { // One is the lonliest number
            toolbar = retval.querySelector('[role="toolbar"]');
            retval.removeChild(toolbar);
        }
        return retval;
    } // createPreferredItem

    function setPreferred(preferredAddrs) {
        var i = 0, element = null, multiple = false, list = null;
        list = preferred.getElementsByTagName('ul')[0];  // There is only one
        multiple = (preferredAddrs.length > 1);
        for (i in preferredAddrs) {
            element = createPreferredItem(preferredAddrs[i], multiple);
            list.appendChild(element);
        }
    } // setPreferred

    function createExtraItem(addr) {
        var retval = null;
        retval = model.querySelector('.extra-address').cloneNode(true);
        retval.setAttribute('id', 'email' + addr.hashCode());
        retval.querySelector('.email').textContent = addr;
        retval.querySelector('.prefer').addEventListener(
                'click', preferredClicked);
        retval.querySelector('.remove').addEventListener(
                'click', removeClicked);
        return retval;
    }// createExtraItem

    function setExtra(extraAddrs) {
        var i = 0, element = null, list = null;
        list = extra.getElementsByTagName('ul')[0];  // There is only one
        for (i in extraAddrs) {
            element = createExtraItem(extraAddrs[i]);
            list.appendChild(element);
        }
    } // setExtra

    function verifyClicked(event) {
        var button = null, listItem = null, email = null, formData = null,
            request = null;
        button = event.target;
        listItem = findItem(button);
        email = listItem.querySelector('code.email').textContent;

        formData = new FormData();
        formData.append('email', email);
        formData.append('resend', 'Resend');

        request = new XMLHttpRequest();
        request.addEventListener('load', verifyLoaded);
        request.open('POST', 'gs-profile-email-settings-resend.json');
        request.send(formData);
    } // verifyClicked

    function verifyLoaded(event) {
        var jsonResponse = null;
        jsonResponse = JSON.parse(this.responseText);
        // TODO: message, error
        setAll(jsonResponse.email);
    } // verifiyLoaded

    function createUnverifiedItem(addr) {
        var retval = null;
        retval = model.querySelector('.unverified-address').cloneNode(true);
        retval.setAttribute('id', 'email' + addr.hashCode());
        retval.querySelector('.email').textContent = addr;
        retval.querySelector('.verify').addEventListener(
                'click', verifyClicked);
        retval.querySelector('.remove').addEventListener(
                'click', removeClicked);
        return retval;
    } // createUnverifiedItem

    function setUnverified(unverifiedAddrs) {
        var i = 0, element = null, list = null;
        list = unverified.getElementsByTagName('ul')[0];  // There is only one
        for (i in unverifiedAddrs) {
            element = createUnverifiedItem(unverifiedAddrs[i]);
            list.appendChild(element);
        }
    } // setUnverified

    function clear(list) {
        while (list.firstChild) {
            list.removeChild(list.firstChild);
        }
    } // clear

    function clearAll() {
        clear(preferred.querySelector('ul'));
        clear(extra.querySelector('ul'));
        clear(unverified.querySelector('ul'));
        addresses = null;
    } // clearAll

    function setAll(addresses) {
        clearAll();
        setPreferred(addresses.preferred);
        setExtra(addresses.other);
        setUnverified(addresses.unverified);
        addresses = addresses;
    } // setAll

    function setUp() {
        model = document.querySelector(modelSelector);
        preferred = document.querySelector(preferredSelector);
        extra = document.querySelector(extraSelector);
        unverified = document.querySelector(unverifiedSelector);
    } // setUp
    setUp(); // Automatic exectution

    return {
        setAddresses: function(addresses) {
            setAll(addresses);
        }, // setAddresses
        getAddresses: function() {return addresses;}
    };
}

function GSProfileEmailSettingsAdd(addSelector, updater) {
    var add = null, input = null, button = null;

    function inputChanged(event) {
        if ((input.value.length > 0) &&
            button.hasAttribute('disabled') &&
            (!('validity' in input) || input.validity.valid)) {
            button.removeAttribute('disabled');
        } else if ((event.key == 'Enter') &&
                   !button.hasAttribute('disabled')) {
            button.click();
        } else if (!button.hasAttribute('disabled') &&
                   (input.value.length == 0) ||
                   (('validity' in input) && !input.validity.valid)) {
            button.setAttribute('disabled', 'disabled');
        }
    }// inputChanged

    function added(event) {
        var jsonResponse = null;
        jsonResponse = JSON.parse(this.responseText);
        // TODO: message, error
        updater.setAddresses(jsonResponse.email);
        input.value = '';
        input.removeAttribute('disabled');
    } // added

    function addClicked(event) {
        var request = null, formData = null;
        input.setAttribute('disabled', 'disabled');

        formData = new FormData();
        formData.append('email', input.value);
        formData.append('add', 'Add'); // The button

        request = new XMLHttpRequest();
        request.addEventListener('load', added);
        request.open('POST', 'gs-profile-email-settings-add.json');
        request.send(formData);
    }// addClicked

    function setUp() {
        add = document.querySelector(addSelector);
        input = add.getElementsByTagName('input')[0];  // There is only one
        input.addEventListener('keyup', inputChanged);

        button = add.getElementsByTagName('button')[0];
        button.setAttribute('disabled', 'disabled');
        button.addEventListener('click', addClicked);
    } // setUp
    setUp(); // Note the automatic execution
}

function gs_profile_email_settings_load(updater) {
    var request = null;

    function loaded(event) {
        var jsonResponse = null;
        jsonResponse = JSON.parse(this.responseText);
        updater.setAddresses(jsonResponse);
    }

    request = new XMLHttpRequest();
    request.addEventListener('load', loaded);
    request.open('GET', 'gs-profile-email-settings-status.json');
    request.send();
}

window.addEventListener('load', function(event) {
    var scriptElement = null, updater = null, adder = null;
    scriptElement = document.getElementById('gs-profile-email-settings-script');
    updater = GSProfileEmailSettingsUpdate(
        scriptElement.getAttribute('data-model'),
        scriptElement.getAttribute('data-preferred'),
        scriptElement.getAttribute('data-extra'),
        scriptElement.getAttribute('data-unverified'));
    gs_profile_email_settings_load(updater);

    adder = GSProfileEmailSettingsAdd(scriptElement.getAttribute('data-add'),
                                      updater);
});
