module.exports = {
  contracts_directory: "./truffle-contracts",
  migrations_directory: "./migrations",

  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545,
      network_id: "*"
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