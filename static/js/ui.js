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
		$('#main').empty().
			append(make_tabs(['Bank','Fixed Deposits','Mutual Funds','Stocks']));
		load_tab_events();
		$.hisab.bank.init();
	}
}

var put_logout = function() {
	$('#logout').empty().append('Logout').
		on('click',function() {
			$.user.logout();	
	});
}

// Takes an array of tab names and returns a div that implements bootstrap tabs
// Usage : make_tabs(['One','Two','Three']);
// makes 3 tabs One, Two and Three and their content divs are accessible with selectors,
// #one,#two,#three
// The first tab is active by default

var make_tabs = function(tabs) {
	apptabs = $(document.createElement('div'));
	tab_list = $(document.createElement('ul'));
	tab_list.addClass('tabs');
	tab_list.attr('data-tabs','tabs');
	tab_contents = $(document.createElement('div'));
	tab_contents.addClass("tab-content");
	$.each(tabs,function(i,tab) {

		//tablist part

		var tabid = munch_name(tab)
		var ele = $(document.createElement('li'));
		var link = $(document.createElement('a'));
		link.attr('href', '#' + tabid);
		link.append(tab);
		ele.append(link);
		if(i==0) {
			ele.addClass('active');
		}
		tab_list.append(ele);

		//tab content part
		
		var content = $(document.createElement('div'));
		content.attr('id', tabid);
		content.addClass("tab-pane");
		if(i==0) {
			content.addClass('active');
		}
		tab_contents.append(content);

	});
	apptabs.addClass('container');
	apptabs.append(tab_list);
	apptabs.append(tab_contents);
	apptabs.css('padding-top','10px');
	return apptabs;
}

var munch_name = function(name) {
	name = name.toLowerCase().
		replace(' ','_');
	return name;
}

var load_tab_events = function() {
		$('#bank').bind('loaded',function() {
			var a = $.hisab.bank.transactions().get()
			var tab = mk_table(a,tab)
			$('#bank').append(tab)
			var oTable = $('table').dataTable({
				'aoColumnDefs' :[ { "bSearchable": false, "bVisible": false, "aTargets": [ 0 ] }],
				"sDom": "<'row'<'span8'l><'span8'f>r>t<'row'<'span8'i><'span8'p>>",
				"sPaginationType": "bootstrap",
				"aaSorting" : [[1,'asc']]
				});

			$('.category').editable( '/cat', {
				"callback": function( sValue, y ) {
					var aPos = oTable.fnGetPosition( this );
					oTable.fnUpdate( sValue, aPos[0], aPos[1] );
				},
				"submitdata": function ( value, settings ) {
					return {
						"row_id": this.parentNode.getAttribute('id'),
						"column": oTable.fnGetPosition( this )[2]
					};
				},
				"height": "14px"
			} );
		});

		$(".category").delegate(".ui-autocomplete-input", "focus", function (event) {
			$(this).autocomplete({
				source: '/cat',
				minLength: 1
			});
});

}
