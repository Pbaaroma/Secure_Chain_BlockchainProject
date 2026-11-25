import { useState, useEffect } from "react";

import {
  getStatus,
  getFiles,
  uploadFile,
  verifyFile,
  recoverFile
} from "./api";

import "./SecureChain.css";

function App() {
  const [status, setStatus] = useState(null);
  const [files, setFiles] = useState([]);
  const [file, setFile] = useState(null);
  const [verifyInput, setVerifyInput] = useState(null);
  const [fileId, setFileId] = useState("");
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("info");
  const [loading, setLoading] = useState(false);
  const [online, setOnline] = useState(false);

  function notify(text, type = "info") {
    setMessage(text);
    setMessageType(type);
  }

  async function refreshDashboard() {
    try {
      const [systemStatus, history] = await Promise.all([
        getStatus(),
        getFiles()
      ]);

      setStatus(systemStatus);
      setFiles(history.files);
      setOnline(true);
    } catch {
      setOnline(false);
    }
  }

  useEffect(() => {
    refreshDashboard();

    const timer = setInterval(refreshDashboard, 5000);

    return () => clearInterval(timer);
  }, []);

  async function handleUpload() {
    if (!file) {
      notify("Please select a file.", "error");
      return;
    }

    setLoading(true);
    notify("Encrypting file and registering on blockchain...");

    try {
      const result = await uploadFile(file);

      setFileId(String(result.file_id));
      setVerifyInput(file);

      notify(
        `File encrypted and uploaded successfully. ` +
        `File ID: ${result.file_id}. ` +
        `Block: ${result.block_number}. ` +
        `Transaction: ${result.transaction_hash}`,
        "success"
      );

      await refreshDashboard();
    } catch (error) {
      notify(error.message, "error");
    } finally {
      setLoading(false);
    }
  }

  async function handleVerify() {
    if (!verifyInput || !/^\d+$/.test(fileId.trim())) {
      notify("Enter a valid file ID and select a file.", "error");
      return;
    }

    setLoading(true);

    try {
      const result = await verifyFile(fileId, verifyInput);

      notify(
        result.verified
          ? "File verified successfully. SHA-256 matches the blockchain."
          : "Verification failed. File integrity mismatch detected.",
        result.verified ? "success" : "error"
      );
    } catch (error) {
      notify(error.message, "error");
    } finally {
      setLoading(false);
    }
  }

  async function handleRecovery(item, source) {
    setLoading(true);
    notify(`Recovering file from ${source} server...`);

    try {
      const blob = await recoverFile(item.file_id, source);

      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.download = item.filename;

      document.body.appendChild(link);
      link.click();
      link.remove();

      setTimeout(() => URL.revokeObjectURL(url), 1000);

      notify(
        `File recovered from ${source} server. ` +
        `Decryption and blockchain verification successful.`,
        "success"
      );
    } catch (error) {
      notify(error.message, "error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="securechain">

      <header className="header">
        <div className="brand">
          <h1>🔐 SecureChain</h1>
          <p>Blockchain-Based Secure File Transfer System</p>
        </div>

        <span className={`badge ${online ? "green" : "red"}`}>
          {online ? "● System Online" : "● System Offline"}
        </span>
      </header>

      <div className="container">

        <h2>System Dashboard</h2>

        <div className="dashboard">

          <div className="card">
            <span>Blockchain</span>
            <h3>{online && status?.connected ? "Connected" : "Unavailable"}</h3>
            <small>Ganache Ethereum Network</small>
          </div>

          <div className="card">
            <span>Current Block</span>
            <h3>{online ? status?.block_number : "—"}</h3>
            <small>Chain ID: {online ? status?.chain_id : "—"}</small>
          </div>

          <div className="card">
            <span>Main Server</span>
            <h3>{online ? status?.main_files : "—"}</h3>
            <small>Google Cloud Storage</small>
          </div>

          <div className="card">
            <span>Mirror Server</span>
            <h3>{online ? status?.mirror_files : "—"}</h3>
            <small>
              {!online
                ? "Status unavailable"
                : status?.mirror_synchronized
                  ? "Files synchronized"
                  : "Synchronization pending"}
            </small>
          </div>

        </div>

        <div className="operations">

          <section className="panel">
            <h2>Encrypt & Transfer</h2>

            <p>
              Encrypt your file locally using RSA-2048
              and AES-256-GCM before uploading.
            </p>

            <input
              type="file"
              onChange={event =>
                setFile(event.target.files?.[0] || null)
              }
            />

            <button
              disabled={loading || !online}
              onClick={handleUpload}
            >
              {loading ? "Processing..." : "Encrypt & Upload"}
            </button>

            <small>Automatic blockchain registration</small>
          </section>

          <section className="panel">
            <h2>Verify File Integrity</h2>

            <p>
              Compare a file's SHA-256 hash with its
              registered blockchain record.
            </p>

            <input
              type="text"
              inputMode="numeric"
              placeholder="Enter File ID"
              value={fileId}
              onChange={event => setFileId(event.target.value)}
            />

            <input
              type="file"
              onChange={event =>
                setVerifyInput(event.target.files?.[0] || null)
              }
            />

            <button
              disabled={loading || !online}
              onClick={handleVerify}
            >
              Verify File
            </button>
          </section>

        </div>

        {message && (
          <div role="status" className={`message ${messageType}`}>
            {message}
          </div>
        )}

        <section className="panel history">
          <div className="section-header">
            <h2>Registered File History</h2>

            <button onClick={refreshDashboard}>
              Refresh
            </button>
          </div>

          <p>
            Encrypted files registered on the blockchain.
          </p>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Filename</th>
                  <th>Block</th>
                  <th>Encrypted Size</th>
                  <th>Transaction</th>
                  <th>Recovery</th>
                </tr>
              </thead>

              <tbody>
                {files.map(item => (
                  <tr key={item.file_id}>
                    <td>{item.file_id}</td>
                    <td>{item.filename}</td>
                    <td>{item.block_number}</td>
                    <td>{item.encrypted_size} B</td>

                    <td title={item.transaction_hash}>
                      {item.transaction_hash.slice(0, 12)}...
                    </td>

                    <td className="actions">
                      <button
                        disabled={loading || !online}
                        onClick={() => handleRecovery(item, "main")}
                      >
                        Main
                      </button>

                      <button
                        disabled={loading || !online}
                        onClick={() => handleRecovery(item, "mirror")}
                      >
                        Mirror
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {files.length === 0 && (
              <p>No file records available.</p>
            )}
          </div>
        </section>

        <footer>
          RSA-2048 · AES-256-GCM · SHA-256 · Ethereum ·
          Ganache · Truffle · Python · Google Cloud
          <p>CSCI 311 — Systems Programming</p>
        </footer>

      </div>
    </main>
  );
}

export default App;
