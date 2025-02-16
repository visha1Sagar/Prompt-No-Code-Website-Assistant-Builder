"use client";

import { useState } from "react";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Clipboard, Check } from "lucide-react";

export default function ScriptSetup() {
  const [website, setWebsite] = useState("");
  const [copied, setCopied] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const scriptUrl = "";

  const copyToClipboard = () => {
    navigator.clipboard.writeText(`<script defer src="${scriptUrl}"></script>`);
    setCopied(true);
    setShowPopup(true);
    setTimeout(() => setCopied(false), 2000);
    setTimeout(() => setShowPopup(false), 2000);
  };

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      {/* Setup Script Configuration */}
      <Card>
        <CardHeader className="text-lg font-semibold">
          Set Up Script Configuration
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label htmlFor="website">Website</Label>
            <div className="flex items-center space-x-2">
              <span className="text-gray-500">https://</span>
              <Input
                id="website"
                value={website}
                onChange={(e) => setWebsite(e.target.value)}
              />
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Your bot will only work on websites with this domain name.
            </p>
          </div>
          <Button className="w-full bg-[#1e2b3b] text-white">Save</Button>
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
}
