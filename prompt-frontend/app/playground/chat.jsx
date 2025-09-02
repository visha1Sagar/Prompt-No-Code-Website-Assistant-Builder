"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { X, Settings, Bot } from "lucide-react";
import config from "@/lib/config";

export default function ChatScreen({
  welcomeMessage,
  aiMsgBg,
  userMsgBg,
  accentColor,
  chatIconBg,
  profileImage,
  displayName,
  selectedModel,
  availableModels,
  onClose,
}) {
  const [messages, setMessages] = useState([{ text: welcomeMessage, sender: "bot" }]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [currentModel, setCurrentModel] = useState(selectedModel);
  const [showModelSelector, setShowModelSelector] = useState(false);

  useEffect(() => {
    setCurrentModel(selectedModel);
  }, [selectedModel]);

  const getAllAvailableModels = () => {
    if (!availableModels || availableModels.length === 0) return [];
    const allModels = [];
    availableModels.forEach(provider => {
      provider.models.forEach((model, index) => {
        allModels.push({
          id: `${provider.id}-${model}-${index}`,
          name: model,
          provider: provider.provider,
          providerName: provider.name,
          apiKey: provider.apiKey
        });
      });
    });
    return allModels;
  };

  const getCurrentModelInfo = () => {
    const allModels = getAllAvailableModels();
    return allModels.find(m => m.id === currentModel);
  };

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;
    const context = messages.map((msg) => msg.text).join(" ");
    const newMessages = [...messages, { text: input, sender: "user" }];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);

    // Get the current model info for API request
    const modelInfo = getCurrentModelInfo();
    
    const response = await fetch(`${config.backendUrl}/query_bot/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        "bot_id": localStorage.getItem("bot_id"),
        "query": input,
        "context": context,
        "model": modelInfo ? {
          provider: modelInfo.provider,
          model_name: modelInfo.name,
          api_key: modelInfo.apiKey
        } : null
      }),
    });

    const data = await response.json();
    setMessages([...newMessages, { text: data.answer, sender: "bot" }]);
    setIsLoading(false);
  };

  // Handle "Enter" key press
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <Card className="fixed bottom-10 right-10 w-96 h-[500px] shadow-lg rounded-lg flex flex-col overflow-hidden">
      <CardHeader className="flex items-center flex-row justify-between p-4" style={{ backgroundColor: accentColor }}>
        <div className="flex items-center gap-2 flex-1">
          {profileImage ? (
            <img src={profileImage} alt="Chatbot" className="w-10 h-10 rounded-full" />
          ) : (
            <div className="w-10 h-10 rounded-full flex items-center justify-center text-white" style={{ backgroundColor: chatIconBg }}>
                {"C"}
            </div>
          )}
          <div className="flex-1">
            <CardTitle className="text-white text-sm">{displayName || "C"}</CardTitle>
            {getCurrentModelInfo() && (
              <p className="text-white/80 text-xs">
                {getCurrentModelInfo().name}
              </p>
            )}
          </div>
        </div>
        <div className="flex items-center gap-2">
          {availableModels.length > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowModelSelector(!showModelSelector)}
              className="text-white hover:bg-white/20 p-1"
            >
              <Settings size={16} />
            </Button>
          )}
          <Button variant="ghost" size="sm" onClick={onClose} className="text-white hover:bg-white/20 p-1">
            <X size={16} />
          </Button>
        </div>
      </CardHeader>

      {/* Model Selector */}
      {showModelSelector && availableModels.length > 0 && (
        <div className="p-3 border-b bg-gray-50">
          <div className="text-sm font-medium mb-2">Select AI Model:</div>
          <select
            value={currentModel}
            onChange={(e) => setCurrentModel(e.target.value)}
            className="w-full p-2 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {getAllAvailableModels().map((model) => (
              <option key={model.id} value={model.id}>
                {model.name} ({model.providerName})
              </option>
            ))}
          </select>
        </div>
      )}

      <CardContent className="flex-1 p-4 overflow-y-auto space-y-2">
        {messages.map((msg, index) => (
          <div key={index} className={`flex gap-2 ${msg.sender === "bot" ? "justify-start" : "justify-end"}`}>
            {msg.sender === "bot" && (
              profileImage ? (
                <img src={profileImage} alt="Chatbot" className="w-8 h-8 rounded-full" />
              ) : (
                <div className="w-8 h-8 rounded-full flex items-center justify-center text-white" style={{ backgroundColor: chatIconBg }}>
                  {"C"}
                </div>
              )
            )}
            <div className={`p-2 rounded-lg max-w-[75%] text-white`} style={{ backgroundColor: msg.sender === "bot" ? aiMsgBg : userMsgBg }}>
              {msg.text}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center gap-2 justify-start">
            {profileImage ? (
              <img src={profileImage} alt="Chatbot" className="w-8 h-8 rounded-full" />
            ) : (
              <div className="w-8 h-8 rounded-full flex items-center justify-center text-white" style={{ backgroundColor: chatIconBg }}>
                {"C"}
              </div>
            )}
            <div className="flex space-x-1">
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150"></span>
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-300"></span>
            </div>
          </div>
        )}
      </CardContent>

      <div className="p-4 flex border-t">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown} // Added Enter key handler
          className="flex-1"
          placeholder="Type a message..."
        />
        <Button onClick={sendMessage} className="ml-2" style={{ backgroundColor: accentColor }} disabled={isLoading}>
          Send
        </Button>
      </div>
    </Card>
  );
}
