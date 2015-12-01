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
}; // String.prototype.hashCode

/** The message area
 * @constructor
 * @param {String} messageBoxSelector - The selector for the message box
 */
function GSProfileEmailSettingsMessage(messageBoxSelector) {
    this.messageBox = document.querySelector(messageBoxSelector);
    this.OK = '';
    this.ERROR = 'alert-error';
    this.SUCCESS = 'alert-success';
    this.INFO = 'alert-info';
}
/** Clear the previous message */
GSProfileEmailSettingsMessage.prototype.clearMessage = function() {
    while (this.messageBox.firstChild) {
        this.messageBox.removeChild(this.messageBox.firstChild);
    }
}; // clearMessage
/** Set a message
 * @param {String} html - The HTML to display
 * @param {String} errorLevel - The Twitter Bootstrap alert error-level
 */
GSProfileEmailSettingsMessage.prototype.setMessage =
    function(html, errorLevel) {
        var alert = null, msg = null, button = null;
        alert = document.createElement('div');
        alert.setAttribute('class', 'alert alert-block fade in' + errorLevel);
        button = document.createElement('button');
        button.setAttribute('type', 'button');
        button.setAttribute('class', 'close');
        button.setAttribute('data-dismiss', 'alert');
        button.textContent = '\u00D7';
        alert.appendChild(button);
        msg = document.createElement('div');
        msg.innerHTML = html;
        alert.appendChild(msg);
        this.messageBox.appendChild(alert);
    }; // setMessage
/** Display a new message, clearing the other message first
 * @param {String} message - The HTML-formatted message to display
 * @param {String} errorLevel - The Twitter Bootstrap alert error-level
 */
GSProfileEmailSettingsMessage.prototype.display =
    function(message, errorLevel) {
        var e = null;
        e = typeof(errorLevel) !== 'undefined' ? ' ' + errorLevel : this.OK;
        this.clearMessage();
        this.setMessage(message, e);
    }; // display

function GSProfileEmailSettingsAJAX() {
    var removeEndpoint = null, preferEndpoint = null, demoteEndpoint = null,
        resendEndpoint = null, addEndpoint = null;

    function AjaxEndpoint(uri, buttonName, buttonValue) {
        function AjaxRequest(listener) {
            var r = null;
            r = new XMLHttpRequest();
            if (typeof(listener) !== 'undefined') {
                r.addEventListener('load', listener);
            }
            r.open('POST', uri);
            return r;
        } // AjaxRequest

        return {
            send: function(address, listener) {
                var request = null, formData = null;
                formData = new FormData();
                formData.append(buttonName, buttonValue);
                formData.append('email', address);

                request = new AjaxRequest(listener);
                request.send(formData);
            }
        };
    } // AjaxEndpoint

    function getStatus(listener) {
        var request = null;
        request = new XMLHttpRequest();
        if (typeof(request) !== 'undefined') {
            request.addEventListener('load', listener);
        }
        request.open('GET', 'gs-profile-email-settings-status.json');
        request.send();
    } // getStatus

    function setUp() {
        removeEndpoint = new AjaxEndpoint(
            'gs-profile-email-settings-delete.json', 'delete', 'Delete');
        preferEndpoint = new AjaxEndpoint(
            'gs-profile-email-settings-prefer.json', 'prefer',
            'Prefer');
        demoteEndpoint = new AjaxEndpoint(
            'gs-profile-email-settings-demote.json', 'demote',
            'Demote');
        resendEndpoint = new AjaxEndpoint(
            'gs-profile-email-settings-resend.json', 'resend',
            'Resend');
        addEndpoint = new AjaxEndpoint(
            'gs-profile-email-settings-add.json', 'add', 'Add');
    }
    setUp(); // Automatic execution

    return {
        remove: function(address, listener) {
            removeEndpoint.send(address, listener);
        },
        prefer: function(address, listener) {
            preferEndpoint.send(address, listener);
        },
        demote: function(address, listener) {
            demoteEndpoint.send(address, listener);
        },
        resend: function(address, listener) {
            resendEndpoint.send(address, listener);
        },
        add: function(address, listener) {
            addEndpoint.send(address, listener);
        },
        status: function(listener) {
            getStatus(listener);
        }
    };
} // GSProfileEmailSettingsAJAX


