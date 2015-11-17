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

function GSProfileEmailSettingsUpdate(modelSelector, preferredSelector, 
                                      otherSelector, unverifiedSelector) {
    var model = null, preferred = null, other = null, unverified = null, 
        addresses = null, ITEM_CLASS = 'gs-profile-email-settings-item';

    function createItem(addr) {
        var retval = null, code = null;
        code = document.createElement('code');
        code.className = 'email';
        code.textContent = addr;

        retval = document.createElement('li');
        retval.className = ITEM_CLASS;
        retval.appendChild(code);
        return retval;
    }

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
    }

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
    }

    function preferredLoaded(event) {
        var jsonResponse = null;
        jsonResponse = JSON.parse(this.responseText);
        // TODO: message, error
        setAll(jsonResponse.email);
    }

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
    }

    function demoteLoaded(event) {
        var jsonResponse = null;
        jsonResponse = JSON.parse(this.responseText);
        // TODO: message, error
        setAll(jsonResponse.email);
    }

    function createPreferredItem(addr, multiple) {
        var retval = null;
        retval = model.querySelector('.preferred-address').cloneNode(true);
        retval.querySelector('.email').textContent = addr;
        if (multiple) {
            retval.querySelector('.demote').onclick = demoteClicked
            retval.querySelector('.remove').onclick = removeClicked;
        }
        return retval;
    }

    function setPreferred(preferredAddrs) {
        var i = 0, element = null, multiple = false, list = null;
        list = preferred.getElementsByTagName('ul')[0];  // There is only one
        multiple = (preferredAddrs.length > 1);
        for (i in preferredAddrs) {
            element = createPreferredItem(preferredAddrs[i], multiple);
            list.appendChild(element);
        }
    } // setPreferred

    function createOtherItem(addr) {
        var retval = null;
        retval = model.querySelector('.extra-address').cloneNode(true);
        retval.querySelector('.email').textContent = addr;
        retval.querySelector('.prefer').onclick = preferredClicked;
        retval.querySelector('.remove').onclick = removeClicked;
        return retval;
    }// createOtherItem

    function setOther(otherAddrs) {
        var i = 0, element = null, list = null;
        list = other.getElementsByTagName('ul')[0];  // There is only one
        for (i in otherAddrs) {
            element = createOtherItem(otherAddrs[i]);
            list.appendChild(element);
        }
    } // setOther

    function createUnverifiedItem(addr) {
        var retval = null;
        retval = model.querySelector('.extra-address').cloneNode(true);
        retval.querySelector('.email').textContent = addr;
        retval.querySelector('.verify').onclick = verifyClicked;
        retval.querySelector('.remove').onclick = removeClicked;
        return retval;
    }

    function setUnverified(unverifiedAddrs) {
        var i = 0, element = null;
        for (i in unverifiedAddrs) {
            element = createUnverifiedItem(unverifiedAddrs[i]);
            unverified.appendChild(element);
        }
    } // setUnverified

    function clearAll() {
        clear(preferred.querySelector('ul'));
        clear(other.querySelector('ul'));
        clear(unverified.querySelector('ul'));
        addresses = null;
    } // clearAll

    function setAll(addresses) {
        clearAll();
        setPreferred(addresses.preferred);
        setOther(addresses.other);
        //setUnverified(addresses.unverified);
        addresses = addresses;
    } // setAll

    function setUp() {
        model = document.querySelector(modelSelector);
        preferred = document.querySelector(preferredSelector);
        other = document.querySelector(otherSelector);
        unverified = document.querySelector(unverifiedSelector);
    } // setUp
    setUp(); // Automatic exectution

    function clear(list) {
        while (list.firstChild) {
            list.removeChild(list.firstChild);
        }
    } // clear


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
        input.onkeyup = inputChanged;

        button = add.getElementsByTagName('button')[0];
        button.setAttribute('disabled', 'disabled');
        button.onclick = addClicked;
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

jQuery(window).load(function() {
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
