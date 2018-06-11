const mongoose = require('mongoose');
const { Schema } = require('mongoose');

const projects = Schema({
  name: { type: String, required: true },
  apidoc: { type: String, default: null },
  owner: { type: Schema.Types.ObjectId, ref: 'accounts' },
  members: [{ type: Schema.Types.ObjectId, ref: 'accounts' }],
}, {
  collection: 'projects',
});

module.exports = mongoose.model('projects', projects);
