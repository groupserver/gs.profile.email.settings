jQuery.noConflict();
GSCheckVerified = function () {
  var email = null;
  var URI = 'checkemailverified.ajax';
  var TIMEOUT_DELTA = 2000

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
      if (verified) {
        otherAddresses = jQuery("#form\\.otherAddresses").text();
        otherAddresses += email;
        jQuery("#form\\.otherAddresses").text(otherAddresses);
        jQuery("#form\\.actions\\.change").click();
      } else {
        setTimeout("GSCheckVerified.poll()", TIMEOUT_DELTA);
      }
    }
  };
}(); //GSCheckVerified

