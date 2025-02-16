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
} from "lucide-react"; // Icons
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

export default function TrainPage() {
  const [activeTab, setActiveTab] = useState("upload");
  const backendUrl = process.env.BACKEND_URL
  return (
    <div className="p-6 h-screen bg-gray-100">
      <div className="flex bg-gray-100 max-w-5xl mx-auto">
        {/* Sidebar */}
        <aside className="w-80 p-5">
          <h2 className="text-xl font-semibold mb-6">Train</h2>
          <nav className="space-y-2">
            <NavItem
              icon={<Upload size={18} />}
              label="Website Link and File Upload"
              active={activeTab === "upload"}
              onClick={() => setActiveTab("upload")}
            />
            <NavItem
              icon={<Database size={18} />}
              label="SQL Database Connection"
              active={activeTab === "sql"}
              onClick={() => setActiveTab("sql")}
            />
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1">
          {activeTab === "upload" ? <UploadFiles /> : <SQLConnection />}
        </main>
      </div>
    </div>
  );
}

// Sidebar Item Component
const NavItem = ({ icon, label, active, onClick }) => {
  return (
    <div
      className={`flex items-center p-3 cursor-pointer rounded-md transition ${
        active ? "bg-gray-200 font-medium" : "hover:bg-gray-100"
      }`}
      onClick={onClick}
    >
      {icon}
      <span className="ml-3">{label}</span>
    </div>
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

    setLoading(true); // Start loading

    try {
      const response = await fetch(
        `https://6983-111-68-97-206.ngrok-free.app/create_bot/`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) throw new Error("Failed to send data");

      const res = await response.json();
      setScriptUrl(`https://localhost:3000/api/chatbot/${res.bot_id}`);
      localStorage.setItem("bot_id", res.bot_id);
    } catch (error) {
      console.error("Error sending data:", error);
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      {/* Main Card */}
      <Card>
        <CardHeader className="text-lg font-semibold">
          Set Up Script Configuration
        </CardHeader>
        <CardContent className="space-y-4">
          <Card>
            <CardHeader className="text-lg font-semibold">
              Website Link
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="website">Website</Label>
                <div className="flex items-center space-x-2">
                  <Input
                    id="website"
                    value={website}
                    onChange={(e) => {
                      setWebsite(e.target.value);
                      setErrors((prev) => ({ ...prev, website: "" }));
                    }}
                  />
                </div>
                {errors.website && (
                  <p className="text-red-500 text-sm mt-1">{errors.website}</p>
                )}
                <p className="text-xs text-gray-500 mt-1">
                  Your bot will only work on websites with this domain name.
                </p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-lg font-semibold">
              Upload Files
              <p className="text-gray-500 text-sm font-normal pt-1 ps-0.5">
                Upload your files to the knowledge base.
              </p>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Drag & Drop Area */}
              <label className="flex flex-col items-center justify-center border-2 border-dashed border-gray-300 p-10 rounded-lg cursor-pointer hover:bg-gray-50">
                <UploadCloud size={40} className="text-gray-400" />
                <p className="text-gray-700 font-medium">
                  Drag & drop files here, or click to select files
                </p>
                <p className="text-sm text-gray-500">
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
                <p className="text-red-500 text-sm mt-1">{errors.files}</p>
              )}

              {/* Uploaded Files List */}
              {files.length > 0 && (
                <div>
                  <p className="font-semibold">
                    Uploaded Files: {files.length}
                  </p>
                  <div className="mt-2 space-y-2">
                    {files.map((file, index) => (
                      <div
                        key={index}
                        className="flex items-center justify-between p-3 bg-gray-100 rounded-lg"
                      >
                        <span className="text-sm font-medium">{file.name}</span>
                        <div className="flex items-center space-x-2">
                          <button
                            onClick={() => handleDelete(index)}
                            className="text-red-600 hover:text-red-800"
                          >
                            <Trash2 size={16} />
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
            className="w-full bg-[#1e2b3b] text-white flex items-center justify-center"
            onClick={handleSave}
            disabled={loading} // Disable while loading
          >
            {loading ? (
              <>
                <Loader className="animate-spin w-5 h-5 mr-2" /> Processing...
              </>
            ) : (
              "Save"
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Embedded Script */}
      <Card>
        <CardHeader className="text-lg font-semibold">
          Embedded Script
        </CardHeader>
        <CardContent>
          <div className="relative">
            <Textarea
              className="font-mono text-sm pr-10 h-24 bg-[#1e2b3b] text-white"
              readOnly
              value={`<script defer src="${scriptUrl}"></script>`}
            />
            <button
              className="absolute top-2 right-2 p-2 bg-gray-200 rounded-md hover:bg-gray-300"
              onClick={copyToClipboard}
            >
              {copied ? (
                <Check className="w-4 h-4 text-[#1e2b3b]" />
              ) : (
                <Clipboard className="w-4 h-4" />
              )}
            </button>
          </div>
        </CardContent>
      </Card>

      {/* Copy Popup */}
      {showPopup && (
        <div className="fixed bottom-4 right-4 bg-gray-800 text-white px-4 py-2 rounded-md shadow-md">
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
    <Card>
      <CardHeader className="text-lg font-semibold">
        SQL Database Connection
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Label htmlFor="host">Host</Label>
          <Input
            id="host"
            value={hostName}
            onChange={(e) => setHostName(e.target.value)}
          />
        </div>
        <div>
          <Label htmlFor="dbName">Database Name</Label>
          <Input
            id="dbName"
            value={dbName}
            onChange={(e) => setDbName(e.target.value)}
          />
        </div>
        <div>
          <Label htmlFor="username">Username</Label>
          <Input
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <Button className="w-full bg-[#1e2b3b] text-white">Save</Button>
      </CardContent>
    </Card>
  );
};
