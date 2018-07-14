var express = require('express');
var path = require('path');
var bodyParser = require('body-parser');
const mongoose = require('mongoose');

var app = express();

var mongodb = require('mongodb');
var dbConn = mongodb.MongoClient.connect('mongodb://localhost:27017');
const dataStore = require('./models/dataStore');

mongoose.connect('mongodb://localhost/annoData');
mongoose.Promise = global.Promise;

app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static(path.resolve(__dirname, 'public')));

app.post('/post-feedback', function (req, res) {
    dataStore.create(req.body).then(function(datastore) {
        res.send(datastore);
    });
    res.send('Data received:\n' + JSON.stringify(req.body));
});


app.get('/view-feedbacks',  function(req, res) {
    dbConn.then(function(db) {
        db.collection('feedbacks').find({}).toArray().then(function(feedbacks) {
            res.status(200).json(feedbacks);
        });
    });
});

app.listen(process.env.PORT || 4000, process.env.IP || '0.0.0.0' );