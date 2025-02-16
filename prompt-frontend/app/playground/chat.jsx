"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { X } from "lucide-react";

export default function ChatScreen({
  welcomeMessage,
  aiMsgBg,
  userMsgBg,
  accentColor,
  chatIconBg,
  profileImage,
  displayName,
  onClose,
}) {
  const [messages, setMessages] = useState([{ text: welcomeMessage, sender: "bot" }]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;
    const context = messages.map((msg) => msg.text).join(" ");
    const newMessages = [...messages, { text: input, sender: "user" }];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);
    const response = await fetch(`https://6983-111-68-97-206.ngrok-free.app/query_bot/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        "bot_id": localStorage.getItem("bot_id"),
        "query": input,
        "context":context
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
        <div className="flex items-center gap-2">
          {profileImage ? (
            <img src={profileImage} alt="Chatbot" className="w-10 h-10 rounded-full" />
          ) : (
            <div className="w-10 h-10 rounded-full flex items-center justify-center text-white" style={{ backgroundColor: chatIconBg }}>
                {"C"}
            </div>
          )}
          <CardTitle className="text-white">{displayName || "C"}</CardTitle>
        </div>
        <button variant="ghost" size="icon" onClick={onClose}>
          <X className="text-white" />
        </button>
      </CardHeader>

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
