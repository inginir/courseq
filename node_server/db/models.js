const Sequelize = require("sequelize");

const usersModel = [
  "users",
  {
    // attributes
    firstName: {
      type: Sequelize.STRING,
      allowNull: false
    },
    lastName: {
      type: Sequelize.STRING
      // allowNull defaults to true
    }
  },
  {
    // options
  }
];

const coursesModel = [
  "courses",
  {
    // attributes
    code: {
      type: Sequelize.STRING,
      allowNull: false
    },
    name: {
      type: Sequelize.STRING
      // allowNull: false
    },
    seasons: {
      type: Sequelize.ARRAY(Sequelize.STRING)
      // allowNull: false
    },
    prereqs: {
      type: Sequelize.ARRAY(Sequelize.STRING)
      // allowNull: false
    },
    coreqs: {
      type: Sequelize.ARRAY(Sequelize.STRING)
      // allowNull: false
    },
    credits: {
      type: Sequelize.FLOAT
      // allowNull defaults to true
    }
  },
  {
    // options
  }
];

module.exports = [usersModel, coursesModel];
