
$(document).bind('login',function (e,username) {

	$.user.name = username;
	$.user.logged_in = true;
	$.ui.make_main_page();
});

$(document).bind('logout',function(e) {
	
	$.user.name = undefined;
	$.user.logged_in = false;
	$.ui.make_login_page();
	$('#logout').empty();
});

$.user = {
	name : undefined,

	logged_in: false,

	login : function(username,password) {
		var data = {
			'name':username,
			'password':password
		}

		$.ajax({
			'type':'POST',
			'url':'/login',
			'data':data,
			'success':function(data,textStatus,jqXHR) {
				var d = JSON.parse(data)
				$(document).trigger('login',d.name);
			}
		});
	},

	check_login : function() {
		$.ajax({
			'type':'GET',
			'url':'/user',
			'success':function(data,textStatus,jqXHR) {
				var d = JSON.parse(data);
				if(d.name==='') {
					$.ui.make_login_page();
				}
				else {
					$(document).trigger('login',d.name)
				}
			}
		});
	},

	logout : function() {
		$.ajax({
			'type' : 'GET',
			'url' : '/logout',
			'success' : function(data,textStatus,jqXHR) {
				$(document).trigger('logout');
			}
		});
	}
}
