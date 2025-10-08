"use client";
import { Button } from "@/components/ui/button";
import { Dna, Activity, Book, Settings, Home, Database } from 'lucide-react';

// Props: the current active tab, and the function to SET the active tab
type SidebarProps = {
  activeTab: string;
  setActiveTab: (tab: string) => void;
};

const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: Home },
  { id: 'browser', label: 'DNA & Chromosomes', icon: Dna },
  { id: 'tools', label: 'Analysis Tools', icon: Activity },
  { id: 'data', label: 'Data Sources', icon: Database },
  { id: 'docs', label: 'Documentation', icon: Book },
  { id: 'settings', label: 'Settings', icon: Settings },
];

export default function Sidebar({ activeTab, setActiveTab }: SidebarProps) {
  return (
    <aside className="w-64 bg-card flex flex-col justify-between">
      <nav className="p-4 space-y-1">
        {navItems.map((item) => (
          <Button
            key={item.id}
            variant={activeTab === item.id ? "secondary" : "ghost"}
            className="w-full justify-start gap-3"
            onClick={() => setActiveTab(item.id)}
          >
            <item.icon className="h-5 w-5" />
            <span>{item.label}</span>
          </Button>
        ))}
      </nav>
      <div className="p-4 border-t">
        <p className="text-xs text-muted-foreground mb-2">Need help?</p>
        <Button variant="outline" className="w-full">
          Contact Support
        </Button>
      </div>
    </aside>
  );
}