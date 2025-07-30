"use client";
import { useState, useEffect, useRef } from "react";

interface Message {
  id: number;
  text: string;
  isUser: boolean;
}

const Chat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messageId = useRef(0);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed) return;
    
    const userMessage: Message = { id: messageId.current++, text: trimmed, isUser: true };
    setMessages((msgs) => [...msgs, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmed }),
      });
      const data = await res.json();

      const botMessage: Message = { id: messageId.current++, text: data.response, isUser: false };
      setMessages((msgs) => [...msgs, botMessage]);
    } catch (error) {
      const errorMessage: Message = { id: messageId.current++, text: "Failed to get response. Please try again.", isUser: false };
      setMessages((msgs) => [...msgs, errorMessage]);
    }
    setIsLoading(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col max-w-xl mx-auto h-screen p-4 bg-gray-100">
      <div className="flex-1 overflow-y-auto mb-4 p-2 bg-white rounded shadow">
        {messages.length === 0 && (
          <p className="text-center text-gray-400 mt-20">Start chatting by typing below...</p>
        )}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`mb-3 flex ${msg.isUser ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[70%] px-4 py-2 rounded-lg whitespace-pre-wrap 
              ${msg.isUser ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-800"}`}
            >
              {msg.text}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          sendMessage();
        }}
        className="flex items-center"
      >
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          placeholder="Type your message..."
          className="flex-grow border border-gray-300 rounded p-2 resize-none focus:outline-none focus:ring-2 focus:ring-blue-400"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading}
          className="ml-2 bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
        >
          {isLoading ? "Embedding" : "Send"}
        </button>
      </form>
    </div>
  );
};

export default Chat;
