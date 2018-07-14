const assert = require('assert');
const dataStore = require('./models/loginStore');
//desrbies tests
describe('Saving records', function() {
	//create tests
	it('Save a record to the database', function(done) {
		var char1 = new loginStore({
			username: "8505353",
			password: "asdada"
		});

		var char2 = new loginStore({
			username: "42059198",
			password: "cat"
		});

		var char3 = new loginStore({
			username: "22839870",
			password: "sed"
		});

		var char4 = new loginStore({
			username: "18334826",
			password: "dsa"
		});

		char1.save().then(function() {
			assert(char.isNew === false);
			done();
		});

		char2.save().then(function() {
			assert(char.isNew === false);
			done();
		});

		char3.save().then(function() {
			assert(char.isNew === false);
			done();
		});
		
		char4.save().then(function() {
			assert(char.isNew === false);
			done();
		});

	});

});