// src/components/header.tsx
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";
import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";
import { UserNav } from "@/components/user-nav";

export function Header() {
  return (
    <header className="sticky top-0 z-10 flex h-16 items-center gap-4 border-b bg-background px-4 md:px-6">
      <div className="hidden md:flex">
        <nav className="flex items-center gap-6 text-sm">
          <Link
            href="#"
            className="transition-colors hover:text-foreground/80 text-foreground/90"
          >
            Overview
          </Link>
          <Link
            href="#"
            className="transition-colors hover:text-foreground/80 text-foreground/60"
          >
            Browser
          </Link>
          <Link
            href="#"
            className="transition-colors hover:text-foreground/80 text-foreground/60"
          >
            Tools
          </Link>
          <Link
            href="#"
            className="transition-colors hover:text-foreground/80 text-foreground/60"
          >
            Documentation
          </Link>
        </nav>
      </div>
      
      <div className="flex w-full items-center gap-4 md:ml-auto md:gap-2 lg:gap-4">
        <form className="ml-auto flex-1 sm:flex-initial">
          <div className="relative">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Search genes, regions, variants..."
              className="pl-8 sm:w-[300px] md:w-[400px] lg:w-[500px]"
            />
          </div>
        </form>
        <ThemeToggle />
        <UserNav />
      </div>
    </header>
  );
}