// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract SecureFileTransfer {

    struct FileRecord {
        string fileName;
        bytes32 fileHash;
        address sender;
        address recipient;
        uint256 timestamp;
    }

    FileRecord[] private files;

    event FileRegistered(
        uint256 indexed fileId,
        address indexed sender,
        address indexed recipient
    );

    function registerFile(
        string memory _fileName,
        bytes32 _fileHash,
        address _recipient
    ) public {
        require(_recipient != address(0), "Invalid recipient");
        require(_fileHash != bytes32(0), "Invalid file hash");

        files.push(FileRecord({
            fileName: _fileName,
            fileHash: _fileHash,
            sender: msg.sender,
            recipient: _recipient,
            timestamp: block.timestamp
        }));

        emit FileRegistered(
            files.length - 1,
            msg.sender,
            _recipient
        );
    }

    function getFile(uint256 _fileId)
        public
        view
        returns (FileRecord memory)
    {
        require(_fileId < files.length, "File not found");
        return files[_fileId];
    }

    function verifyFile(
        uint256 _fileId,
        bytes32 _fileHash
    ) public view returns (bool) {
        require(_fileId < files.length, "File not found");
        return files[_fileId].fileHash == _fileHash;
    }

    function getFileCount() public view returns (uint256) {
        return files.length;
    }
}