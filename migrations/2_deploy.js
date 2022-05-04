// migrations/2_deploy.js
// SPDX-License-Identifier: MIT
const sfpcode = artifacts.require("SFPCODE_v1");

module.exports = function(deployer) {
  deployer.deploy(sfpcode);
};