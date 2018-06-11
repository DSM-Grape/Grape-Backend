const mongoose = require('mongoose');
const { Schema } = require('mongoose');

const accounts = Schema({
  id: { type: String, unique: true, required: true },
  password: { type: String, required: false, default: null },
  plan: {
    type: String, enum: ['FREE', 'BUSINESS', 'FIRST'], required: true, default: 'FREE',
  },
  email: { type: String, required: false, default: null },
  nickname: { type: String, required: false, default: null },
}, {
  collection: 'accounts',
});

module.exports = mongoose.model('accounts', accounts);
