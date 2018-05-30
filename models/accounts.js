module.exports = (sequelize, DataTypes) => {
  const accounts = sequelize.define('tbl_accounts', {
    uuid: {
      type: DataTypes.CHAR(32),
      primaryKey: true,
    },
    id: {
      type: DataTypes.STRING(127),
      unique: true,
    },
    password: {
      type: DataTypes.STRING(200),
      allowNull: true,
      defaultValue: null,
    },
    plan: {
      type: DataTypes.ENUM('FREE', 'BUSINESS', 'FIRST'),
      defaultValue: 'FREE',
    },
    email: {
      type: DataTypes.STRING(63),
      allowNull: true,
      defaultValue: null,
    },
    nickname: {
      type: DataTypes.STRING(63),
      allowNull: true,
      defaultValue: null,
    },
  }, {
    timestamps: false,
  });

  accounts.associate = (models) => {
    models.tbl_accounts.hasMany(models.tbl_projects, {foreignKey: 'projects', sourceKey: 'uuid'});
  };

  return accounts;
};
