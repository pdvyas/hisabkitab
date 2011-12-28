
tab_order = ['id','date','method','card','narration','amount']
tab_names = {
	'id' : 'id',
	'date' : 'Date',
	'method' : 'Method',
	'narration' : 'Narration',
	'card' : 'Card',
	'amount' : 'Amount'
}

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
		iret = {}
		for(i in tab_names) {
			iret[i] = txn[i]
		}
		if (txn.party) {
			iret['narration'] = txn['party']	
		}
		ret.push(iret)
	});
	return ret;
}

mk_table = function(data) {
	var cols = tab_order;
	data = sanit_data(data);
	var arr = make_arr(data);
	var table = $(document.createElement('table'));
	var thead = $(document.createElement('thead'));
	var tbody = $(document.createElement('tbody'));
	var tr = $(document.createElement('tr'));
	$.each(cols,function(i,col) {
		var th = $(document.createElement('th'));
		th.append(tab_names[col]);
		tr.append(th);
	});
	thead.append(tr);

	$.each(arr,function(i,iarr) {
		var tr = $(document.createElement('tr'));
		for (j in iarr) {
			var td = $(document.createElement('td'));
			td.append(iarr[j]);
			tr.append(td);
		}
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
