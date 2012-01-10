txn_tab = [
	{
		'name':'id',
		'idx' : 'id',
	},
	{
		'name':'Date',
		'idx':'date'	
	},
	{
		'name':'Method',
		'idx' : 'method'
	},
	{
		'name' : 'Card',
		'idx' : 'card'
	},
	{
		'name' : 'Narration',
		'idx' : 'narration'
	},
	{
		'name' : 'Amount',
		'idx' : 'amount'
	},
	{
		'name' : 'Type',
		'idx' : 't_type'
	},
	{
		'name' : 'Category',
		'idx' : 'category',
		'options' : {
			'class' : 'category'
		}
	}
];

make_table = function(data) {
	var div = $(document.createElement('div'))
	var table = $(document.createElement('table'));
	div.append(table)
	table.addClass('display');
	data = sanit_data(data)
	var keys = tab_order;
	var arr = make_arr(data);
	var dt_dict = {};
	dt_dict.aaData = arr;
	var aoColumns = Array();
	$.each(keys,function(i,col) {
		aoColumns.push({'sTitle':col});
	});
	dt_dict.aoColumns = aoColumns;
	table.dataTable(dt_dict);
	return table;
}


sanit_data = function(data) {
	var ret = []
	$.each(data,function(i,txn) {
		iret = $.extend({},txn)

		if (txn.party) {
			iret['narration'] = txn['party']	
		}
		ret.push(iret)
	});
	return ret;
}

var get_tab_cols = function(tab) {
	var ret = [];
	$.each(tab,function(i,col) {
		ret.push(col.name);
	});
	return ret;
}

mk_table = function(data,tab) {
	tab = txn_tab
	var cols = get_tab_cols(tab);
	data = sanit_data(data)
	var table = $(document.createElement('table'));
	var thead = $(document.createElement('thead'));
	var tbody = $(document.createElement('tbody'));
	var tr = $(document.createElement('tr'));
	$.each(cols,function(i,col) {
		var th = $(document.createElement('th'));
		th.append(col);
		tr.append(th);
	});
	thead.append(tr);

	$.each(data,function(i,txn) {
		var tr = $(document.createElement('tr'));
		$.each(tab,function(j,col) {
			var td = $(document.createElement('td'));
			td.append(txn[col.idx]);
			if(col.options) {
				td.addClass(col.options.class)
			}
			tr.append(td);
		});

		tbody.append(tr);
	});
	table.append(thead).append(tbody);
	return table;
}

get_keys = function(data) {
	data = data[0];
	var arr = Array();
	for(i in data) {
		arr.push(i);
	}
	return arr;
}

make_arr = function(data) {
	var ret = Array();
	$.each(data,function(index,i) {
		iret = Array();
		for(j in tab_order) {
			iret.push(i[tab_order[j]]);
		}
		ret.push(iret);
	});
	return ret;
}

test = function() {
	$.hisab.bank.init();
	a = $.hisab.bank.transactions().get()
	b = mk_table(a)
	$('#bank').append(b)
}
