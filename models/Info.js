const mongoose = require('mongoose')

const fileSchema = new mongoose.Schema({
    filename : String,
    name : String
});

const infoModel = mongoose.model('File',fileSchema);

module.exports = infoModel