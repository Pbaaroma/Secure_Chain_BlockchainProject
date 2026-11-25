module.exports = {
  contracts_directory: "./truffle-contracts",
  migrations_directory: "./migrations",
  contracts_build_directory: "./build/contracts",

  networks: {
    development: {
      host: "securechain-ganache",
      port: 7545,
      network_id: 1337
    }
  },

  compilers: {
    solc: {
      version: "0.8.34",
      settings: {
        evmVersion: "shanghai"
      }
    }
  }
};
