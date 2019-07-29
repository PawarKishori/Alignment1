$('#ser').on('keyup', function(){
    var value = $(this).val();
    $('#dvCSV table tr').each(function(index){
        if(index != 0){
            var $row = $(this);
            var id = $row.find("td:first").text();
            if(id.indexOf(value) != 0){
                $(this).hide();
            }
            else{
                $(this).show();
            }
        }
    });
});

$(document).ready(function() {
  var columns = ['para', 'layer']
  $('#dvCSV table tr').each(function() {
    var cells = $('td', this);
    var titleArr = cells.map(function(index) {
	if(index == 0 || index == 1)
	{
    		return columns[index] + ':' + this.innerHTML;
	}
    });
    cells.each(function(index) {
    	var finalTooltip = titleArr.filter(function(i){
      	return index !== i;
      });
      $(this).attr('title', finalTooltip.toArray().join(','))
    })
    var name = cells[0];
    var regNumber = cells[1];
    var idCode = cells[2];

  });
  var oTable = $('#dvCSV').dataTable();
  $(oTable.fnGetNodes()).tooltip({
    "delay": 0,
    "track": true,
    "fade": 250
  });
});


/*$(document).ready(function() {
	var input = document.getElementById('ser').value;
	$('#.table tr').each(function() {
		var cells = $('td', this);
        var i=0;
        for (i=0; i<cells.length; i++)
        {
            if(cells[i].textContent.toLowerCase().includes(input.toLowerCase()))
		    {
			     flag=0;
		    }
        }
        if(flag == 0)
            {
                table.style.display = 'table-cell';
            }
	
	});
});
}*/

var $rows = $('.table tr');
$('#ser').keyup(function() {
var val = '^(?=.*\\b' + $.trim($(this).val()).split(/\s+/)
	reg = RegExp(val, 'i'),
	text;

$rows.show().filter(function() {
	text = $(this).text().replace(/\s+/g, '');
	return !reg.test(test);
}).hide();
});

/* $('#dvCSV table tr').addClass('visible');
  $('#ser').keyup(function(event) {
    //if esc is pressed or nothing is entered
    if (event.keyCode == 27 || $(this).val() == '') {
      //if esc is pressed we want to clear the value of search box
      $(this).val('');
             
      //we want each row to be visible because if nothing
      //is entered then all rows are matched.
      $('#dvCSV table tr').removeClass('visible').show().addClass('visible');
    }
 
    //if there is text, lets filter
    else {
      filter('dvCSV table tr', $(this).val());
    }
});*/