// --=mpj17=-- The event uses the old API for creating events,
// because IE (10 & 11) only support this API, rather than the
// new event creation.
function GSProfileEmailSettingsRemoveEvent(data) {
    var evt = document.createEvent('CustomEvent');
    evt.initCustomEvent('GSProfileEmailSettingsRemove', true, true, data);
    return evt;
} // GSProfileEmailSettingsRemoveEvent


/** Abstract base-class for the settings areas
 * @constructor
 * @param {Element} elem - The HTML element for the area
 * @param {Element} model - The HTML element for the list-item models
 *
 * Concrete impmentations of a settings area should implement an
 * update method.
 */
function GSProfileEmailSettingsArea(elem, model) {
    this.elem = elem;
    this.list = elem.getElementsByTagName('ul')[0];  // There is only one
    this.model = model;
}
/** Find a list-item starting at an element
 * @param {Element} element The HTML element where the search starts.
 * @return {Element} The HTML element for the list-item.
 */
GSProfileEmailSettingsArea.prototype.findItem = function(element) {
    var retval = null;
    retval = element;
    while (retval != null) {
        if (retval.tagName.toLowerCase() == 'li') {
            break;
        }
        retval = retval.parentElement;
    }
    return retval;
}; // findItem
/** Clear the list */
GSProfileEmailSettingsArea.prototype.clear = function() {
    while (this.list.firstChild) {
        this.list.removeChild(this.list.firstChild);
    }
}; // clear
/** Find the email address associated with an event.
 * @param {Event} event The HTML event that triggered the search
 * @return {String} The email address in the list-item.
 */
GSProfileEmailSettingsArea.prototype.emailFromEvent = function(event) {
    var button = null, listItem = null, retval = null;
    button = event.target;
    listItem = this.findItem(button);
    retval = listItem.querySelector('code.email').textContent;
    return retval;
}; // emailFromEvent
/** Handle the Remove button being clicked
 * @param {Event} event The HTML click-event on the Remove button
 */
GSProfileEmailSettingsArea.prototype.removeClicked = function(event) {
    var email = null, removeEvent = null;
    email = this.emailFromEvent(event);
    removeEvent = GSProfileEmailSettingsRemoveEvent({'email': email});
    event.target.dispatchEvent(removeEvent);
}; // removeClicked
/** Does the drag-n-drop event contain a GroupServer address
 * @param {Event} event The HTML event
 * @return (Boolean} True if the event contains "application/x-gs-address" data
 */
GSProfileEmailSettingsArea.prototype.isAddr = function(event) {
    var retval = false;
    for( var i = 0; i < event.dataTransfer.types.length; ++i )
    {
        if(event.dataTransfer.types[i] === "application/x-gs-address")
            retval = true;
    }
    return retval;
} // isAddr

function GSProfileEmailSettingsPreferEvent(data) {
    var evt = document.createEvent('CustomEvent');
    evt.initCustomEvent('GSProfileEmailSettingsPrefer', true, true, data);
    return evt;
} // GSProfileEmailSettingsPreferEvent

function GSProfileEmailSettingsDemoteEvent(data) {
    var evt = document.createEvent('CustomEvent');
    evt.initCustomEvent('GSProfileEmailSettingsDemote', true, true, data);
    return evt;
} // GSProfileEmailSettingsDemoteEvent

function GSProfileEmailPreferDragStart(data) {
    var evt = document.createEvent('CustomEvent');
    evt.initCustomEvent('GSProfileEmailPreferDragStart', true, true, data);
    return evt;
} // GSProfileEmailPreferDragStart

