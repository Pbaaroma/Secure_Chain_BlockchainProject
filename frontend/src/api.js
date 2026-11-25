const API_URL = "http://127.0.0.1:9100";

async function request(endpoint, options = {}) {
  const response = await fetch(
    `${API_URL}${endpoint}`,
    options
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));

    throw new Error(
      typeof error.detail === "string"
        ? error.detail
        : `Request failed: ${response.status}`
    );
  }

  return response;
}

export async function getStatus() {
  const response = await request("/api/status");
  return response.json();
}

export async function getFiles() {
  const response = await request("/api/files");
  return response.json();
}

export async function uploadFile(file) {
  const form = new FormData();
  form.append("file", file);

  const response = await request("/api/upload", {
    method: "POST",
    body: form
  });

  return response.json();
}

export async function verifyFile(fileId, file) {
  const form = new FormData();
  form.append("file", file);

  const response = await request(
    `/api/verify/${fileId}`,
    {
      method: "POST",
      body: form
    }
  );

  return response.json();
}

export async function recoverFile(fileId, source) {
  const response = await request(
    `/api/recover/${fileId}/${source}`
  );

  return response.blob();
}
