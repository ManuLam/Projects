const express = require('express');
const router = express.Router();
const dataStore = require('../models/dataStore');

router.get('tester', function(req, res){
	res.send({type: 'GET'});
});

router.post('tester', function(req, res){
	dataStore.create(req.body).then(function(datastore) {
		res.send(datastore);
	});
});


router.put('tester/:id', function(req, res){
	res.send({type: 'PUT'});
});

router.delete('tester/:id', function(req, res){
	res.send({type: 'DELETE'});
});

module.exports = router;