/** Area for the preferred email-addresses.
 * @constructor
 * @extends GSProfileEmailSettingsArea
 * @param {Element} elem - The HTML element for the area
 * @param {Element} model - The HTML element for the list-item models
*/
function GSProfileEmailSettingsPreferred(elem, model) {
    GSProfileEmailSettingsArea.call(this, elem, model);
    elem.addEventListener('dragover', this.dragOver.bind(this));
    elem.addEventListener('drop', this.drop.bind(this));
}
GSProfileEmailSettingsPreferred.prototype =
    Object.create(GSProfileEmailSettingsArea.prototype);
/** Why? */
GSProfileEmailSettingsPreferred.prototype.constructor =
    GSProfileEmailSettingsPreferred;
/** Handle the Demote button being clicked
 * @param {Event} event The HTML click-event on the Demote button
 */
GSProfileEmailSettingsPreferred.prototype.demoteClicked = function(event) {
    var email = null, demoteEvent = null;
    email = this.emailFromEvent(event);
    demoteEvent = GSProfileEmailSettingsDemoteEvent({'email': email});
    event.target.dispatchEvent(demoteEvent);
}; // demoteClicked
GSProfileEmailSettingsPreferred.prototype.dragOver = function(event) {
    if (this.isAddr(event)) {
        event.preventDefault();  // Announce that we will handle the drop
    }
}// dragOver
GSProfileEmailSettingsPreferred.prototype.drop = function(event) {
    var email = null, preferEvent = null;
    event.preventDefault();
    email = event.dataTransfer.getData('application/x-gs-address');
    preferEvent = GSProfileEmailSettingsPreferEvent({'email': email});
    event.target.dispatchEvent(preferEvent);
}// drop
GSProfileEmailSettingsPreferred.prototype.dragStart = function(event) {
    var email = null, dragStartEvent = null;
    email = this.emailFromEvent(event);
    event.dataTransfer.setData('application/x-gs-address', email);
    event.dataTransfer.effectAllowed = 'move';
    dragStartEvent = GSProfileEmailPreferDragStart();
    event.target.dispatchEvent(dragStartEvent);
}; // demoteClicked
/** Create an item for the Preferred address list
 * @param {String} addr The email address for the item
 * @param {Bool} multiple If there are multiple email addresses
 * @return {Element} An HTML element for the new item
 */
GSProfileEmailSettingsPreferred.prototype.createItem =
    function(addr, multiple) {
        var retval = null, email = null;
        retval = this.model.querySelector('.preferred-address').cloneNode(true);
        retval.setAttribute('id', 'email' + addr.hashCode());
        email = retval.querySelector('.email');
        email.textContent = addr;
        if (multiple) {
            // --=mpj17=-- Note the use of .bind(this) so the this in
            // this.demoteClicked is this this.
            retval.querySelector('.demote').addEventListener(
                'click', this.demoteClicked.bind(this));
            retval.querySelector('.remove').addEventListener(
                'click', this.removeClicked.bind(this));
            // We can drag 'n' drop if we have more than one preferred address
            email.setAttribute('draggable', 'true');
            email.addEventListener('dragstart', this.dragStart.bind(this));
        } else { // One is the lonliest number
            toolbar = retval.querySelector('[role="toolbar"]');
            retval.removeChild(toolbar);
        }
        return retval;
    }; // CreateItem
/** Update the preferred email-address list
 * @param {Object} data - The data containing the email addresses
 */
GSProfileEmailSettingsPreferred.prototype.update = function(data) {
    var newItem = null, multiple = false, i = 0;
    this.clear();
    multiple = (data.preferred.length > 1);
    for (i in data.preferred) {
        newItem = this.createItem(data.preferred[i], multiple);
        this.list.appendChild(newItem);
    }
}; // update


function GSProfileEmailExtraDragStart(data) {
    var evt = document.createEvent('CustomEvent');
    evt.initCustomEvent('GSProfileEmailExtraDragStart', true, true, data);
    return evt;
} // GSProfileEmailPreferDragStart


