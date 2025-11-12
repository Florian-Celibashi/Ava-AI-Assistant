import { useCallback, useState } from 'react';
import { sendChatMessage } from '../services/api';

const INITIAL_MESSAGE = {
  role: 'system',
  content: "Hi! I'm Ava. How can I assist?",
};

/**
 * Encapsulates Ava chat state management.
 * Keeps App.jsx focused on layout while preserving existing behaviour.
 */
export function useAvaChat() {
  const [messages, setMessages] = useState([INITIAL_MESSAGE]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const updateInput = useCallback((value) => {
    setInput(value);
  }, []);

  const sendMessage = useCallback(async () => {
    const trimmed = input.trim();
    if (!trimmed) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const data = await sendChatMessage(trimmed);
      const botReply = {
        role: 'assistant',
        content: data?.answer ?? 'No response received.',
      };
      setMessages((prev) => [...prev, botReply]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Error: Could not reach Ava backend.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  }, [input]);

  return {
    input,
    loading,
    messages,
    sendMessage,
    setInput: updateInput,
  };
}
