import { useEffect, useState } from "react";
import { ethers } from "ethers";
import contractArtifact from "./SecureFileTransfer.json";

// Local Ganache configuration
const CHAIN_ID = 1337n;
const RPC_URL = "http://127.0.0.1:7545";

// Previously deployed contract address.
// Update if Ganache has been reset or contract redeployed.
const CONTRACT_ADDRESS =
  "0x1354E36D461851aFA2DC95107694874b1e896bbA";

const REGISTER_SIGNATURE =
  "registerFile(string,bytes32,address)";

const VERIFY_SIGNATURE =
  "verifyFile(uint256,bytes32)";

const shortAddress = (address) =>
  address
    ? `${address.slice(0, 8)}...${address.slice(-6)}`
    : "";

async function calculateFileHash(file) {
  const buffer = await file.arrayBuffer();
  const digest = await crypto.subtle.digest(
    "SHA-256",
    buffer
  );

  return ethers.hexlify(new Uint8Array(digest));
}

function App() {
  const [account, setAccount] = useState("");
  const [file, setFile] = useState(null);
  const [recipient, setRecipient] = useState("");
  const [fileId, setFileId] = useState("");
  const [verifyFileInput, setVerifyFileInput] =
    useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // Display connected account without requesting
  // wallet permission automatically.
  useEffect(() => {
    if (!window.ethereum) return;

    let active = true;

    const refreshAccounts = async () => {
      try {
        const accounts = await window.ethereum.request({
          method: "eth_accounts",
        });

        if (active) {
          setAccount(accounts[0] || "");
        }
      } catch (error) {
        console.error("Wallet check:", error);
      }
    };

    const onAccountsChanged = (accounts) => {
      setAccount(accounts[0] || "");
    };

    const onChainChanged = () => {
      setMessage(
        "Network changed. Check that Ganache Local is selected."
      );
    };

    refreshAccounts();

    window.ethereum.on?.(
      "accountsChanged",
      onAccountsChanged
    );
    window.ethereum.on?.(
      "chainChanged",
      onChainChanged
    );

    return () => {
      active = false;
      window.ethereum.removeListener?.(
        "accountsChanged",
        onAccountsChanged
      );
      window.ethereum.removeListener?.(
        "chainChanged",
        onChainChanged
      );
    };
  }, []);

  const connectWallet = async () => {
    try {
      if (!window.ethereum) {
        throw new Error(
          "MetaMask is not installed."
        );
      }

      const accounts = await window.ethereum.request({
        method: "eth_requestAccounts",
      });

      const provider = new ethers.BrowserProvider(
        window.ethereum
      );

      const network = await provider.getNetwork();

      if (network.chainId !== CHAIN_ID) {
        throw new Error(
          "Switch MetaMask to Ganache Local (Chain ID 1337)."
        );
      }

      setAccount(accounts[0]);
      setMessage("Wallet connected successfully.");
    } catch (error) {
      console.error("Wallet connection:", error);
      setMessage(
        error.shortMessage ||
          error.message ||
          "Wallet connection failed."
      );
    }
  };

  // Confirm contract exists and ABI matches Solidity.
  const getContract = async (write = false) => {
    if (!window.ethereum) {
      throw new Error("MetaMask is not installed.");
    }

    const provider = new ethers.BrowserProvider(
      window.ethereum
    );

    const network = await provider.getNetwork();

    if (network.chainId !== CHAIN_ID) {
      throw new Error(
        "Wrong network. Select Ganache Local."
      );
    }

    if (!ethers.isAddress(CONTRACT_ADDRESS)) {
      throw new Error("Invalid contract address.");
    }

    const code = await provider.getCode(
      CONTRACT_ADDRESS
    );

    if (code === "0x") {
      throw new Error(
        "Contract not found at this address. Check Ganache deployment."
      );
    }

    const abi = contractArtifact.abi;

    if (!Array.isArray(abi)) {
      throw new Error("Invalid contract ABI.");
    }

    const contractInterface = new ethers.Interface(abi);

    try {
      contractInterface.getFunction(
        REGISTER_SIGNATURE
      );
      contractInterface.getFunction(
        VERIFY_SIGNATURE
      );
    } catch {
      throw new Error(
        "Contract ABI is outdated. Recompile and copy the latest Truffle artifact."
      );
    }

    const runner = write
      ? await provider.getSigner()
      : provider;

    return new ethers.Contract(
      CONTRACT_ADDRESS,
      abi,
      runner
    );
  };

  // REGISTER FILE
  const registerFile = async () => {
    if (!file) {
      setMessage("Please select a file first.");
      return;
    }

    if (!window.ethereum) {
      setMessage("Please install MetaMask.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      await window.ethereum.request({
        method: "eth_requestAccounts",
      });

      const contract = await getContract(true);

      const signerAddress =
        await contract.runner.getAddress();

      const recipientAddress = recipient.trim()
        ? recipient.trim()
        : signerAddress;

      if (
        !ethers.isAddress(recipientAddress) ||
        recipientAddress === ethers.ZeroAddress
      ) {
        throw new Error(
          "Enter a valid recipient wallet address."
        );
      }

      const fileHash = await calculateFileHash(file);

      if (fileHash === ethers.ZeroHash) {
        throw new Error(
          "Invalid file hash."
        );
      }

      setMessage(
        "Please confirm the registration transaction in MetaMask."
      );

      const tx = await contract[
        REGISTER_SIGNATURE
      ](
        file.name,
        fileHash,
        recipientAddress
      );

      setMessage(
        "Transaction submitted. Waiting for confirmation..."
      );

      const receipt = await tx.wait();

      if (!receipt || receipt.status !== 1) {
        throw new Error(
          "Blockchain transaction failed."
        );
      }

      let registeredId = null;

      for (const log of receipt.logs) {
        try {
          const parsed =
            contract.interface.parseLog(log);

          if (parsed?.name === "FileRegistered") {
            registeredId =
              parsed.args.fileId.toString();
            break;
          }
        } catch {
          // Ignore logs not recognized by the ABI.
        }
      }

      if (registeredId === null) {
        throw new Error(
          "Transaction confirmed, but FileRegistered event was not found."
        );
      }

      setFileId(registeredId);
      setVerifyFileInput(file);
      setAccount(signerAddress);

      setMessage(
        `File registered successfully! File ID: ${registeredId}`
      );
    } catch (error) {
      console.error("Registration error:", error);

      setMessage(
        `Registration failed: ${
          error.shortMessage ||
          error.reason ||
          error.message ||
          "Unknown error"
        }`
      );
    } finally {
      setLoading(false);
    }
  };

  // VERIFY FILE
  const verifyFile = async () => {
    if (!/^\d+$/.test(fileId.trim())) {
      setMessage(
        "Enter a valid numeric File ID."
      );
      return;
    }

    if (!verifyFileInput) {
      setMessage(
        "Choose the original file to verify."
      );
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const contract = await getContract(false);

      const fileHash = await calculateFileHash(
        verifyFileInput
      );

      const result = await contract[
        VERIFY_SIGNATURE
      ](
        BigInt(fileId),
        fileHash
      );

      setMessage(
        result
          ? "File verified successfully! The SHA-256 hash matches the blockchain record."
          : "Verification failed! The selected file does not match the registered hash."
      );
    } catch (error) {
      console.error("Verification error:", error);

      setMessage(
        `Verification failed: ${
          error.shortMessage ||
          error.reason ||
          error.message ||
          "Unknown error"
        }`
      );
    } finally {
      setLoading(false);
    }
  };

  const buttonStyle = {
    background: "#ffd900",
    color: "#222",
    border: "none",
    padding: "12px 24px",
    borderRadius: "8px",
    cursor: loading ? "wait" : "pointer",
    fontWeight: "bold",
    marginTop: "12px",
  };

  const inputStyle = {
    width: "100%",
    maxWidth: "380px",
    padding: "12px",
    borderRadius: "7px",
    border: "1px solid #aac4ef",
    boxSizing: "border-box",
    marginTop: "8px",
  };

  return (
    <main
      style={{
        minHeight: "100vh",
        background:
          "linear-gradient(135deg, #071b41, #1559aa)",
        color: "white",
        padding: "40px 16px",
        fontFamily: "Arial, sans-serif",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          maxWidth: "550px",
          margin: "auto",
          padding: "30px",
          background: "rgba(255,255,255,0.09)",
          borderRadius: "16px",
          textAlign: "center",
          boxShadow: "0 8px 30px rgba(0,0,0,0.2)",
        }}
      >
        <h1>🔐 Secure Chain</h1>

        <p>
          Blockchain-Based Secure File Transfer System
        </p>

        <button
          style={buttonStyle}
          onClick={connectWallet}
          disabled={loading}
        >
          {account
            ? "Wallet Connected"
            : "Connect MetaMask"}
        </button>

        {account && (
          <p>
            Connected: {shortAddress(account)}
          </p>
        )}

        <hr style={{ margin: "28px 0" }} />

        <section>
          <h2>Register a File</h2>

          <p>
            Select a file to record its SHA-256 hash
            on Ganache.
          </p>

          <input
            type="file"
            aria-label="File to register"
            style={inputStyle}
            onChange={(event) =>
              setFile(
                event.target.files?.[0] || null
              )
            }
          />

          <p>
            Recipient wallet address (optional for
            local testing)
          </p>

          <input
            type="text"
            aria-label="Recipient wallet address"
            placeholder="0x... (defaults to your wallet)"
            value={recipient}
            onChange={(event) =>
              setRecipient(event.target.value)
            }
            style={inputStyle}
          />

          <div>
            <button
              style={buttonStyle}
              onClick={registerFile}
              disabled={loading}
            >
              {loading
                ? "Processing..."
                : "Register File"}
            </button>
          </div>
        </section>

        <hr style={{ margin: "28px 0" }} />

        <section>
          <h2>Verify File</h2>

          <input
            type="text"
            inputMode="numeric"
            aria-label="File ID"
            placeholder="Enter File ID"
            value={fileId}
            onChange={(event) =>
              setFileId(event.target.value)
            }
            style={inputStyle}
          />

          <input
            type="file"
            aria-label="File to verify"
            style={inputStyle}
            onChange={(event) =>
              setVerifyFileInput(
                event.target.files?.[0] || null
              )
            }
          />

          <div>
            <button
              style={buttonStyle}
              onClick={verifyFile}
              disabled={loading}
            >
              {loading
                ? "Processing..."
                : "Verify File"}
            </button>
          </div>
        </section>

        {message && (
          <div
            role="status"
            style={{
              marginTop: "25px",
              padding: "16px",
              background: "rgba(255,255,255,0.15)",
              borderRadius: "8px",
              overflowWrap: "anywhere",
            }}
          >
            {message}
          </div>
        )}

        <footer
          style={{
            marginTop: "35px",
            fontSize: "12px",
            opacity: 0.85,
          }}
        >
          Powered by Ethereum, Ganache, Truffle
          and MetaMask
        </footer>
      </div>
    </main>
  );
}

export default App;