const mongoose = require('mongoose');

const Schema = mongoose.Schema;

/**
 * Defines what fields are stored in a Door document in MongoDB.
 */
const doorSchema = new Schema({
    name: { type: String },
    status: { type: String }, 
    cipher: { type: String}
});

const Door = mongoose.model('Door', doorSchema, 'doors');

module.exports = Door;