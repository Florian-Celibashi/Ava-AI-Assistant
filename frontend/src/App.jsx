import { useState, useEffect, useRef } from 'react';
import avatar from '../public/avatar.jpeg';
import './App.css';

const MAX_HISTORY_MESSAGES = 8;
const INLINE_FORMAT_PATTERN = /(\*\*[^*]+\*\*|\[[^\]]+\]\(https?:\/\/[^)\s]+\)|https?:\/\/[^\s]+)/g;

function renderInlineFormattedText(text) {
  const nodes = [];
  let cursor = 0;
  let match;

  while ((match = INLINE_FORMAT_PATTERN.exec(text)) !== null) {
    const token = match[0];
    if (match.index > cursor) {
      nodes.push(text.slice(cursor, match.index));
    }

    if (token.startsWith('**') && token.endsWith('**')) {
      nodes.push(<strong key={`b-${match.index}`}>{token.slice(2, -2)}</strong>);
    } else if (token.startsWith('[')) {
      const linkMatch = token.match(/^\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)$/);
      if (linkMatch) {
        nodes.push(
          <a
            key={`m-${match.index}`}
            href={linkMatch[2]}
            target="_blank"
            rel="noopener noreferrer"
            className="underline text-blue-700 hover:text-blue-800"
          >
            {linkMatch[1]}
          </a>
        );
      } else {
        nodes.push(token);
      }
    } else {
      nodes.push(
        <a
          key={`u-${match.index}`}
          href={token}
          target="_blank"
          rel="noopener noreferrer"
          className="underline text-blue-700 hover:text-blue-800"
        >
          {token}
        </a>
      );
    }
    cursor = match.index + token.length;
  }

  if (cursor < text.length) {
    nodes.push(text.slice(cursor));
  }

  return nodes;
}

function renderMessageContent(content, role) {
  if (role === 'user') {
    return content;
  }

  return content.split('\n').map((line, idx, lines) => (
    <span key={`line-${idx}`}>
      {renderInlineFormattedText(line)}
      {idx < lines.length - 1 && <br />}
    </span>
  ));
}

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
        res = await fetch('/api/ask', {
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
            className={`max-w-[85%] px-4 py-2 rounded-lg text-sm whitespace-pre-wrap break-words ${msg.role === 'user'
              ? 'ml-auto bg-blue-100 text-gray-800'
              : 'mr-auto bg-indigo-100 text-gray-800'
              }`}
          >
            {renderMessageContent(msg.content, msg.role)}
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
