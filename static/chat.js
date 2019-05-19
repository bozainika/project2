document.addEventListener('DOMContentLoaded', ()=>{
	
	var socket = io.connect(location.protocol+'//'+document.domain+':'+location.port);
	var room_socket=io(location.protocol+'//'+document.domain+':'+location.port+'/room')

	
	room_socket.on('connect', () => {
		document.querySelector('#submitForm').onclick = ()=> {
			const name = document.querySelector('#name').value;
			const room = document.querySelector('#room').value;
			const message=document.querySelector('#message_text').value;
			const data={
				"name" : name,
				"room" : room,
				"message" : message
			};
			room_socket.emit('send', data);
			return false;
		
		};
	});
	
	room_socket.on('show messages', data => {
		//data.messages.forEach(mess => {
			ul=document.querySelector('#list');
			li=document.createElement('li');
			li.innerHTML = data['name']+' said: '+data['message'];
			ul.appendChild(li);
	});

});