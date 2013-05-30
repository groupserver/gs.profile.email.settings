jQuery.noConflict();function GSEmailSettingsUpdate(){return{updateDelivery:function(){var a="";
jQuery("#delivery-addresses").children().children(".email").each(function(){a+=jQuery(this).text()+"\n"
});jQuery("#form\\.deliveryAddresses").text(a)},updateOther:function(){var a="";jQuery("#other-addresses").children().children(".email").each(function(){a+=jQuery(this).text()+"\n"
});jQuery("#form\\.otherAddresses").text(a)},updateUnverified:function(){var a="";
jQuery("#unverified-addresses").children().children(".email").each(function(){a+=jQuery(this).text()+"\n"
});jQuery("#form\\.unverifiedAddresses").text(a)}}}function GSEmailSettings(){var h=GSEmailSettingsUpdate();
function a(){h.updateDelivery();h.updateOther();h.updateUnverified();jQuery("#form\\.resendVerificationAddress").val("");
jQuery("#form\\.actions\\.change").click()}function g(){jQuery("#add-email-address-dialog").dialog("open")
}function i(){var j=null;h.updateDelivery();h.updateOther();h.updateUnverified();
j=jQuery(this).parents("li").find(".email").text();jQuery("#form\\.resendVerificationAddress").val(j);
jQuery("#form\\.actions\\.change").click()}function e(){jQuery(this).parents("li").remove();
a()}function c(j,k){jQuery("#delivery-addresses").addClass("ui-state-hover")}function d(j,k){jQuery("#delivery-addresses").removeClass("ui-state-hover")
}function b(j,k){jQuery("#other-addresses").addClass("ui-state-hover")}function f(j,k){jQuery("#other-addresses").removeClass("ui-state-hover")
}return{init:function(){var j=null;jQuery("#delivery-addresses").sortable({connectWith:"#other-addresses",update:a,cancel:".ui-state-disabled",start:b,stop:f}).disableSelection();
jQuery("#other-addresses").sortable({connectWith:"#delivery-addresses",update:a,start:c,stop:d}).disableSelection();
j={autoOpen:false,minWidth:516,modal:true};jQuery("#add-email-address-dialog").dialog(j);
jQuery("#open-add").button({icons:{primary:"ui-icon-plusthick"}}).removeAttr("href").click(g);
jQuery("#form\\.actions\\.add").button({icons:{primary:"ui-icon-plusthick"}});jQuery(".removeLink").button({icons:{primary:"ui-icon-minusthick"}}).removeAttr("href").click(e);
jQuery(".resendLink").button({icons:{primary:"ui-icon-mail-closed"}}).removeAttr("href").click(i)
}}}function GSCheckVerified(){var c=null,b="checkemailverified.ajax",a=2000,d=GSEmailSettingsUpdate();
return{init:function(){},poll:function(){jQuery("#unverified-addresses").children().children(".email").each(function(){var f=null,g=null;
f=jQuery(this).text();g={type:"POST",url:b,cache:false,data:"email="+encodeURIComponent(f),success:GSCheckVerified.checkReturn};
jQuery.ajax(g)})},checkReturn:function(g,i){var e=g=="1",h=null,f=null;if(e){f='<li><samp class="email">'+c+"</samp></li>";
h=jQuery("#other-addresses");h.append(f);d.updateOther();jQuery("#form\\.actions\\.change").click()
}else{setTimeout("GSCheckVerified.poll()",a)}}}}jQuery(window).load(function(){var b=null,a=null;
b=GSEmailSettings();b.init();a=GSCheckVerified();a.poll()});