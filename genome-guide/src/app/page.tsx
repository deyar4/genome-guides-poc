"use client";
import { useState } from 'react';
import Header from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar';
import DashboardView from '@/components/views/DashboardView';
import GenomeBrowserView from '@/components/views/GenomeBrowserView';
import ToolsView from '@/components/views/ToolsView';

export default function GenomeDashboard() {
  const [activeTab, setActiveTab] = useState("dashboard");

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardView />;
      case 'browser':
        return <GenomeBrowserView />;
      case 'tools':
        return <ToolsView />;
      default:
        return (
          <div className="p-6">
            <h1 className="text-2xl font-bold">{`${activeTab.charAt(0).toUpperCase() + activeTab.slice(1)}`}</h1>
          </div>
        );
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background text-foreground">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
        <main className="flex-1 overflow-y-auto">
          {renderContent()}
        </main>
      </div>
    </div>
  );
}