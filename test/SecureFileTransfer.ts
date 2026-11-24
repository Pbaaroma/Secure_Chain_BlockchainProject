import { expect } from "chai";
import { network } from "hardhat";
import { ethers } from "ethers";

const { ethers: hardhatEthers } = await network.connect();

describe("SecureFileTransfer", function () {
  async function deployContract() {
    const [sender, recipient] = await hardhatEthers.getSigners();

    const contract = await hardhatEthers.deployContract(
      "SecureFileTransfer"
    );

    await contract.waitForDeployment();

    return { contract, sender, recipient };
  }

  it("Should register a file", async function () {
    const { contract, recipient } = await deployContract();

    const hash = ethers.id("sample-file");

    await contract.registerFile(
      "document.pdf",
      hash,
      recipient.address
    );

    expect(await contract.getFileCount()).to.equal(1n);
  });

  it("Should retrieve a registered file", async function () {
    const { contract, sender, recipient } = await deployContract();

    const hash = ethers.id("sample-file");

    await contract.registerFile(
      "document.pdf",
      hash,
      recipient.address
    );

    const file = await contract.getFile(0);

    expect(file.fileName).to.equal("document.pdf");
    expect(file.fileHash).to.equal(hash);
    expect(file.sender).to.equal(sender.address);
    expect(file.recipient).to.equal(recipient.address);
  });

  it("Should verify a correct file hash", async function () {
    const { contract, recipient } = await deployContract();

    const hash = ethers.id("sample-file");

    await contract.registerFile(
      "document.pdf",
      hash,
      recipient.address
    );

    expect(await contract.verifyFile(0, hash)).to.equal(true);
  });

  it("Should reject an incorrect file hash", async function () {
    const { contract, recipient } = await deployContract();

    const hash = ethers.id("sample-file");
    const wrongHash = ethers.id("modified-file");

    await contract.registerFile(
      "document.pdf",
      hash,
      recipient.address
    );

    expect(await contract.verifyFile(0, wrongHash)).to.equal(false);
  });

  it("Should reject an invalid recipient", async function () {
    const { contract } = await deployContract();

    const hash = ethers.id("sample-file");

    await expect(
      contract.registerFile(
        "document.pdf",
        hash,
        ethers.ZeroAddress
      )
    ).to.be.revertedWith("Invalid recipient");
  });
});