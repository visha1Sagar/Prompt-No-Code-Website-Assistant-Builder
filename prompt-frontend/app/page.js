import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight, Bot, FileText, MessageSquare, Upload, Zap } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Hero Section */}
      <div className="container mx-auto px-6 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Build AI Assistants Without Code
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Create intelligent chatbots by simply uploading your documents. 
            Train AI assistants that understand your content and engage with your users naturally.
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/train">
              <Button size="lg" className="text-lg px-8 py-3">
                Get Started <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </Link>
            
          </div>
        </div>

        {/* How It Works Section */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            How It Works
          </h2>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {/* Step 1 */}
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto mb-4 p-3 bg-blue-100 rounded-full w-fit">
                  <Upload className="w-8 h-8 text-blue-600" />
                </div>
                <CardTitle className="text-xl">1. Upload Documents</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  Upload your documents, PDFs, or text files. Our system will process and understand your content automatically.
                </CardDescription>
              </CardContent>
            </Card>

            {/* Step 2 */}
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto mb-4 p-3 bg-green-100 rounded-full w-fit">
                  <Bot className="w-8 h-8 text-green-600" />
                </div>
                <CardTitle className="text-xl">2. Train Your Bot</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  Give your bot a name and description. The AI will learn from your documents and create a knowledge base.
                </CardDescription>
              </CardContent>
            </Card>

            {/* Step 3 */}
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto mb-4 p-3 bg-purple-100 rounded-full w-fit">
                  <MessageSquare className="w-8 h-8 text-purple-600" />
                </div>
                <CardTitle className="text-xl">3. Start Chatting</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  Your AI assistant is ready! Users can ask questions and get intelligent responses based on your content.
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Features Section */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Powerful Features
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <FileText className="w-8 h-8 text-blue-600 mb-2" />
                <CardTitle>Smart Document Processing</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Supports multiple file formats including PDF, DOCX, and TXT. Advanced text extraction and preprocessing.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <Zap className="w-8 h-8 text-yellow-600 mb-2" />
                <CardTitle>Instant Deployment</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  No coding required. Your AI assistant is ready to use immediately after training on your documents.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <Bot className="w-8 h-8 text-green-600 mb-2" />
                <CardTitle>Intelligent Responses</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Powered by advanced AI models that understand context and provide accurate, relevant answers.
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center bg-white rounded-lg shadow-lg p-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Ready to Build Your AI Assistant?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Join thousands of users who have created intelligent chatbots in minutes, not months.
          </p>
          <Link href="/train">
            <Button size="lg" className="text-lg px-8 py-3">
              Start Building Now <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
