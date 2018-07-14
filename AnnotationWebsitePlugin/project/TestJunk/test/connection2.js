const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost/loginData');

mongoose.connection.once('open', function() {
	console.log('Connection created');}).on('error', function(error) {
	console.log('Connection error:', error);
});