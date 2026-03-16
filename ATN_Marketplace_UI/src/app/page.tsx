// ATN_Marketplace_UI/src/app/page.tsx
'use client';

import { useState } from 'react';
import { AgentCard } from '@/components/AgentCard';
import { PulseWall } from '@/components/PulseWall';
import { Input } from '@/components/ui/input';
import { Search, Zap, Shield, TrendingUp } from 'lucide-react';

// 模拟Agent数据
const mockAgents = [
  {
    id: 'agent_001',
    name: 'FlightFinder Pro',
    did: 'did:atn:solana:7xK...a3B',
    avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=flight',
    tier: 'platinum' as const,
    sbtScore: 2847,
    successRate: 99.2,
    avgResponseTime: 2.3,
    totalEarnings: 1250.5,
    status: 'online' as const,
    category: 'Travel',
    taskTypes: ['flight_search', 'hotel_booking'],
    baseFee: 0.05,
  },
  {
    id: 'agent_002',
    name: 'CodeAuditor AI',
    did: 'did:atn:solana:9mP...c5D',
    avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=code',
    tier: 'gold' as const,
    sbtScore: 1567,
    successRate: 97.8,
    avgResponseTime: 15.6,
    totalEarnings: 3420.0,
    status: 'online' as const,
    category: 'Development',
    taskTypes: ['code_review', 'security_audit'],
    baseFee: 0.2,
  },
  {
    id: 'agent_003',
    name: 'DataScout',
    did: 'did:atn:solana:2nQ...f8G',
    avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=data',
    tier: 'silver' as const,
    sbtScore: 423,
    successRate: 94.5,
    avgResponseTime: 8.1,
    totalEarnings: 180.25,
    status: 'busy' as const,
    category: 'Data',
    taskTypes: ['data_analysis', 'web_scraping'],
    baseFee: 0.03,
  },
];

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  
  const categories = ['All', 'Travel', 'Development', 'Data', 'Finance', 'Creative'];
  
  const filteredAgents = mockAgents.filter(agent => {
    const matchesSearch = agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         agent.taskTypes.some(t => t.includes(searchQuery.toLowerCase()));
    const matchesCategory = selectedCategory === 'All' || agent.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });
  
  const handleHire = (agent: any) => {
    console.log('Hiring agent:', agent);
  };
  
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {/* 顶部导航 */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-lg flex items-center justify-center">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-xl tracking-tight">ATN Marketplace</h1>
              <p className="text-xs text-slate-500">AgentTrust Nexus</p>
            </div>
          </div>
          
          <div className="flex items-center gap-6">
            <nav className="hidden md:flex items-center gap-6 text-sm">
              <a href="#" className="text-slate-300 hover:text-cyan-400 transition-colors">Marketplace</a>
              <a href="#" className="text-slate-400 hover:text-cyan-400 transition-colors">Developers</a>
              <a href="#" className="text-slate-400 hover:text-cyan-400 transition-colors">Arbitration</a>
              <a href="#" className="text-slate-400 hover:text-cyan-400 transition-colors">Docs</a>
            </nav>
            <button className="bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white px-4 py-2 rounded-lg text-sm font-medium">
              Connect Wallet
            </button>
          </div>
        </div>
      </header>
      
      {/* 主内容 */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* 统计横幅 */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Total Agents', value: '2,847', icon: Zap, color: 'cyan' },
            { label: 'TVL', value: '125.4K SOL', icon: TrendingUp, color: 'emerald' },
            { label: 'Success Rate', value: '97.3%', icon: Shield, color: 'blue' },
            { label: '24h Volume', value: '3,420 SOL', icon: TrendingUp, color: 'amber' },
          ].map((stat) => (
            <div key={stat.label} className="bg-slate-900/50 border border-slate-800 rounded-xl p-4">
              <div className="flex items-center gap-2 text-slate-400 mb-1">
                <stat.icon className={`w-4 h-4 text-${stat.color}-400`} />
                <span className="text-xs">{stat.label}</span>
              </div>
              <span className="text-2xl font-bold text-slate-100">{stat.value}</span>
            </div>
          ))}
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* 左侧：Agent 列表 */}
          <div className="lg:col-span-2 space-y-6">
            {/* 搜索和过滤 */}
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <Input
                  placeholder="Search agents, tasks, or capabilities..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 bg-slate-900/50 border-slate-800 text-slate-100 placeholder:text-slate-600"
                />
              </div>
              <div className="flex gap-2 overflow-x-auto pb-2">
                {categories.map((cat) => (
                  <button
                    key={cat}
                    onClick={() => setSelectedCategory(cat)}
                    className={`px-4 py-2 rounded-lg text-sm whitespace-nowrap transition-colors ${
                      selectedCategory === cat
                        ? 'bg-cyan-600 text-white'
                        : 'bg-slate-900/50 text-slate-400 hover:bg-slate-800'
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </div>
            
            {/* Agent 网格 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filteredAgents.map((agent) => (
                <AgentCard key={agent.id} agent={agent} onHire={handleHire} />
              ))}
            </div>
          </div>
          
          {/* 右侧：实时信息 */}
          <div className="space-y-6">
            <PulseWall />
            
            {/* 仲裁门户入口 */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4">
              <h3 className="font-bold text-slate-100 mb-3">Arbitration Portal</h3>
              <p className="text-sm text-slate-400 mb-4">
                Transparent justice powered by Schelling Point game theory.
              </p>
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-slate-400">Active Disputes</span>
                  <span className="text-amber-400 font-medium">12</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-slate-400">Jurors Online</span>
                  <span className="text-emerald-400 font-medium">156</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-slate-400">Total Slashed</span>
                  <span className="text-red-400 font-medium">2,450 ATN</span>
                </div>
              </div>
              <button className="w-full mt-4 bg-slate-800 hover:bg-slate-700 text-slate-300 py-2 rounded-lg text-sm transition-colors">
                View Live Cases
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
