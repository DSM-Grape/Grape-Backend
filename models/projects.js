module.exports = (sequelize, DataTypes) => {
  const Projects = sequelize.define('tbl_projects', {
    id: {
      type: DataTypes.INTEGER(11),
      primaryKey: true,
      autoIncrement: true,
    },
    // owner_uuid: {
    //   type: DataTypes.CHAR(32),
    //   references: {
    //     model: accounts,
    //     key: 'uuid',
    //   },
    // },
    name: {
      type: DataTypes.STRING(127),
    },
    apidoc_json: {
      type: DataTypes.TEXT,
      defaultValue: null,
    },
  }, {
    timestamps: false,
  });

  Projects.associate = (models) => {
    models.tbl_projects.belongsTo(models.tbl_accounts, {foreignKey: 'owner_uuid'});
  };

  return Projects;
};
