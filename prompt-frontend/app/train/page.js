"use client";
import { useState } from "react";
import {
  Upload,
  Database,
  UploadCloud,
  Trash2,
  Clipboard,
  Check,
  Loader,
  Bot,
  Plus,
  Eye,
  EyeOff,
} from "lucide-react"; // Icons
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import config from "@/lib/config";

export default function TrainPage() {
  const [activeTab, setActiveTab] = useState("upload");
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header with responsive tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4">
          <h1 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">Train</h1>
          {/* Desktop tabs */}
          <nav className="hidden lg:flex space-x-8">
            <TabItem
              icon={<Upload size={18} />}
              label="Website Link and File Upload"
              active={activeTab === "upload"}
              onClick={() => setActiveTab("upload")}
            />
            <TabItem
              icon={<Database size={18} />}
              label="SQL Database Connection"
              disabled={true}
              active={activeTab === "sql"}
              onClick={() => setActiveTab("sql")}
            />
            <TabItem
              icon={<Bot size={18} />}
              label="AI Models Management"
              active={activeTab === "models"}
              onClick={() => setActiveTab("models")}
            />
          </nav>
          {/* Mobile dropdown */}
          <div className="lg:hidden">
            <select
              value={activeTab}
              onChange={(e) => setActiveTab(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md bg-white text-sm font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="upload">Website Link and File Upload</option>
              <option value="sql" disabled>SQL Database Connection (in progress)</option>
              <option value="models">AI Models Management</option>
            </select>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-4 sm:py-8">
        {activeTab === "upload" ? (
          <UploadFiles />
        ) : activeTab === "sql" ? (
          <SQLConnection />
        ) : (
          <ModelsManagement />
        )}
      </main>
    </div>
  );
}

// Tab Item Component
const TabItem = ({ icon, label, active, disabled, onClick }) => {
  return (
    <button
      className={`flex items-center gap-2 sm:gap-3 px-2 sm:px-4 py-2 sm:py-3 text-xs sm:text-sm font-medium rounded-lg transition-all duration-200 ${
        disabled 
          ? "text-gray-400 cursor-not-allowed" 
          : active 
            ? "bg-blue-50 text-blue-700 border border-blue-200" 
            : "text-gray-600 hover:text-gray-900 hover:bg-gray-50"
      }`}
      onClick={disabled ? undefined : onClick}
      disabled={disabled}
    >
      <span className={disabled ? "text-gray-300" : active ? "text-blue-600" : "text-gray-500"}>
        {icon}
      </span>
      <span className="whitespace-nowrap text-xs sm:text-sm">
        {label}
        {disabled && <span className="text-xs ml-1 sm:ml-2 text-gray-400">(in progress)</span>}
      </span>
    </button>
  );
};

const UploadFiles = () => {
  const [files, setFiles] = useState([]);
  const [website, setWebsite] = useState("");
  const [errors, setErrors] = useState({ website: "", files: "" });
  const [copied, setCopied] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [loading, setLoading] = useState(false); // New loader state
  const [scriptUrl, setScriptUrl] = useState("");

  const copyToClipboard = () => {
    navigator.clipboard.writeText(`<script defer src="${scriptUrl}"></script>`);
    setCopied(true);
    setShowPopup(true);
    setTimeout(() => setCopied(false), 2000);
    setTimeout(() => setShowPopup(false), 2000);
  };

  const handleFileUpload = (event) => {
    const selectedFiles = Array.from(event.target.files || []);
    const filteredFiles = selectedFiles.filter((file) =>
      ["application/pdf", "text/plain"].includes(file.type)
    );

    if (filteredFiles.length === 0) {
      setErrors((prev) => ({
        ...prev,
        files: "Only PDF and TXT files are allowed.",
      }));
    } else {
      setErrors((prev) => ({ ...prev, files: "" }));
    }

    setFiles([...files, ...filteredFiles]);
  };

  const handleDelete = (index) => {
    const updatedFiles = files.filter((_, i) => i !== index);
    setFiles(updatedFiles);
  };

  const handleSave = async () => {
    let newErrors = { website: "" };

    if (!website.trim()) {
      newErrors.website = "Website URL is required.";
    }

    setErrors(newErrors);

    if (newErrors.website) return;

    const formData = new FormData();
    formData.append("website_url", website);
    files.forEach((file) => formData.append("files", file));

    // Add user ID for potential future use
    const userId = localStorage.getItem('userId');
    if (userId) {
      formData.append("user_id", userId);
    }

    setLoading(true); // Start loading

    try {
      const response = await fetch(
        `${config.backendUrl}/create_bot/`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) throw new Error("Failed to send data");

      const res = await response.json();
      setScriptUrl(`${config.frontendUrl}/api/chatbot/${res.bot_id}`);
      localStorage.setItem("bot_id", res.bot_id);
    } catch (error) {
      console.error("Error sending data:", error);
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <div className="w-full max-w-none space-y-4 sm:space-y-6">
      {/* Main Card */}
      <Card>
        <CardHeader className="text-base sm:text-lg font-semibold px-4 sm:px-6">
          Set Up Script Configuration
        </CardHeader>
        <CardContent className="space-y-4 px-4 sm:px-6">
          <Card>
            <CardHeader className="text-base sm:text-lg font-semibold px-4 sm:px-6">
              Website Link
            </CardHeader>
            <CardContent className="space-y-4 px-4 sm:px-6">
              <div>
                <Label htmlFor="website" className="text-sm sm:text-base">Website</Label>
                <div className="flex items-center space-x-2">
                  <Input
                    id="website"
                    value={website}
                    onChange={(e) => {
                      setWebsite(e.target.value);
                      setErrors((prev) => ({ ...prev, website: "" }));
                    }}
                    placeholder="https://example.com"
                    className="text-sm sm:text-base"
                  />
                </div>
                {errors.website && (
                  <p className="text-red-500 text-xs sm:text-sm mt-1">{errors.website}</p>
                )}
                <p className="text-xs text-gray-500 mt-1">
                  Your bot will only work on websites with this domain name.
                </p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-base sm:text-lg font-semibold px-4 sm:px-6">
              Upload Files
              <p className="text-gray-500 text-xs sm:text-sm font-normal pt-1 ps-0.5">
                Upload your files to the knowledge base.
              </p>
            </CardHeader>
            <CardContent className="space-y-4 px-4 sm:px-6">
              {/* Drag & Drop Area */}
              <label className="flex flex-col items-center justify-center border-2 border-dashed border-gray-300 p-6 sm:p-10 rounded-lg cursor-pointer hover:bg-gray-50">
                <UploadCloud size={32} className="sm:w-10 sm:h-10 text-gray-400" />
                <p className="text-gray-700 font-medium text-sm sm:text-base text-center">
                  Drag & drop files here, or click to select files
                </p>
                <p className="text-xs sm:text-sm text-gray-500 text-center">
                  Supported File Types:{" "}
                  <span className="text-blue-600">.pdf, .txt</span>
                </p>
                <input
                  type="file"
                  className="hidden"
                  multiple
                  onChange={handleFileUpload}
                  accept=".pdf,.txt"
                />
              </label>
              {errors.files && (
                <p className="text-red-500 text-xs sm:text-sm mt-1">{errors.files}</p>
              )}

              {/* Uploaded Files List */}
              {files.length > 0 && (
                <div>
                  <p className="font-semibold text-sm sm:text-base">
                    Uploaded Files: {files.length}
                  </p>
                  <div className="mt-2 space-y-2">
                    {files.map((file, index) => (
                      <div
                        key={index}
                        className="flex items-center justify-between p-2 sm:p-3 bg-gray-100 rounded-lg"
                      >
                        <span className="text-xs sm:text-sm font-medium truncate flex-1 mr-2">{file.name}</span>
                        <div className="flex items-center space-x-2">
                          <button
                            onClick={() => handleDelete(index)}
                            className="text-red-600 hover:text-red-800 p-1"
                          >
                            <Trash2 size={14} className="sm:w-4 sm:h-4" />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Save Button with Loader */}
          <Button
            className="w-full bg-[#1e2b3b] text-white flex items-center justify-center text-sm sm:text-base"
            onClick={handleSave}
            disabled={loading} // Disable while loading
          >
            {loading ? (
              <>
                <Loader className="animate-spin w-4 h-4 sm:w-5 sm:h-5 mr-2" /> Processing...
              </>
            ) : (
              "Save"
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Embedded Script */}
      <Card>
        <CardHeader className="text-base sm:text-lg font-semibold px-4 sm:px-6">
          Embedded Script
        </CardHeader>
        <CardContent className="px-4 sm:px-6">
          <div className="relative">
            <Textarea
              className="font-mono text-xs sm:text-sm pr-10 h-20 sm:h-24 bg-[#1e2b3b] text-white"
              readOnly
              value={`<script defer src="${scriptUrl}"></script>`}
            />
            <button
              className="absolute top-2 right-2 p-1 sm:p-2 bg-gray-200 rounded-md hover:bg-gray-300"
              onClick={copyToClipboard}
            >
              {copied ? (
                <Check className="w-3 h-3 sm:w-4 sm:h-4 text-[#1e2b3b]" />
              ) : (
                <Clipboard className="w-3 h-3 sm:w-4 sm:h-4" />
              )}
            </button>
          </div>
        </CardContent>
      </Card>

      {/* Copy Popup */}
      {showPopup && (
        <div className="fixed bottom-4 right-4 bg-gray-800 text-white px-3 py-2 sm:px-4 sm:py-2 rounded-md shadow-md text-xs sm:text-sm">
          Copied to clipboard
        </div>
      )}
    </div>
  );
};

// SQL Connection Component
const SQLConnection = () => {
  const [hostName, setHostName] = useState("");
  const [dbName, setDbName] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  return (
    <div className="w-full max-w-none">
      <Card>
        <CardHeader className="text-base sm:text-lg font-semibold px-4 sm:px-6">
          SQL Database Connection
        </CardHeader>
        <CardContent className="space-y-4 px-4 sm:px-6">
          <div>
            <Label htmlFor="host" className="text-sm sm:text-base">Host</Label>
            <Input
              id="host"
              value={hostName}
              onChange={(e) => setHostName(e.target.value)}
              className="text-sm sm:text-base"
            />
          </div>
          <div>
            <Label htmlFor="dbName" className="text-sm sm:text-base">Database Name</Label>
            <Input
              id="dbName"
              value={dbName}
              onChange={(e) => setDbName(e.target.value)}
              className="text-sm sm:text-base"
            />
          </div>
          <div>
            <Label htmlFor="username" className="text-sm sm:text-base">Username</Label>
            <Input
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="text-sm sm:text-base"
            />
          </div>
          <div>
            <Label htmlFor="password" className="text-sm sm:text-base">Password</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="text-sm sm:text-base"
            />
          </div>

          <Button className="w-full bg-[#1e2b3b] text-white text-sm sm:text-base">Save</Button>
        </CardContent>
      </Card>
    </div>
  );
};

// Models Management Component
const ModelsManagement = () => {
  const [models, setModels] = useState(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('aiModels');
      return saved ? JSON.parse(saved) : [];
    }
    return [];
  });
  const [showAddForm, setShowAddForm] = useState(false);
  const [newModel, setNewModel] = useState({
    provider: '',
    apiKey: '',
    name: ''
  });
  const [showApiKeys, setShowApiKeys] = useState({});

  const providerOptions = {
    openai: {
      name: 'OpenAI',
      models: ['gpt-4.1-nano', 'gpt-5-nano', 'gpt-4o-mini'],
      placeholder: 'sk-...'
    },
    gemini: {
      name: 'Google Gemini',
      models: ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-2.5-lite', 'gemini-2.0-flash-exp', 'gemini-1.5-pro-002', 'gemini-1.5-flash-002'],
      placeholder: 'AIza...'
    }
  };

  const handleAddModel = async () => {
    if (!newModel.provider || !newModel.apiKey || !newModel.name) {
      alert('Please fill in all fields');
      return;
    }

    const modelData = {
      id: Date.now().toString(),
      provider: newModel.provider,
      apiKey: newModel.apiKey,
      name: newModel.name,
      models: providerOptions[newModel.provider].models,
      createdAt: new Date().toISOString()
    };

    // Generate or get user ID
    let userId = localStorage.getItem('userId');
    if (!userId) {
      userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('userId', userId);
    }

    // Store API key in backend
    try {
      const response = await fetch(`${config.backendUrl}/store_api_key/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          provider: newModel.provider,
          api_key: newModel.apiKey,
          model_name: newModel.name
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to store API key in backend');
      }

      const updatedModels = [...models, modelData];
      setModels(updatedModels);
      localStorage.setItem('aiModels', JSON.stringify(updatedModels));
      
      setNewModel({ provider: '', apiKey: '', name: '' });
      setShowAddForm(false);
      
      alert('AI model added successfully!');
    } catch (error) {
      console.error('Error storing API key:', error);
      alert('Failed to store API key securely. Please try again.');
    }
  };

  const handleDeleteModel = async (id) => {
    if (window.confirm('Are you sure you want to delete this model configuration?')) {
      const modelToDelete = models.find(model => model.id === id);
      const userId = localStorage.getItem('userId');
      
      // Delete from backend if we have user ID and model
      if (userId && modelToDelete) {
        try {
          const response = await fetch(`${config.backendUrl}/delete_api_key/`, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              user_id: userId,
              provider: modelToDelete.provider
            }),
          });

          if (!response.ok) {
            console.warn('Failed to delete API key from backend, but continuing with local deletion');
          }
        } catch (error) {
          console.error('Error deleting API key from backend:', error);
        }
      }
      
      const updatedModels = models.filter(model => model.id !== id);
      setModels(updatedModels);
      localStorage.setItem('aiModels', JSON.stringify(updatedModels));
    }
  };

  const toggleApiKeyVisibility = (id) => {
    setShowApiKeys(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const maskApiKey = (apiKey) => {
    if (apiKey.length <= 8) return '*'.repeat(apiKey.length);
    // Show first 4 and last 4 characters, with limited asterisks in between
    const maskedLength = Math.min(12, apiKey.length - 8); // Limit to 12 asterisks max
    return apiKey.substring(0, 4) + '*'.repeat(maskedLength) + apiKey.substring(apiKey.length - 4);
  };

  return (
    <div className="w-full max-w-none space-y-4 sm:space-y-6">
      <Card className="border-0 shadow-sm">
        <CardHeader className="pb-4 px-4 sm:px-6">
          <div className="flex flex-col sm:flex-row items-start justify-between gap-3">
            <div>
              <h2 className="text-xl sm:text-2xl font-bold text-gray-900">AI Models Management</h2>
              <p className="text-gray-600 mt-1 text-sm sm:text-base">
                Manage your AI model providers and API keys for the chatbot
              </p>
            </div>
            <Button
              onClick={() => setShowAddForm(true)}
              className="bg-gray-900 hover:bg-gray-800 text-white flex items-center gap-2 px-3 py-2 sm:px-4 sm:py-2 text-sm sm:text-base w-full sm:w-auto"
            >
              <Plus size={14} className="sm:w-4 sm:h-4" />
              Add Model
            </Button>
          </div>
        </CardHeader>
        <CardContent className="pt-0 px-4 sm:px-6">
          {models.length === 0 ? (
            <div className="text-center py-8 sm:py-12">
              <div className="w-12 h-12 sm:w-16 sm:h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                <Bot size={24} className="sm:w-8 sm:h-8 text-gray-400" />
              </div>
              <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2">No AI models configured</h3>
              <p className="text-gray-500 mb-4 text-sm sm:text-base">Add your first model to get started with the chatbot</p>
              <Button
                onClick={() => setShowAddForm(true)}
                className="bg-gray-900 hover:bg-gray-800 text-white text-sm sm:text-base"
              >
                <Plus size={14} className="sm:w-4 sm:h-4 mr-2" />
                Add Your First Model
              </Button>
            </div>
          ) : (
            <div className="space-y-3">
              {models.map((model) => (
                <Card key={model.id} className="border border-gray-200 hover:border-gray-300 transition-colors">
                  <CardContent className="p-3 sm:p-5">
                    <div className="flex flex-col sm:flex-row items-start justify-between gap-3">
                      <div className="flex-1 w-full">
                        {/* Header with name, provider, and primary badge */}
                        <div className="flex items-center gap-3 mb-3">
                          <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center">
                            <Bot size={16} className="sm:w-[18px] sm:h-[18px] text-white" />
                          </div>
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <h3 className="font-semibold text-gray-900 text-sm sm:text-base">{model.name}</h3>
                            </div>
                            <p className="text-xs sm:text-sm text-gray-500">
                              {providerOptions[model.provider]?.name || model.provider}
                            </p>
                          </div>
                        </div>

                        {/* API Key section */}
                        <div className="mb-3 p-2 sm:p-3 bg-gray-50 rounded-lg">
                          <div className="flex items-center gap-2">
                            <Label className="text-xs font-medium text-gray-600 uppercase tracking-wide">API Key</Label>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => toggleApiKeyVisibility(model.id)}
                              className="p-0 h-4 w-4 sm:h-5 sm:w-5 text-gray-400 hover:text-gray-600"
                            >
                              {showApiKeys[model.id] ? <EyeOff size={10} className="sm:w-3 sm:h-3" /> : <Eye size={10} className="sm:w-3 sm:h-3" />}
                            </Button>
                          </div>
                          <code className="text-xs sm:text-sm text-gray-800 font-mono break-all">
                            {showApiKeys[model.id] ? model.apiKey : maskApiKey(model.apiKey)}
                          </code>
                        </div>

                        {/* Available models */}
                        <div>
                          <Label className="text-xs font-medium text-gray-600 uppercase tracking-wide mb-2 block">
                            Available Models ({model.models.length})
                          </Label>
                          <div className="flex flex-wrap gap-1 sm:gap-1.5">
                            {model.models.map((modelName, index) => (
                              <span
                                key={`${model.id}-${modelName}-${index}`}
                                className="text-xs bg-blue-50 text-blue-700 px-2 py-1 sm:px-2.5 sm:py-1 rounded-md border border-blue-200 font-medium break-all"
                              >
                                {modelName}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>

                      {/* Action buttons */}
                      <div className="flex sm:flex-col gap-2 sm:ml-4 w-full sm:w-auto">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleDeleteModel(model.id)}
                          className="text-red-600 border-red-300 hover:bg-red-50 hover:border-red-400 flex-1 sm:flex-none text-xs sm:text-sm"
                        >
                          <Trash2 size={12} className="sm:w-[14px] sm:h-[14px]" />
                          <span className="sm:hidden ml-1">Delete</span>
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Add Model Form */}
      {showAddForm && (
        <Card>
          <CardHeader className="px-4 sm:px-6">
            <h3 className="text-base sm:text-lg font-semibold">Add New AI Model</h3>
          </CardHeader>
          <CardContent className="space-y-4 px-4 sm:px-6">
            <div>
              <Label htmlFor="provider" className="text-sm sm:text-base">Provider</Label>
              <select
                id="provider"
                value={newModel.provider}
                onChange={(e) => setNewModel(prev => ({ ...prev, provider: e.target.value }))}
                className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base"
              >
                <option value="">Select a provider</option>
                {Object.entries(providerOptions).map(([key, option]) => (
                  <option key={key} value={key}>
                    {option.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <Label htmlFor="modelName" className="text-sm sm:text-base">Configuration Name</Label>
              <Input
                id="modelName"
                value={newModel.name}
                onChange={(e) => setNewModel(prev => ({ ...prev, name: e.target.value }))}
                placeholder="e.g., My OpenAI Account"
                className="text-sm sm:text-base"
              />
            </div>

            <div>
              <Label htmlFor="apiKey" className="text-sm sm:text-base">API Key</Label>
              <Input
                id="apiKey"
                type="password"
                value={newModel.apiKey}
                onChange={(e) => setNewModel(prev => ({ ...prev, apiKey: e.target.value }))}
                placeholder={newModel.provider ? providerOptions[newModel.provider].placeholder : 'Enter your API key'}
                className="text-sm sm:text-base"
              />
            </div>

            {newModel.provider && (
              <div>
                <Label className="text-sm sm:text-base">Available Models</Label>
                <div className="flex flex-wrap gap-1 sm:gap-2 mt-2">
                  {providerOptions[newModel.provider].models.map((modelName, index) => (
                    <span
                      key={`${newModel.provider}-${modelName}-${index}`}
                      className="text-xs sm:text-sm bg-gray-100 text-gray-700 px-2 py-1 sm:px-3 sm:py-1 rounded-full break-all"
                    >
                      {modelName}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div className="flex flex-col sm:flex-row gap-2">
              <Button
                onClick={handleAddModel}
                className="bg-[#1e2b3b] text-white text-sm sm:text-base"
              >
                Add Model
              </Button>
              <Button
                variant="outline"
                onClick={() => {
                  setShowAddForm(false);
                  setNewModel({ provider: '', apiKey: '', name: '' });
                }}
                className="text-sm sm:text-base"
              >
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
