import axios from "axios";

export const pythonClient = axios.create({
  baseURL: import.meta.env.VITE_PYTHON_API_BASE || "/api/python",
  timeout: 300_000,
});

export const rClient = axios.create({
  baseURL: import.meta.env.VITE_R_API_BASE || "/api/r",
  timeout: 300_000,
});