/** Area for the extra email-addresses.
 * @constructor
 * @extends GSProfileEmailSettingsArea
 * @param {Element} elem - The HTML element for the area
 * @param {Element} model - The HTML element for the list-item models
*/
function GSProfileEmailSettingsExtra(elem, model) {
    GSProfileEmailSettingsArea.call(this, elem, model);
    elem.addEventListener('dragover', this.dragOver.bind(this));
    elem.addEventListener('drop', this.drop.bind(this));
}
GSProfileEmailSettingsExtra.prototype =
    Object.create(GSProfileEmailSettingsArea.prototype);
/** Why? */
GSProfileEmailSettingsExtra.prototype.constructor =
    GSProfileEmailSettingsExtra;
/** Handle the Prefer button being clicked
 * @param {Event} event The HTML click-event on the Prefer button
 */
GSProfileEmailSettingsExtra.prototype.preferClicked = function(event) {
    var email = null, preferEvent = null;
    email = this.emailFromEvent(event);
    preferEvent = GSProfileEmailSettingsPreferEvent({'email': email});
    event.target.dispatchEvent(preferEvent);
}; // demoteClicked
/** Handle the an item being dragged over
 * @param {Event} event The HTML drag-event
 */
GSProfileEmailSettingsExtra.prototype.dragOver = function(event) {
    if (this.isAddr(event)) {
        event.preventDefault();  // Announce that we will handle the drop
    }
}; // dragOver
/** Handle an email being dropped
 * @param {Event} event The HTML drop event
 */
GSProfileEmailSettingsExtra.prototype.drop = function(event) {
    var email = null, preferEvent = null;
    event.preventDefault();
    email = event.dataTransfer.getData('application/x-gs-address');
    preferEvent = GSProfileEmailSettingsDemoteEvent({'email': email});
    event.target.dispatchEvent(preferEvent);
}; // drop
/** Handle an email being dropped
 * @param {Event} event The HTML drop event
 */
GSProfileEmailSettingsExtra.prototype.dragStart = function(event) {
    var email = null, dragStartEvent = null;
    email = this.emailFromEvent(event);
    event.dataTransfer.setData('application/x-gs-address', email);
    event.dataTransfer.effectAllowed = 'move';
    dragStartEvent = GSProfileEmailExtraDragStart();
    event.target.dispatchEvent(dragStartEvent);
}; // dragStart
/** Create an item for the Extra address list
 * @param {String} addr The email address for the item
 * @return {Element} An HTML element for the new item
 */
GSProfileEmailSettingsExtra.prototype.createItem = function(addr) {
    var retval = null, email = null;
    retval = this.model.querySelector('.extra-address').cloneNode(true);
    retval.setAttribute('id', 'email' + addr.hashCode());
    email = retval.querySelector('.email');
    email.textContent = addr;
    email.addEventListener('dragstart', this.dragStart.bind(this));
    retval.querySelector('.prefer').addEventListener(
        'click', this.preferClicked.bind(this));
    retval.querySelector('.remove').addEventListener(
        'click', this.removeClicked.bind(this));
    return retval;
    }; // createItem
/** Update the preferred email-address list
 * @param {Object} data - The data containing the email addresses
 */
GSProfileEmailSettingsExtra.prototype.update = function(data) {
    var newItem = null, i = 0;
    this.clear();
    for (i in data.other) {
        newItem = this.createItem(data.other[i]);
        this.list.appendChild(newItem);
    }
}; // update


function GSProfileEmailSettingsResendEvent(data) {
    var evt = document.createEvent('CustomEvent');
    evt.initCustomEvent('GSProfileEmailSettingsResend', true, true, data);
    return evt;
} // GSProfileEmailSettingsResendEvent


