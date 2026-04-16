import { useState, useEffect, useRef } from 'react';
import avatar from '../public/avatar.jpeg';
import './App.css';

const API_BASE_URL = (
  import.meta.env.VITE_API_URL ||
  import.meta.env.VITE_BACKEND_URL ||
  ''
).replace(/\/+$/, '');

const MAX_HISTORY_MESSAGES = 8;

function App() {
  const [messages, setMessages] = useState([
    { role: 'system', content: 'Hi! I\'m Ava. How can I assist?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef(null);

  useEffect(() => {
    if (!loading) {
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, loading]);

  const sendMessage = async () => {
    const question = input.trim();
    if (!question || loading) return;

    const userMessage = { role: 'user', content: question };
    const history = messages
      .filter((msg) => msg.role === 'user' || msg.role === 'assistant')
      .slice(-MAX_HISTORY_MESSAGES)
      .map((msg) => ({ role: msg.role, content: msg.content }));

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 60_000);
      let res;
      try {
        res = await fetch(`${API_BASE_URL}/api/ask`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            question,
            history
          }),
          signal: controller.signal
        });
      } finally {
        clearTimeout(timeoutId);
      }

      const payload = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(payload.detail || 'Ava backend request failed.');
      }

      const botReply = {
        role: 'assistant',
        content: payload.answer || 'No response received.'
      };

      setMessages(prev => [...prev, botReply]);
    } catch (error) {
      const fallback = error?.name === 'AbortError'
        ? 'Error: Request timed out. Please try again.'
        : `Error: ${error?.message || 'Could not reach Ava backend.'}`;

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: fallback
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  return (
    <div className="flex flex-col h-screen w-screen md:w-3xl max-w-full mx-auto bg-white shadow-2xl overflow-hidden border border-gray-300">
      <div className="flex items-center gap-4 p-4 bg-gray-100 border-b border-gray-300">
        <img src={avatar} alt="Ava" className="w-18 h-18 rounded-full object-cover border" />
        <div>
          <h2 className="font-bold text-2xl">Ava</h2>
          <p className="text-md text-gray-500 font-semibold">Florian's AI Assistant</p>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto space-y-2 p-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`max-w-fit px-4 py-2 rounded-lg text-sm ${msg.role === 'user'
              ? 'ml-auto bg-blue-100 text-gray-800'
              : 'mr-auto bg-indigo-100 text-gray-800'
              }`}
          >
            {msg.content}
          </div>
        ))}
        {loading && (
          <div className="mr-auto max-w-fit bg-indigo-100 text-gray-800 px-4 py-2 rounded-lg text-sm animate-pulse">
            Ava is typing...
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="flex items-center gap-2 p-4 bg-gray-100 border-t border-gray-300">
        <input
          type="text"
          className="flex-1 rounded px-3 py-2 text-sm border-gray-300 bg-white border"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Type your message..."
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-black text-white px-4 py-2 text-sm rounded disabled:opacity-50"
        >
          {loading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  );

}

export default App;
