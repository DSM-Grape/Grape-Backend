/* eslint import/no-unresolved: off */
/* eslint import/no-absolute-path: off */
const fs = require('fs');
const path = require('path');
const Sequelize = require('sequelize');

const basename = path.basename(__filename);
const env = process.env.NODE_ENV || 'development'; // 'development', 'test', 'production' 3 cases
const config = require('/app/config/grape/config')[env];

const db = {};

const sequelize = new Sequelize(config.database, config.username, config.password, config);

fs.readdirSync(__dirname)
  .filter(filename => (filename.indexOf('.') !== 0) && (filename !== basename) && (filename.slice(-3) === '.js'))
  .forEach((filename) => {
    const model = sequelize.import(path.join(__dirname, filename));
    db[model.name] = model;
  });

Object.keys(db)
  .forEach((modelName) => {
    if (db[modelName].associate) {
      db[modelName].associate(db);
    }
  });

db.sequelize = sequelize;
db.Sequelize = Sequelize;

module.exports = db;
