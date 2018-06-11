const mongoose = require('mongoose');
const debug = require('debug')('server:');

module.exports = new Promise((resolve) => {
  mongoose.Promise = global.Promise;
  mongoose.connect('mongodb://localhost:27017/grape');
  mongoose.connection.on('error', console.error.bind(console, 'mongoose connection error.'));
  mongoose.connection.on('open', () => {
    debug('CONNECTED TO DATABASE');
    resolve();
  });
  mongoose.connection.on('disconnected', () => {
    debug('DISCONNECTED FROM DATABASE');
    process.exit(1);
  });
});
