jQuery.noConflict();

GSEmailSettingsUpdate = function () {
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

GSEmailSettings = function () {
  var updater = GSEmailSettingsUpdate()
  var updateAddresses = function () {
    updater.updateDelivery();
    updater.updateOther();
    updater.updateUnverified();
    
    // Blank the resend verification address. If this needs to be
    // set the resendVerification function will handle it.
    jQuery('#form\\.resendVerificationAddress').val('');
    
    // Submit the form\\.
    jQuery("#form\\.actions\\.change").click();
  };
  
  var showDialog = function () {
    jQuery('#add-email-address-dialog').dialog("open");
  };
  
  var resendVerification = function () {
    var email = null;
    updater.updateDelivery();
    updater.updateOther();
    updater.updateUnverified();
    email = jQuery(this).parents('li').find('.email').text();
    jQuery('#form\\.resendVerificationAddress').val(email);
    // Submit the form\\.
    jQuery("#form\\.actions\\.change").click();
  }
  
  var removeAddr = function () {
    jQuery(this).parents('li').remove();
    updateAddresses();
  }

  var highlightDelivery = function(event, ui) {
    jQuery('#delivery-addresses').addClass("ui-state-hover");
  }
  var lowlightDelivery = function(event, ui) {
    jQuery('#delivery-addresses').removeClass("ui-state-hover");
  }
  var highlightOther = function(event, ui) {
    jQuery('#other-addresses').addClass("ui-state-hover");
  }
  var lowlightOther = function(event, ui) {
    jQuery('#other-addresses').removeClass("ui-state-hover");
  }

  return {
    init: function () {
      jQuery("#delivery-addresses").sortable({
        connectWith: "#other-addresses",
        update: updateAddresses,
        cancel: ".ui-state-disabled",
        start: highlightOther,
        stop: lowlightOther
      }).disableSelection();
      
      jQuery("#other-addresses").sortable({
        connectWith: "#delivery-addresses",
        update: updateAddresses,
        start: highlightDelivery,
        stop: lowlightDelivery
      }).disableSelection();
      
      // Add dialog
      var o = { autoOpen: false, minWidth: 516, modal: true };
      jQuery('#add-email-address-dialog').dialog(o);
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
}(); //GSEmailSettings

// Check to see if the newly added email addresses have become verified.
GSCheckVerified = function () {
  var email = null;
  var URI = 'checkemailverified.ajax';
  var TIMEOUT_DELTA = 2000

  var updater = GSEmailSettingsUpdate();

  return {
    init: function () {
    },
    poll: function () {
      jQuery("#unverified-addresses").children().children(".email").each(function () {
        email = jQuery(this).text()
        jQuery.ajax({
          type: "POST",
          url: URI, 
          cache: false,
          data: 'email='+encodeURIComponent(email),
          success: GSCheckVerified.checkReturn});
       });
    },
    checkReturn: function (data, textStatus) {
      var verified = data == '1';
      var otherAddresses = null
      var newItem = null;
      if (verified) {
        //TODO: FIX
        newItem = '<li><samp class="email">'+email+'</samp></li>';
        otherAddresses = jQuery("#other-addresses");
        otherAddresses.append(newItem);
        updater.updateOther();
        // The Unverified addresses should not need to be updated.
        jQuery("#form\\.actions\\.change").click();
      } else {
        setTimeout(function () { GSCheckVerified.poll(); }, TIMEOUT_DELTA);
      }
    }
  };
}(); //GSCheckVerified

