jQuery.noConflict();

function GSEmailSettingsUpdate() {
    return {
        updateDelivery: function () {
            // Copy each addresses in the Default Addresses list to the
            // newDeliveries variable
            var newDeliveries = "";
            jQuery("#delivery-addresses").children().children(".email").each(function () {
                newDeliveries += jQuery(this).text() + "\n";
            });
            // Set the text of the hidden deliveryAddresses form element
            // to the default addresses text.
            jQuery("#form\\.deliveryAddresses").text(newDeliveries);
        },
        updateOther: function () {
            // Now do the same for the "other" addresses
            var newOthers = "";
            jQuery("#other-addresses").children().children(".email").each(function () {
                newOthers += jQuery(this).text() + "\n";
            });
            jQuery("#form\\.otherAddresses").text(newOthers);
        },
        updateUnverified: function () {
            // Aaaand for the unverified addresses
            var newUnverified = "";
            jQuery("#unverified-addresses").children().children(".email").each(function () {
                newUnverified += jQuery(this).text() + "\n";
            });
            jQuery("#form\\.unverifiedAddresses").text(newUnverified);
        }
    };
}//GSEmailSettingsUpdate

function GSEmailSettings() {
    var updater = null,
        dialog = null, 
        verificationAddress = null, 
        changeButton = null,
        deliveryAddresses = null, 
        otherAddresses = null;
    
    function updateAddresses() {
        updater.updateDelivery();
        updater.updateOther();
        updater.updateUnverified();
    
        // Blank the resend verification address. If this needs to be
        // set the resendVerification function will handle it.
        verificationAddress.val('');
    
        // Submit the form\\.
        changeButton.click();
    }
  
    function showDialog() {
        dialog.dialog("open");
    }
    
    function resendVerification() {
        var email = null;
        updater.updateDelivery();
        updater.updateOther();
        updater.updateUnverified();
        email = jQuery(this).parents('li').find('.email').text();
        verificationAddress.val(email);
        // Submit the form\\.
        changeButton.click();
    }
    
    function removeAddr() {
        jQuery(this).parents('li').remove();
        updateAddresses();
    }

    function highlightDelivery(event, ui) {
        deliveryAddresses.addClass("ui-state-hover");
    }

    function lowlightDelivery(event, ui) {
        deliveryAddresses.removeClass("ui-state-hover");
    }

    function highlightOther(event, ui) {
        otherAddresses.addClass("ui-state-hover");
    }

    function lowlightOther(event, ui) {
        otherAddresses.removeClass("ui-state-hover");
    }

    function start () {
        updater = GSEmailSettingsUpdate();
        dialog = jQuery('#add-email-address-dialog');
        verificationAddress = jQuery('#form\\.resendVerificationAddress');
        changeButton = jQuery("#form\\.actions\\.change");
        deliveryAddresses = jQuery('#delivery-addresses');
        otherAddresses = jQuery('#other-addresses');
    }
    start();  // Note the automatic execution

    return {
        init: function () {
            var o = null;

            deliveryAddresses.sortable({
                connectWith: "#other-addresses",
                update: updateAddresses,
                cancel: ".ui-state-disabled",
                start: highlightOther,
                stop: lowlightOther
            }).disableSelection();
            
            otherAddresses.sortable({
                connectWith: "#delivery-addresses",
                update: updateAddresses,
                start: highlightDelivery,
                stop: lowlightDelivery
            }).disableSelection();
            
            // Add dialog
            o = { autoOpen: false, minHeight: 190, modal: true,
                  dialogClass: 'gs-content-js-jqueryui' };
            dialog.dialog(o);
            jQuery('#open-add')
                .button({ icons: {primary:'ui-icon-plusthick'}})
                .removeAttr('href')
                .click(showDialog);
            jQuery('#form\\.actions\\.add')
                .button({ icons: {primary:'ui-icon-plusthick'}});
            jQuery('.removeLink')
                .button({ icons: {primary:'ui-icon-minusthick'}})
                .removeAttr('href')
                .click(removeAddr);
            jQuery('.resendLink')
                .button({ icons: {primary:'ui-icon-mail-closed'}})
                .removeAttr('href')
                .click(resendVerification);
        }
    };
} //GSEmailSettings.

// Check to see if the newly added email addresses have become verified.
function GSCheckVerified() {
    var email = null, 
        URI = 'checkemailverified.ajax', 
        TIMEOUT_DELTA = 2000, 
        updater = GSEmailSettingsUpdate();

  return {
      init: function () {
      },
      poll: function () {
          jQuery("#unverified-addresses")
              .children().children(".email").each(function () {
                  var e = null, d = null;
                  e = jQuery(this).text();
                  d = {type: "POST",
                       url: URI, 
                       cache: false,
                       data: 'email='+encodeURIComponent(e),
                       success: GSCheckVerified.checkReturn}
                  jQuery.ajax(d);
              });
      },
      checkReturn: function (data, textStatus) {
          var verified = data == '1', otherAddresses = null, newItem = null;
          if ( verified ) {
              //TODO: FIX
              newItem = '<li><samp class="email">'+email+'</samp></li>';
              otherAddresses = jQuery("#other-addresses");
              otherAddresses.append(newItem);
              updater.updateOther();
              // The Unverified addresses should not need to be updated.
              jQuery("#form\\.actions\\.change").click();
          } else {
              setTimeout(function () {GSCheckVerified.poll()}, TIMEOUT_DELTA);
          }
      }
  };
} //GSCheckVerified

jQuery(window).load(function () {
    var settings = null, checker = null;
    settings = GSEmailSettings();
    settings.init();

    checker = GSCheckVerified();
    checker.poll();
});
