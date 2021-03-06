$(document).bind('got_accounts',function(e,acids) {
	acids = JSON.parse(acids)
	if($.type(acids)==="string") {
		acids = Array(acids);
	}
	$.hisab.bank.acids = acids;
	$.hisab.bank.got_txns = $.hisab.bank.got_txns || [];
	$.each(acids,function(i,acid) {
		if(!(acid in $.hisab.bank.got_txns)) {
			get_transactions(acid);
		}
	});
});

$(document).bind('got_txns',function(e,acid) {
	$.hisab.bank.got_txns.push(acid);
	if($.hisab.bank.got_txns.length == $.hisab.bank.acids.length) {
		$.hisab.bank.loaded = true;
		$('#bank').trigger('loaded');
	}
});

$.hisab = $.hisab || {};
$.hisab.bank = {
	init : function() {
		get_accounts();
	},

	loaded : false
}

var get_accounts = function() {

	$.ajax({
		'type' : 'GET',
		'url' : '/account',
		'success' : function(data,textStatus,jqXHR) {
			var d = JSON.parse(data);
			$.hisab.bank.accounts = TAFFY(d);
			var acids = $.hisab.bank.accounts().select('id');
			$(document).trigger('got_accounts',JSON.stringify(acids));
		}
	});
}

var get_transactions = function(acid) {
	if(!(acid in $.hisab.bank.got_txns)) {
		$.ajax({
			'type' : 'GET',
			'url' : '/account/'+acid+'/transaction',
			'success' : function(data,textStatus,jqXHR) {
				var d = JSON.parse(data);
				if($.hisab.bank.transactions) {
					$.hisab.bank.transactions.insert(d);
				}
				else {
					$.hisab.bank.transactions = TAFFY(d);
				}
				$(document).trigger('got_txns',acid);
			}
		});	
	}
}
