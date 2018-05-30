module.exports = (sequelize, DataTypes) => {
  const projectMembers = sequelize.define('tbl_project_members', {
    id: {
      type: Sequelize.INTEGER(11),
      primaryKey: true,
      autoIncrement: true,
    },
    // project_id: {
    //   type: Sequelize.INTEGER(11),
    //   references: {
    //     model: projects,
    //     key: 'id',
    //   },
    // },
    // member_uuid: {
    //   type: Sequelize.CHAR(32),
    //   references: {
    //     model: accounts,
    //     key: 'uuid',
    //   },
    // },
    role: {
      type: Sequelize.ENUM('MEMBER', 'MAINTAINER', 'OWNER'),
    },
  }, {
    timestamps: false,
  });

  projectMembers.associate = (models) => {
    // models.tbl_project_members.hasMany(models.tbl_accounts, {foreignKey: 'members', sourceKey: 'member_uuid'});
    // models.tbl_project_members.hasMany(models.tbl_projects, {foreignKey: ''})
    // I don't know sry
  };
};
