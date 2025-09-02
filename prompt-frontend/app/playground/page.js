"use client";

import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { MessageSquare, ArrowRight } from "lucide-react";
import ChatScreen from "./chat";

export default function Playground() {
  const [chatbotName, setChatbotName] = useState("");
  const [displayName, setDisplayName] = useState("Chatbot");
  const [placeholderText, setPlaceholderText] = useState(
    "Hi there! I'm here to assist you. What can I do for you today?"
  );
  const [welcomeMessage, setWelcomeMessage] = useState(
    "Hello there, How was your day?"
  );
  const [headerText, setHeaderText] = useState("Hi there, How can I help you?");
  const [assistantText, setAssistantText] = useState(
    "Need help navigating the website?"
  );
  const [aiMsgBg, setAiMsgBg] = useState("#1C2454");
  const [userMsgBg, setUserMsgBg] = useState("#07953F");
  const [accentColor, setAccentColor] = useState("#f5af1c");
  const [chatIconBg, setChatIconBg] = useState("#1C2454");
  const [profileImage, setProfileImage] = useState(null);
  const [isOpen, setIsOpen] = useState(false);
  const [availableModels, setAvailableModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');

  useEffect(() => {
    // Load available models from localStorage
    const savedModels = localStorage.getItem('aiModels');
    if (savedModels) {
      const models = JSON.parse(savedModels);
      setAvailableModels(models);
      if (models.length > 0) {
        setSelectedModel(`${models[0].id}-${models[0].models[0]}-0`);
      }
    }
  }, []);

  const getAllAvailableModels = () => {
    const allModels = [];
    availableModels.forEach(provider => {
      provider.models.forEach((model, index) => {
        allModels.push({
          id: `${provider.id}-${model}-${index}`,
          name: model,
          provider: provider.provider,
          providerName: provider.name,
          apiKey: provider.apiKey,
          providerId: provider.id
        });
      });
    });
    return allModels;
  };

  const handleImageUpload = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => setProfileImage(reader.result);
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="flex gap-4 p-6 max-w-[1300px] mx-auto">
      {/* Left Side - Chatbot Configuration */}

      <Card className="w-full">
        <CardHeader className="text-lg font-semibold">
          <CardTitle>Chatbot Settings</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Basic Settings */}
          <div>
            <h2 className="text-lg font-semibold">Basic Settings</h2>
            <Label htmlFor="chatbot-name">Chatbot Name</Label>
            <Input
              id="chatbot-name"
              value={chatbotName}
              onChange={(e) => setChatbotName(e.target.value)}
            />
            <Label htmlFor="display-name">Display Name</Label>
            <Input
              id="display-name"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
            />
          </div>
          <Separator />

          {/* Popup Message Settings */}
          <div>
            <h2 className="text-lg font-semibold">Popup Message</h2>
            <Label htmlFor="placeholder-text">Placeholder Text</Label>
            <Textarea
              id="placeholder-text"
              value={placeholderText}
              onChange={(e) => setPlaceholderText(e.target.value)}
            />
            <Label htmlFor="welcome-message">Welcome Message</Label>
            <Textarea
              id="welcome-message"
              value={welcomeMessage}
              onChange={(e) => setWelcomeMessage(e.target.value)}
            />
            <Label htmlFor="header-text">Header Text</Label>
            <Textarea
              id="header-text"
              value={headerText}
              onChange={(e) => setHeaderText(e.target.value)}
            />
            <Label htmlFor="assistant-text">Assistant Text</Label>
            <Textarea
              id="assistant-text"
              value={assistantText}
              onChange={(e) => setAssistantText(e.target.value)}
            />
          </div>
          <Separator />

          {/* Appearance Settings */}
          <div>
            <h2 className="text-lg font-semibold">Appearance</h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="ai-msg-bg">AI Message Background</Label>
                <Input
                  type="color"
                  id="ai-msg-bg"
                  value={aiMsgBg}
                  onChange={(e) => setAiMsgBg(e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="user-msg-bg">User Message Background</Label>
                <Input
                  type="color"
                  id="user-msg-bg"
                  value={userMsgBg}
                  onChange={(e) => setUserMsgBg(e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="accent-color">Accent Color</Label>
                <Input
                  type="color"
                  id="accent-color"
                  value={accentColor}
                  onChange={(e) => setAccentColor(e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="chat-icon-bg">Chat Icon Background</Label>
                <Input
                  type="color"
                  id="chat-icon-bg"
                  value={chatIconBg}
                  onChange={(e) => setChatIconBg(e.target.value)}
                />
              </div>
            </div>
            <Label htmlFor="profile-image">Chatbot Profile Image</Label>
            <Input
              type="file"
              id="profile-image"
              accept="image/*"
              onChange={handleImageUpload}
            />
          </div>
          <Button className="w-full">Save Changes</Button>
        </CardContent>
      </Card>
      {/* Right Side - Chatbot UI Preview */}
      {!isOpen && <Card className="p-4 w-[800px] h-[600px]">
        <CardHeader className="flex flex-row space-x-4 items-center">
          {profileImage ? (
            <img
              src={profileImage}
              alt="Chatbot Profile"
              className="w-12 h-12 rounded-full object-cover"
              style={{ backgroundColor: chatIconBg }}
            />
          ) : (
            <div
              className="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold"
              style={{ backgroundColor: chatIconBg }}
            >
              {displayName[0] || "C"}
            </div>
          )}
          <div className="font-extrabold">{displayName}</div>
        </CardHeader>
        <CardContent className="space-y-12">
          <p className="text-lg font-bold mt-4 ml-1">{headerText}</p>
          <div className="mt-4 space-y-2">
            <Card>
              <CardHeader>
                <CardTitle>{assistantText}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                  <Button
                    variant="outline"
                    className="w-full flex items-center justify-start px-4 py-2 bg-gray-100 hover:bg-gray-200"
                    onClick={() => setIsOpen(true)}
                  >
                    <MessageSquare className="text-brown-700" size={20} />
                    <span>Chat with us</span>
                    <ArrowRight className="ml-auto text-gray-500" size={18} />
                  </Button>
              </CardContent>
            </Card>
          </div>
        </CardContent>
      </Card>}
      {isOpen && <div className="w-[800px] h-[600px]">
        <ChatScreen
                    welcomeMessage={welcomeMessage}
                    aiMsgBg={aiMsgBg}
                    userMsgBg={userMsgBg}
                    accentColor={accentColor}
                    chatIconBg={chatIconBg}
                    profileImage={profileImage}
                    displayName = {displayName}
                    selectedModel={selectedModel}
                    availableModels={availableModels}
                    onClose={() => setIsOpen(false)}
                  />
      </div>
                  }
    </div>
  );
}
