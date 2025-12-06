import React, { useState, useEffect, useRef } from 'react';
import {
    Send, BookOpen, Menu, Plus, MessageSquare,
    Settings, LogOut, Mic, Image as ImageIcon,
    Code, Copy, ThumbsUp, ThumbsDown, RotateCcw
} from 'lucide-react';
import { sendMessage, checkHealth } from '../api/client';

const ChatInterface = () => {
    const [messages, setMessages] = useState([
        {
            role: 'assistant',
            content: 'Hello! I am your NEET AI Tutor. I can help you with Physics, Chemistry, and Biology questions from NCERT.',
            timestamp: new Date().toLocaleTimeString()
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = input;
        setInput('');
        setMessages(prev => [...prev, {
            role: 'user',
            content: userMessage,
            timestamp: new Date().toLocaleTimeString()
        }]);
        setIsLoading(true);

        try {
            const response = await sendMessage(userMessage);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: response.answer,
                sources: response.sources,
                timestamp: new Date().toLocaleTimeString()
            }]);
        } catch (error) {
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: "Sorry, I encountered an error. Please try again later.",
                isError: true,
                timestamp: new Date().toLocaleTimeString()
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex h-screen bg-[#0f1117] text-gray-100 font-sans overflow-hidden">
            {/* Sidebar */}
            <aside className={`${isSidebarOpen ? 'w-64' : 'w-20'} bg-[#161b22] border-r border-gray-800 transition-all duration-300 flex flex-col`}>
                <div className="p-4 flex items-center justify-between border-b border-gray-800">
                    {isSidebarOpen && <span className="font-bold text-xl bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">NEET.AI</span>}
                    <button onClick={() => setIsSidebarOpen(!isSidebarOpen)} className="p-2 hover:bg-gray-800 rounded-lg text-gray-400">
                        <Menu className="h-5 w-5" />
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto p-3 space-y-2">
                    <button className="w-full flex items-center gap-3 p-3 bg-blue-600 hover:bg-blue-700 rounded-xl transition-colors text-white shadow-lg shadow-blue-900/20">
                        <Plus className="h-5 w-5" />
                        {isSidebarOpen && <span className="font-medium">New Chat</span>}
                    </button>

                    <div className="mt-6">
                        {isSidebarOpen && <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3 px-2">Recent Chats</p>}
                        {[1, 2, 3].map((i) => (
                            <button key={i} className="w-full flex items-center gap-3 p-3 hover:bg-gray-800 rounded-lg text-gray-400 hover:text-white transition-colors text-left group">
                                <MessageSquare className="h-4 w-4" />
                                {isSidebarOpen && <span className="truncate text-sm">Biology Chapter {i} Revision</span>}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="p-4 border-t border-gray-800 space-y-2">
                    <button className="w-full flex items-center gap-3 p-2 hover:bg-gray-800 rounded-lg text-gray-400 hover:text-white transition-colors">
                        <Settings className="h-5 w-5" />
                        {isSidebarOpen && <span>Settings</span>}
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col relative">
                {/* Header */}
                <header className="h-16 border-b border-gray-800 flex items-center justify-between px-6 bg-[#0f1117]/80 backdrop-blur-md z-10">
                    <div className="flex items-center gap-3">
                        <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-blue-500 to-purple-600 flex items-center justify-center">
                            <BookOpen className="h-4 w-4 text-white" />
                        </div>
                        <div>
                            <h2 className="font-semibold text-gray-100">AI Tutor Assistant</h2>
                            <p className="text-xs text-green-400 flex items-center gap-1">
                                <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse"></span>
                                Online
                            </p>
                        </div>
                    </div>
                </header>

                {/* Chat Area */}
                <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-gray-800">
                    {messages.map((msg, index) => (
                        <div key={index} className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                            <div className={`h-8 w-8 rounded-full flex-shrink-0 flex items-center justify-center ${msg.role === 'user' ? 'bg-blue-600' : 'bg-purple-600'
                                }`}>
                                {msg.role === 'user' ? <span className="text-xs font-bold">U</span> : <BookOpen className="h-4 w-4" />}
                            </div>

                            <div className={`max-w-[80%] space-y-2 ${msg.role === 'user' ? 'items-end flex flex-col' : ''}`}>
                                <div className={`p-4 rounded-2xl ${msg.role === 'user'
                                        ? 'bg-blue-600 text-white rounded-tr-none'
                                        : 'bg-[#1e2330] border border-gray-800 text-gray-200 rounded-tl-none'
                                    }`}>
                                    <p className="leading-relaxed whitespace-pre-wrap">{msg.content}</p>

                                    {msg.sources && msg.sources.length > 0 && (
                                        <div className="mt-4 pt-3 border-t border-gray-700/50">
                                            <p className="text-xs font-semibold text-gray-400 mb-2 flex items-center gap-2">
                                                <BookOpen className="h-3 w-3" /> Sources
                                            </p>
                                            <div className="flex flex-wrap gap-2">
                                                {msg.sources.map((source, idx) => (
                                                    <span key={idx} className="text-xs bg-gray-800 text-blue-400 px-2 py-1 rounded-md border border-gray-700">
                                                        {source}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>

                                {msg.role === 'assistant' && !msg.isError && (
                                    <div className="flex items-center gap-2 px-2">
                                        <button className="p-1 hover:bg-gray-800 rounded text-gray-500 hover:text-gray-300 transition-colors">
                                            <Copy className="h-3 w-3" />
                                        </button>
                                        <button className="p-1 hover:bg-gray-800 rounded text-gray-500 hover:text-gray-300 transition-colors">
                                            <ThumbsUp className="h-3 w-3" />
                                        </button>
                                        <button className="p-1 hover:bg-gray-800 rounded text-gray-500 hover:text-gray-300 transition-colors">
                                            <RotateCcw className="h-3 w-3" />
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}

                    {isLoading && (
                        <div className="flex gap-4">
                            <div className="h-8 w-8 rounded-full bg-purple-600 flex items-center justify-center animate-pulse">
                                <BookOpen className="h-4 w-4" />
                            </div>
                            <div className="bg-[#1e2330] border border-gray-800 p-4 rounded-2xl rounded-tl-none flex items-center gap-3">
                                <div className="flex gap-1">
                                    <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></span>
                                    <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce delay-100"></span>
                                    <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce delay-200"></span>
                                </div>
                                <span className="text-sm text-gray-400">Analyzing NCERT data...</span>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-6 bg-[#0f1117]">
                    <div className="max-w-4xl mx-auto relative">
                        <form onSubmit={handleSend} className="relative bg-[#1e2330] border border-gray-700 rounded-xl shadow-2xl shadow-black/50 focus-within:ring-2 focus-within:ring-blue-500/50 transition-all">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                placeholder="Ask about Physics, Chemistry, or Biology..."
                                className="w-full bg-transparent text-gray-100 p-4 pr-32 outline-none placeholder-gray-500"
                                disabled={isLoading}
                            />

                            <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
                                <button type="button" className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-colors" title="Voice Input">
                                    <Mic className="h-5 w-5" />
                                </button>
                                <button type="button" className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-colors" title="Upload Image">
                                    <ImageIcon className="h-5 w-5" />
                                </button>
                                <div className="h-6 w-px bg-gray-700 mx-1"></div>
                                <button
                                    type="submit"
                                    disabled={isLoading || !input.trim()}
                                    className="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg shadow-blue-900/20"
                                >
                                    <Send className="h-5 w-5" />
                                </button>
                            </div>
                        </form>
                        <p className="text-center text-xs text-gray-600 mt-3">
                            AI Tutor can make mistakes. Always verify with your NCERT textbooks.
                        </p>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default ChatInterface;
