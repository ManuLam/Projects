const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const userSchema = new Schema({
   username: {
       type: String
   },

    password: {
       type: String
    } 
});

const loginStore = mongoose.model('loginstore', userSchema);

module.exports = loginStore;