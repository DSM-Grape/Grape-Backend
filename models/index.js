const Sequelize = require('sequelize');

const sequelize = new Sequelize(
  'grape',
  'root',
  process.env.GRAPE_MYSQL_PW,
  {
    host: 'localhost',
    dialect: 'mysql',
  },
);

const accounts = sequelize.define('tbl_accounts', {
  uuid: {
    type: Sequelize.CHAR(32),
    primaryKey: true,
  },
  id: {
    type: Sequelize.STRING(127),
    unique: true,
  },
  password: {
    type: Sequelize.STRING(200),
    allowNull: true,
    defaultValue: null,
  },
  plan: {
    type: Sequelize.ENUM('FREE', 'BUSINESS', 'FIRST'),
    defaultValue: 'FREE',
  },
  email: {
    type: Sequelize.STRING(63),
    allowNull: true,
    defaultValue: null,
  },
  nickname: {
    type: Sequelize.STRING(63),
    allowNull: true,
    defaultValue: null,
  },
}, {
  timestamps: false,
});

const projects = sequelize.define('tbl_projects', {
  id: {
    type: Sequelize.INTEGER(11),
    primaryKey: true,
    autoIncrement: true,
  },
  owner_uuid: {
    type: Sequelize.CHAR(32),
    references: {
      model: accounts,
      key: 'uuid',
    },
  },
  name: {
    type: Sequelize.STRING(127),
  },
  apidoc_json: {
    type: Sequelize.TEXT,
    defaultValue: null,
  },
}, {
  timestamps: false,
});

sequelize.sync();

module.exports = sequelize;