/** Area for the unverified email-addresses.
 * @constructor
 * @extends GSProfileEmailSettingsArea
 * @param {Element} elem - The HTML element for the area
 * @param {Element} model - The HTML element for the list-item models
*/
function GSProfileEmailSettingsUnverified(elem, model) {
    GSProfileEmailSettingsArea.call(this, elem, model);
}
GSProfileEmailSettingsUnverified.prototype =
    Object.create(GSProfileEmailSettingsArea.prototype);
/** Why? */
GSProfileEmailSettingsUnverified.prototype.constructor =
    GSProfileEmailSettingsUnverified;
/** Handle the Resend verification button being clicked
 * @param {Event} event The HTML click-event on the Resend verification button
 */
GSProfileEmailSettingsArea.prototype.verifyClicked = function(event) {
    var email = null, verifyEvent = null;
    email = this.emailFromEvent(event);
    verifyEvent = GSProfileEmailSettingsResendEvent({'email': email});
    event.target.dispatchEvent(verifyEvent);
}; // removeClicked
/** Create an item for the Unverified address list
 * @param {String} addr The email address for the item
 * @return {Element} An HTML element for the new item
 */
GSProfileEmailSettingsUnverified.prototype.createItem = function(addr) {
    var retval = null;
    retval = this.model.querySelector('.unverified-address').cloneNode(true);
    retval.setAttribute('id', 'email' + addr.hashCode());
    retval.querySelector('.email').textContent = addr;
    retval.querySelector('.verify').addEventListener(
        'click', this.verifyClicked.bind(this));
    retval.querySelector('.remove').addEventListener(
        'click', this.removeClicked.bind(this));
    return retval;
}; // createItem
/** Update the preferred email-address list
 * @param {Object} data - The data containing the email addresses
 */
GSProfileEmailSettingsUnverified.prototype.update = function(data) {
    var newItem = null, i = 0;
    this.clear();
    for (i in data.unverified) {
        newItem = this.createItem(data.unverified[i]);
        this.list.appendChild(newItem);
    }
}; // update


function GSProfileEmailSettingsAddEvent(data) {
    var evt = document.createEvent('CustomEvent');
    evt.initCustomEvent('GSProfileEmailSettingsAdd', true, true, data);
    return evt;
} // GSProfileEmailSettingsAddEvent


/** The area that allows email addresses to be added.
 * @constructor
 * @param {Element} elem - The HTML element for the area
 */
function GSProfileEmailSettingsAdd(elem) {
    this.elem = elem;
    this.input = elem.getElementsByTagName('input')[0];  // There is only one
    this.input.addEventListener('keyup', this.inputChanged.bind(this));
    this.button = elem.getElementsByTagName('button')[0];
    this.button.setAttribute('disabled', 'disabled');
    this.button.addEventListener('click', this.addClicked.bind(this));
} // GSProfileEmailSettingsAdd
/** Handle the text-entry being updated
 * @param {Event} event - The key-up event
 *
 * The button should only be enabled when there is valid input in
 * the text-entry.
 */
GSProfileEmailSettingsAdd.prototype.inputChanged = function(event) {
    if ((this.input.value.length > 0) &&
        this.button.hasAttribute('disabled') &&
        (!('validity' in this.input) || this.input.validity.valid)) {
        this.button.removeAttribute('disabled');
    } else if ((event.key == 'Enter') &&
               !this.button.hasAttribute('disabled')) {
        this.button.click();
    } else if (!this.button.hasAttribute('disabled') &&
               (this.input.value.length == 0) ||
               (('validity' in this.input) && !this.input.validity.valid)) {
        this.button.setAttribute('disabled', 'disabled');
    }
}; // inputChanged
/** Handle the Add buttom being clicked
 * @param {Event} event - The click event
 */
GSProfileEmailSettingsAdd.prototype.addClicked = function(event) {
    var request = null, formData = null, addEvent = null;
    this.input.setAttribute('disabled', 'disabled');
    addEvent = GSProfileEmailSettingsAddEvent({'email': this.input.value});
    event.target.dispatchEvent(addEvent);
}; // addClicked
/** Reset the form
 */
