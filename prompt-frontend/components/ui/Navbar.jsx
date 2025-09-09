"use client"

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Menu, Github } from "lucide-react";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import Image from "next/image";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="flex items-center justify-between px-6 py-4 shadow-md bg-white">
      {/* Left - Logo */}
      <Link href="/">
        <Image src="/logo.svg" alt="Logo" width={50} height={20} />
      </Link>

      {/* Center - Navigation Links (Hidden on Small Screens) */}
      <div className="hidden md:flex gap-6 text-lg font-medium">
        <Link href="/train" className="hover:text-blue-600">
          Train
        </Link>
        <Link href="/playground" className="hover:text-blue-600">
          Playground
        </Link>
      </div>

      {/* Right - GitHub Link */}
      <div className="hidden md:flex items-center">
        <Button variant="ghost" asChild>
          <a 
            href="https://github.com/visha1Sagar/Prompt-No-Code-Website-Assistant-Builder" 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center gap-2 hover:text-blue-600"
          >
            <Github className="w-5 h-5" />
            <span className="hidden lg:inline">GitHub</span>
          </a>
        </Button>
      </div>

      {/* Mobile Menu */}
      <Sheet open={isOpen} onOpenChange={setIsOpen}>
        <SheetTrigger asChild>
          <Button variant="ghost" className="md:hidden">
            <Menu className="w-6 h-6" />
          </Button>
        </SheetTrigger>
        <SheetContent side="left">
          <nav className="flex flex-col gap-4 mt-6">
            <Link
              href="/train"
              className="text-lg"
              onClick={() => setIsOpen(false)}
            >
              Train
            </Link>
            <Link
              href="/playground"
              className="text-lg"
              onClick={() => setIsOpen(false)}
            >
              Playground
            </Link>
            <a
              href="https://github.com/visha1Sagar/Prompt-No-Code-Website-Assistant-Builder"
              target="_blank"
              rel="noopener noreferrer"
              className="text-lg flex items-center gap-2 hover:text-blue-600"
              onClick={() => setIsOpen(false)}
            >
              <Github className="w-5 h-5" />
              GitHub
            </a>
          </nav>
        </SheetContent>
      </Sheet>
    </nav>
  );
}
