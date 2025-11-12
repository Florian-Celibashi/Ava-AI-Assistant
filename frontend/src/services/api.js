/**
 * Lightweight API client helpers for the Ava frontend.
 */
import axios from 'axios';

const ASK_ENDPOINT = `${import.meta.env.VITE_API_URL}/ask`;

/**
 * Send a chat question to the backend and return the JSON payload.
 * The backend contract remains unchanged: `{ answer: string }` or `{ error: string }`.
 */
export async function sendChatMessage(question) {
  const response = await axios.post(ASK_ENDPOINT, { question });
  return response.data;
}
