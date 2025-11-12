import { useRef } from 'react';
import avatar from '../public/avatar.jpeg';
import './App.css';
import StartupNotice from './components/StartupNotice';
import { useAvaChat } from './hooks/useAvaChat';
import { useScrollToBottom } from './hooks/useScrollToBottom';

function App() {
  const { input, loading, messages, sendMessage, setInput } = useAvaChat();
  const bottomRef = useRef(null);

  useScrollToBottom(bottomRef, [messages, loading], !loading);

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-screen w-screen md:w-3xl max-w-full mx-auto bg-white shadow-2xl overflow-hidden border border-gray-300">
      <StartupNotice />
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
          onChange={(event) => setInput(event.target.value)}
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
  );
}

export default App;
