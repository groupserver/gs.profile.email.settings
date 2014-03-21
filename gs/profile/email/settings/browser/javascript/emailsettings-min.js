"use strict";jQuery.noConflict();function GSEmailSettingsUpdate(){return{updateDelivery:function(){var a="";
jQuery("#delivery-addresses").children().children(".email").each(function(){a+=jQuery(this).text()+"\n"
});jQuery("#form\\.deliveryAddresses").text(a)},updateOther:function(){var a="";jQuery("#other-addresses").children().children(".email").each(function(){a+=jQuery(this).text()+"\n"
});jQuery("#form\\.otherAddresses").text(a)},updateUnverified:function(){var a="";
jQuery("#unverified-addresses").children().children(".email").each(function(){a+=jQuery(this).text()+"\n"
});jQuery("#form\\.unverifiedAddresses").text(a)}}}function GSEmailSettings(){var o=null,i=null,m=null,k=null,c=null,g=null;
function b(){o.updateDelivery();o.updateOther();o.updateUnverified();m.val("");k.click()
}function l(){i.dialog("open")}function n(){var p=null;o.updateDelivery();o.updateOther();
o.updateUnverified();p=jQuery(this).parents("li").find(".email").text();m.val(p);
k.click()}function h(){jQuery(this).parents("li").remove();b()}function e(p,q){c.addClass("ui-state-hover")
}function f(p,q){c.removeClass("ui-state-hover")}function d(p,q){g.addClass("ui-state-hover")
}function j(p,q){g.removeClass("ui-state-hover")}function a(){o=GSEmailSettingsUpdate();
i=jQuery("#add-email-address-dialog");m=jQuery("#form\\.resendVerificationAddress");
k=jQuery("#form\\.actions\\.change");c=jQuery("#delivery-addresses");g=jQuery("#other-addresses")
}a();return{init:function(){var p=null;c.sortable({connectWith:"#other-addresses",update:b,cancel:".ui-state-disabled",start:d,stop:j}).disableSelection();
g.sortable({connectWith:"#delivery-addresses",update:b,start:e,stop:f}).disableSelection();
p={autoOpen:false,minHeight:190,modal:true,dialogClass:"gs-content-js-jqueryui"};
i.dialog(p);jQuery("#open-add").button({icons:{primary:"ui-icon-plusthick"}}).removeAttr("href").click(l);
jQuery("#form\\.actions\\.add").button({icons:{primary:"ui-icon-plusthick"}});jQuery(".removeLink").button({icons:{primary:"ui-icon-minusthick"}}).removeAttr("href").click(h);
jQuery(".resendLink").button({icons:{primary:"ui-icon-mail-closed"}}).removeAttr("href").click(n)
}}}function GSCheckVerified(){var c=null,b="checkemailverified.ajax",a=2000,d=GSEmailSettingsUpdate();
return{init:function(){},poll:function(){jQuery("#unverified-addresses").children().children(".email").each(function(){var f=null,g=null;
f=jQuery(this).text();g={type:"POST",url:b,cache:false,data:"email="+encodeURIComponent(f),success:GSCheckVerified.checkReturn};
jQuery.ajax(g)})},checkReturn:function(g,i){var e=g=="1",h=null,f=null;if(e){f='<li><samp class="email">'+c+"</samp></li>";
h=jQuery("#other-addresses");h.append(f);d.updateOther();jQuery("#form\\.actions\\.change").click()
}else{setTimeout(function(){GSCheckVerified.poll()},a)}}}}function gs_profile_email_profile_settings_init(){var b=null,a=null;
b=GSEmailSettings();b.init();a=GSCheckVerified();a.poll()}jQuery(window).load(function(){gsJsLoader.with_module("/++resource++jquery-ui-1.10.3.js",gs_profile_email_profile_settings_init)
});