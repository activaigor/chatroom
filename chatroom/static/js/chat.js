var ws;

$(document).ready(function(){

	function create_ws() {
		ws = new WebSocket("ws://127.0.0.1:5000/chat");

		ws.onopen = function(e) {
			send_message('hello', 'hello');
		};

		ws.onmessage = function(e) {
			var data = JSON.parse(e.data);
			msg = prepare_message(data);
			if (msg) {
				$('#chat_window').append(msg);
				if (data['from'] == 'system') {
					update_list();
				}
			}
		};
	}

	function update_list() {
		$.post("/ajax", { 
			users_online: 1 
		}, function(data) {
			data = eval('(' + data + ')');
			if (data['success']) {
				$('#users_online').find('ul').html('');
				$.map(data['data'], function (user) {
					$('#users_online').find('ul').append('<li><span>' + user + '</span></li>');
				});
			}
		});
	}

	function prepare_message(data) {
		if (data['room'] == chat_room) {
			return '<p><i>' + data['from'] + '</i>: ' + data['body'] + '</p>';
		} else {
			return null;
		}
	}
	
	function send_message(data, type) {
		msg = {};
		msg['room'] = chat_room;
		msg['from'] = chat_user;
		msg['to'] = 'all';
		msg['body'] = data;
		msg['type'] = type
		ws.send(JSON.stringify(msg));
	}
	
	// Check if we support WS-technology
	if("WebSocket" in window) {
		create_ws();
	}

	$('#message_input').keypress(function(e){
        if(e.which == 13){
            $('#message_send').click();
        }
    });
	
	$('#message_send').click(function(){
		data = $('#message_input').val();
		$('#message_input').val('');
		send_message(data, 'user');
		$('#chat_window').scrollTo('max', {axis: 'y'});
	});


})