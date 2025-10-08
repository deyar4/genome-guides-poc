"use client";
import { useState } from 'react';
import Header from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar';
import DashboardView from '@/components/views/DashboardView';
import GenomeBrowserView from '@/components/views/GenomeBrowserView';
import ToolsView from '@/components/views/ToolsView';
import DnaView from '@/components/views/DnaView';

export default function GenomeDashboard() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [selectedGene, setSelectedGene] = useState<string | null>("BRCA1");

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardView selectedGeneSymbol={selectedGene} />;
      case 'browser':
        return <DnaView />;
      case 'tools':
        return <ToolsView />;
      default:
        return <div className="p-6">...</div>;
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background text-foreground">
      {/* 3. Pass the function to update the gene down to the Header */}
      <Header onGeneSelect={setSelectedGene} />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
        <main className="flex-1 overflow-y-auto">
          {renderContent()}
        </main>
      </div>
    </div>
  );
}