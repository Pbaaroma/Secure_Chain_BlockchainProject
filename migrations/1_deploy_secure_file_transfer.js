const SecureFileTransfer = artifacts.require("SecureFileTransfer");

module.exports = async function (deployer) {
  await deployer.deploy(SecureFileTransfer);
};