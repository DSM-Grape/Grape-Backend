const mongoose = require('mongoose');

module.exports = new Promise((resolve) => {
  mongoose.Promise = global.Promise;
  mongoose.connect('mongodb://localhost:27017/grape');
  mongoose.connection.on('error', console.error.bind(console, 'mongoose connection error.'));
  mongoose.connection.on('open', () => {
    console.log('CONNECTED TO DATABASE');
    resolve();
  });
  mongoose.connection.on('disconnected', () => {
    console.log('DISCONNECTED FROM DATABASE');
    process.exit(1);
  });
});
