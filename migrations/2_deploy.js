// migrations/2_deploy.js
// SPDX-License-Identifier: MIT
const chainbox = artifacts.require("ChainBox_v1");

module.exports = function(deployer) {
  deployer.deploy(chainbox);
};