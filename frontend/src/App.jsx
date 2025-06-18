import { useState } from 'react';
import axios from 'axios';
import avatar from '../public/avatar.jpeg';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    { role: 'system', content: 'Hi! I\'m Ava. How can I assist?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages([...messages, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await axios.post(`${import.meta.env.VITE_API_URL}/ask`, {
        question: input
      });

      const botReply = {
        role: 'assistant',
        content: res.data.answer || 'No response received.'
      };

      setMessages(prev => [...prev, botReply]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Error: Could not reach Ava backend.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  return (
    <div className="flex flex-col h-screen mx-auto bg-white shadow-2xl rounded-lg overflow-hidden max-w-2xl border border-gray-300 relative">
      <div className="sticky top-0 bg-white z-10">
        <div className="flex items-center gap-4 p-4 bg-gray-100 border-b border-gray-300">
          <img src={avatar} alt="Ava" className="w-18 h-18 rounded-full object-cover border" />
          <div>
            <h2 className="font-bold text-2xl">Ava</h2>
            <p className="text-md text-gray-500 font-semibold">Florian's AI Assistant</p>
          </div>
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
      </div>

      <div className="sticky bottom-0 bg-white z-10">
        <div className="flex items-center gap-2 p-4">
          <input
            type="text"
            className="flex-1 rounded px-3 py-2 text-sm border-gray-300 border"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
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
    </div>
  );
}

export default App;
