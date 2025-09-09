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
    <div className="flex flex-col lg:flex-row gap-4 p-4 sm:p-6 max-w-[1400px] mx-auto">
      {/* Left Side - Chatbot Configuration */}
      <div className="w-full lg:w-1/2">
        <Card className="w-full">
          <CardHeader className="text-base sm:text-lg font-semibold px-4 sm:px-6">
            <CardTitle className="text-base sm:text-lg">Chatbot Settings</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 sm:space-y-6 px-4 sm:px-6">
            {/* Basic Settings */}
            <div>
              <h2 className="text-base sm:text-lg font-semibold mb-3">Basic Settings</h2>
              <div className="space-y-3">
                <div>
                  <Label htmlFor="chatbot-name" className="text-sm sm:text-base">Chatbot Name</Label>
                  <Input
                    id="chatbot-name"
                    value={chatbotName}
                    onChange={(e) => setChatbotName(e.target.value)}
                    className="text-sm sm:text-base"
                  />
                </div>
                <div>
                  <Label htmlFor="display-name" className="text-sm sm:text-base">Display Name</Label>
                  <Input
                    id="display-name"
                    value={displayName}
                    onChange={(e) => setDisplayName(e.target.value)}
                    className="text-sm sm:text-base"
                  />
                </div>
              </div>
            </div>
            <Separator />

            {/* Popup Message Settings */}
            <div>
              <h2 className="text-base sm:text-lg font-semibold mb-3">Popup Message</h2>
              <div className="space-y-3">
                <div>
                  <Label htmlFor="placeholder-text" className="text-sm sm:text-base">Placeholder Text</Label>
                  <Textarea
                    id="placeholder-text"
                    value={placeholderText}
                    onChange={(e) => setPlaceholderText(e.target.value)}
                    className="text-sm sm:text-base"
                  />
                </div>
                <div>
                  <Label htmlFor="welcome-message" className="text-sm sm:text-base">Welcome Message</Label>
                  <Textarea
                    id="welcome-message"
                    value={welcomeMessage}
                    onChange={(e) => setWelcomeMessage(e.target.value)}
                    className="text-sm sm:text-base"
                  />
                </div>
                <div>
                  <Label htmlFor="header-text" className="text-sm sm:text-base">Header Text</Label>
                  <Textarea
                    id="header-text"
                    value={headerText}
                    onChange={(e) => setHeaderText(e.target.value)}
                    className="text-sm sm:text-base"
                  />
                </div>
                <div>
                  <Label htmlFor="assistant-text" className="text-sm sm:text-base">Assistant Text</Label>
                  <Textarea
                    id="assistant-text"
                    value={assistantText}
                    onChange={(e) => setAssistantText(e.target.value)}
                    className="text-sm sm:text-base"
                  />
                </div>
              </div>
            </div>
            <Separator />

            {/* Appearance Settings */}
            <div>
              <h2 className="text-base sm:text-lg font-semibold mb-3">Appearance</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
                <div>
                  <Label htmlFor="ai-msg-bg" className="text-sm sm:text-base">AI Message Background</Label>
                  <Input
                    type="color"
                    id="ai-msg-bg"
                    value={aiMsgBg}
                    onChange={(e) => setAiMsgBg(e.target.value)}
                    className="h-10 sm:h-12"
                  />
                </div>
                <div>
                  <Label htmlFor="user-msg-bg" className="text-sm sm:text-base">User Message Background</Label>
                  <Input
                    type="color"
                    id="user-msg-bg"
                    value={userMsgBg}
                    onChange={(e) => setUserMsgBg(e.target.value)}
                    className="h-10 sm:h-12"
                  />
                </div>
                <div>
                  <Label htmlFor="accent-color" className="text-sm sm:text-base">Accent Color</Label>
                  <Input
                    type="color"
                    id="accent-color"
                    value={accentColor}
                    onChange={(e) => setAccentColor(e.target.value)}
                    className="h-10 sm:h-12"
                  />
                </div>
                <div>
                  <Label htmlFor="chat-icon-bg" className="text-sm sm:text-base">Chat Icon Background</Label>
                  <Input
                    type="color"
                    id="chat-icon-bg"
                    value={chatIconBg}
                    onChange={(e) => setChatIconBg(e.target.value)}
                    className="h-10 sm:h-12"
                  />
                </div>
              </div>
              <div className="mt-3">
                <Label htmlFor="profile-image" className="text-sm sm:text-base">Chatbot Profile Image</Label>
                <Input
                  type="file"
                  id="profile-image"
                  accept="image/*"
                  onChange={handleImageUpload}
                  className="text-sm sm:text-base"
                />
              </div>
            </div>
            <Button className="w-full text-sm sm:text-base">Save Changes</Button>
          </CardContent>
        </Card>
      </div>

      {/* Right Side - Chatbot UI Preview */}
      <div className="w-full lg:w-1/2">
        {!isOpen && (
          <Card className="p-4 w-full h-[400px] sm:h-[500px] lg:h-[600px]">
            <CardHeader className="flex flex-row space-x-3 sm:space-x-4 items-center px-0">
              {profileImage ? (
                <img
                  src={profileImage}
                  alt="Chatbot Profile"
                  className="w-10 h-10 sm:w-12 sm:h-12 rounded-full object-cover"
                  style={{ backgroundColor: chatIconBg }}
                />
              ) : (
                <div
                  className="w-10 h-10 sm:w-12 sm:h-12 rounded-full flex items-center justify-center text-white font-bold text-sm sm:text-base"
                  style={{ backgroundColor: chatIconBg }}
                >
                  {displayName[0] || "C"}
                </div>
              )}
              <div className="font-extrabold text-sm sm:text-base">{displayName}</div>
            </CardHeader>
            <CardContent className="space-y-8 sm:space-y-12 px-0">
              <p className="text-base sm:text-lg font-bold mt-4 ml-1">{headerText}</p>
              <div className="mt-4 space-y-2">
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm sm:text-base">{assistantText}</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4 pt-0">
                    <Button
                      variant="outline"
                      className="w-full flex items-center justify-start px-3 py-2 sm:px-4 sm:py-2 bg-gray-100 hover:bg-gray-200 text-sm sm:text-base"
                      onClick={() => setIsOpen(true)}
                    >
                      <MessageSquare className="text-brown-700" size={16} />
                      <span className="ml-2">Chat with us</span>
                      <ArrowRight className="ml-auto text-gray-500" size={16} />
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </CardContent>
          </Card>
        )}
        {isOpen && (
          <div className="w-full h-[400px] sm:h-[500px] lg:h-[600px]">
            <ChatScreen
              welcomeMessage={welcomeMessage}
              aiMsgBg={aiMsgBg}
              userMsgBg={userMsgBg}
              accentColor={accentColor}
              chatIconBg={chatIconBg}
              profileImage={profileImage}
              displayName={displayName}
              selectedModel={selectedModel}
              availableModels={availableModels}
              onClose={() => setIsOpen(false)}
            />
          </div>
        )}
      </div>
    </div>
  );
}
