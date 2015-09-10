var util = {

    setCookie: function (c_name, value) {
		document.cookie = c_name+"="+value+";path=/";
	},

	getCookie: function (n) {
		var Q=n+"=";var v=document.cookie.split(';');for(var i=0;i<v.length;i++){var c=v[i];while(c.charAt(0)==' ')c=c.substring(1,c.length);if(c.indexOf(Q)==0)return c.substring(Q.length,c.length)}return null;
	},

    ajaxSetup: function (){
        $.ajaxSetup({
            xhrFields: { withCredentials: true },
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", util.getCookie('csrftoken'));
            }
        });
    },

    messageTimeoutID: 0,

    showMessage: function (message, is_error){

        clearTimeout(util.messageTimeoutID);

        var m_sel = $(".message");

        m_sel.removeClass("error");

        m_sel.find(".text").html(message);
        m_sel.fadeIn(150);

        if (is_error){
            m_sel.addClass("error");
        }

        util.messageTimeoutID = setTimeout('util.hideMessage()', 8000);
    },

    hideMessage: function (){

        var m_sel = $(".message");
        m_sel.fadeOut(150);

        clearTimeout(util.messageTimeoutID);
    },

    setBusy: function (sl){
        $(sl).addClass('busy')
    },

    setUnBusy: function (sl){
        $(sl).removeClass('busy');
    },

    api: function (method, url, data, success_callback, error_callback){
        var params = {
            url: API_URL + url,
            type: method,
            data: data,
            dataType: 'json'
        };

        if (success_callback){
            params.success = success_callback;
        }

        if (error_callback){
            params.error = error_callback;
        }

        $.ajax(params);
    },

    update: function (sender){
        util.setBusy(sender);
        $(sender).html("Updating..");

        util.api("GET", "/update", {}, function (){
            util.setUnBusy(sender);
            $(sender).html("Update");
        }, function (data){
            util.showMessage("Update failed<br/>Error:" + data.responseText)
            util.setUnBusy(sender);
        });

    }
};


var API_URL = "/api/v1";


var person = {

    add: function (){
        var name = $(".name-input > input").val();

        util.setBusy(".button.add");

        util.api('POST', '/person', {"name": name}, function (result){
            location.href = "/person/%s/edit".replace('%s', result.id);
        }, function (result) {
            util.showMessage(result, true);
            util.setUnBusy(".button.add");
        });

    },

    changeName: function (){
        var name = $(".name-input > input").val();

        util.setBusy(".button.change");

        util.api('PUT', "/person/" + person_id, {"name": name}, function() {
            util.showMessage("Successfully changed name");
            util.setUnBusy(".button.change");
        }, function (result){
            util.showMessage(result, true);
            util.setUnBusy(".button.add");
        });

    },

    setImage: function (account_pk, sender){

        util.setBusy(sender);

        var url = "/person/" + person_id + "/account/" + account_pk + "/set-image";

        util.api('POST', url, {}, function() {
            util.showMessage("Successfully set person's main photo");
            util.setUnBusy(sender);
        }, function (result){
            util.showMessage(result, true);
            util.setUnBusy(sender);
        });
    },

    removeAccount: function (account_pk, sender){
        var item_sel = $(sender).parent().parent();
        item_sel.animate({"opacity": 0.3}, 250);

        var url = "/person/" + person_id + "/account/" + account_pk;

        util.api("DELETE", url, {}, function() {
            item_sel.remove();
            util.showMessage("Successfully removed account");
        });
    },

    addAccount: function (){

        util.setBusy(".button.add");

        var link = $(".link-input > input").val();
        var url = "/person/" + person_id + "/account";

        util.api("POST", url, {"link": link}, function() {
            location.reload();
        }, function (response){
            util.showMessage("Unable to add new account<br/>Error:" + response.responseText, true);
            util.setUnBusy(".button.add");
        });

    }

};


$(document).ready(function (){
    util.ajaxSetup();

    $(".message > .close-btn").click(function (){
        util.hideMessage();
    });
});