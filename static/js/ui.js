jQuery.fn.center = function () {
	this.css("position","absolute");
	this.css("top", (($(window).height() - this.outerHeight()) / 2) + $(window).scrollTop() + "px");
	this.css("left", (($(window).width() - this.outerWidth()) / 2) + $(window).scrollLeft() + "px");
	return this;

}

$.ui = {
	make_login_page: function() {
		$('#main').html(' \
			  <div id="login" class="span4 centered">\
			  <input name="name" id="username" class="span4" placeholder="username"/><br/><br/>\
			  <input id="password" name="password" type="password" class="span4" placeholder="password"/><br/><br/>\
				<button id="loginbtn" class="btn primary span4">Login</button>\
			  </div>\
			  ');
		$('#login').center();
		$('#loginbtn').on('click',function() {
			var uname = $('#username').val();
			var pass = $('#password').val();
			$.user.login(uname,pass);
		});


	},

	make_main_page: function() {
		put_logout();
		$('#main').empty();
	}
}

var put_logout = function() {
	$('#logout').empty().append('Logout').
		on('click',function() {
			$.user.logout();	
	});
}