GSProfileEmailSettingsAdd.prototype.reset = function() {
    this.input.value = '';
    this.input.removeAttribute('disabled');
}; // reset


function GSProfileEmailSettingsUpdate(
    preferredSelector, extraSelector, unverifiedSelector, addSelector,
    modelSelector, messageBoxSelector) {
    var settingsAjax = null, preferred = null, extra = null, unverified = null,
        messageBox = null, adder = null;

    function load(event) {
        var jsonResponse = null;
        jsonResponse = JSON.parse(event.target.responseText);
        updateAll(jsonResponse);
    } // load

    function updateAll(addrs) {
        preferred.update(addrs);
        extra.update(addrs);
        unverified.update(addrs);
    }

    function remove(event) {
        settingsAjax.remove(event.detail.email, ajaxReturn);
    }

    function prefer(event) {
        settingsAjax.prefer(event.detail.email, ajaxReturn);
    }

    function demote(event) {
        settingsAjax.demote(event.detail.email, ajaxReturn);
    }

    function resend(event) {
        settingsAjax.resend(event.detail.email, ajaxReturn);
    }

    function ajaxReturn(event) {
        var jsonResponse = null;
        jsonResponse = JSON.parse(event.target.responseText);
        // TODO: error
        messageBox.display(jsonResponse.message);
        updateAll(jsonResponse.email);
    }

    function add(event) {
        settingsAjax.add(event.detail.email, addAjaxReturn);
    }

    function addAjaxReturn(event) {
        var jsonResponse = null;
        jsonResponse = JSON.parse(this.responseText);
        messageBox.display(jsonResponse.message, messageBox.SUCCESS);
        // TODO: error
        updateAll(jsonResponse.email);
        adder.reset();
    } // addReturn

    function setUp() {
        var prefElem = null, extraElem = null, unverifiedElem = null,
            addElem = null, modelElem = null;
        messageBox = new GSProfileEmailSettingsMessage(messageBoxSelector);

        modelElem = document.querySelector(modelSelector);

        prefElem = document.querySelector(preferredSelector);
        prefElem.addEventListener('GSProfileEmailSettingsRemove', remove);
        prefElem.addEventListener('GSProfileEmailSettingsPrefer', prefer);
        prefElem.addEventListener('GSProfileEmailSettingsDemote', demote);
        preferred = new GSProfileEmailSettingsPreferred(prefElem, modelElem);

        extraElem = document.querySelector(extraSelector);
        extraElem.addEventListener('GSProfileEmailSettingsRemove', remove);
        extraElem.addEventListener('GSProfileEmailSettingsPrefer', prefer);
        extraElem.addEventListener('GSProfileEmailSettingsDemote', demote);
        extra = new GSProfileEmailSettingsExtra(extraElem, modelElem);

        unverifiedElem = document.querySelector(unverifiedSelector);
        unverifiedElem.addEventListener('GSProfileEmailSettingsRemove', remove);
        unverifiedElem.addEventListener('GSProfileEmailSettingsResend', resend);
        unverified = new GSProfileEmailSettingsUnverified(unverifiedElem,
                                                          modelElem);

        addElem = document.querySelector(addSelector);
        adder = new GSProfileEmailSettingsAdd(addElem);
        addElem.addEventListener('GSProfileEmailSettingsAdd', add);

        settingsAjax = new GSProfileEmailSettingsAJAX();
        settingsAjax.status(load);
    }
    setUp(); // Note the automatic execution
}


window.addEventListener('load', function(event) {
    var scriptElement = null, updater = null;
    scriptElement = document.getElementById('gs-profile-email-settings-script');
    updater = GSProfileEmailSettingsUpdate(
        scriptElement.getAttribute('data-preferred'),
        scriptElement.getAttribute('data-extra'),
        scriptElement.getAttribute('data-unverified'),
        scriptElement.getAttribute('data-add'),
        scriptElement.getAttribute('data-model'),
        scriptElement.getAttribute('data-messagebox'));
});
