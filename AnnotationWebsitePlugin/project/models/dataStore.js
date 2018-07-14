const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const annotationSchema = new Schema({
   username: {
       type: Number,
       required: true
   },

    annotation: {
       type: Array,
       required: true
    } 
});

const dataStore = mongoose.model('datastore', annotationSchema);

module.exports = dataStore;