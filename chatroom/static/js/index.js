$(document).ready(function(){
	$(function(){
		$("input[name$='room']").Watermark('Поиск комнаты...');
		$("input[name$='room_add']").Watermark('Название комнаты');
	});
	$('#room_add').find('a').click(function(){
		if ($('#room_add').find('input').val() == 'Название комнаты') {
			$('#room_add').css('width','307px');
			$('#room_add').find('input').show();
		} else {
			name = $('#room_add').find('input').val();
			$.post("/ajax", { 
				name: name,
				room_add: 1 
			}, function(data) {
				data = eval('(' + data + ')');
				if (data['success']) {
					alert('Комната успешно добавлена');
					$("#parrent_list").append('<div class="room"><a href="/chat/' + name + '">' + name + '</a></div>');
					$('#room_add').css('width','60px');
					$('#room_add').find('input').hide();
					$('#room_add').find('input').val('Название комнаты');
				}
			});
		}
	});
	//$('#room_search').find('input').autocomplete({ source : '/jsonp' }); 
	$('#room_search').find('input').autocomplete({
		source: function (request, response) {
    	    $.ajax({
    	        url: "/jsonp",
    	        dataType: "json",
    	        data: {
    	            term: request.term
    	        },
    	        success: function (data) {
    	        	$("#parrent_list").hide();
    	        	$("#search_list").html('');
    	        	$("#search_list").show();
    	            response($.map(data, function (item) {
    	                $("#search_list").append('<div class="room"><a href="/chat/' + item + '">' + item + '</a></div>');
    	            }))
    	        }
    	    })
    	}
	});

	$("#room_search").find('input').keyup (function (e) {
	    val = $(this).val();
	    if (!val) {
	    	$("#parrent_list").show();
    	    $("#search_list").html('');
    	    $("#search_list").hide();
	    }
	});
	
})