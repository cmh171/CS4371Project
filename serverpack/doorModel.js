const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const doorSchema = new Schema({
    // Define your schema here. For example:
    // id: { type: Number},
    name: { type: String },
    status: { type: String }
});

const Door = mongoose.model('Door', doorSchema, 'doors');

module.exports = Door;