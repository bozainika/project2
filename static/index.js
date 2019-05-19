document.addEventListener('DOMContentLoaded', ()=>{
	
	var domain=location.protocol+'//'+document.domain+':'+location.port;
	var socket = io.connect(location.protocol+'//'+document.domain+':'+location.port);

	socket.on('connect', () => {

		document.querySelector('#form').onsubmit=() => {
			const name = document.querySelector('#name').value;
		//	const message=document.querySelector('#message_text').value;
			socket.emit('create room',{'name':name});
			return false;
		
		};
	
	});
	
	socket.on('show rooms', data => {
		name=data['title']
		let link=`${name}`
		let a=document.createElement('a');
		a.appendChild(document.createTextNode(name));
		a.href=link;
		a.class='room_name';
		a.value=name;
		let li=document.createElement('li');
		li.class='list-group item';
		li.appendChild(a);
		document.querySelector('#list').appendChild(li);
		document.querySelector('#p').innerHTML='';
		document.querySelector('#p').style.display="none";

	});
	socket.on('failure', data =>{
		const status=data;
		
		document.querySelector('#p').innerHTML=`${status} `;
		document.querySelector('#p').style.display="block";
		//document.querySelector('#container').appendChild(p);

	});
	socket_join_room=io(domain+'/join_room')
	document.querySelectorAll(".room_name").onclick=function(){
			room = this.value;
			socket_join_room.emit('join',{'room':room});
		};

});

