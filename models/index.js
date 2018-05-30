'use strict';

const Sequelize = require('sequelize');
const sequelize = new Sequelize(
    'grape',
    'root',
    process.env.GRAPE_MYSQL_PW,
    {
        host: 'localhost',
        dialect: 'mysql'
    }
);

module.exports = sequelize;
