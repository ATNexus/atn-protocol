import React, { useState, useEffect } from 'react';
import { Search, Filter, Star, TrendingUp, Shield, Zap } from 'lucide-react';

// 搜索和过滤组件
export function SearchAndFilter({ onSearch, onFilter }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [priceRange, setPriceRange] = useState([0, 1]);
  
  const categories = ['All', 'Travel', 'Development', 'Data', 'Finance', 'Creative'];
  
  useEffect(() => {
    onSearch(searchQuery);
  }, [searchQuery]);
  
  useEffect(() => {
    onFilter({ category: selectedCategory, priceRange });
  }, [selectedCategory, priceRange]);
  
  return (
    <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4 mb-6">
      <div className="flex flex-col md:flex-row gap-4">
        {/* 搜索框 */}
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
          <input
            type="text"
            placeholder="Search agents by name, task, or capability..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-cyan-500"
          />
        </div>
        
        {/* 分类过滤 */}
        <div className="flex gap-2 overflow-x-auto">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-4 py-2 rounded-lg text-sm whitespace-nowrap transition-all ${
                selectedCategory === cat
                  ? 'bg-cyan-600 text-white'
                  : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>
      
      {/* 高级过滤 */}
      <div className="mt-4 flex flex-wrap gap-4 text-sm">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-slate-500" />
          <span className="text-slate-400">Price Range:</span>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={priceRange[1]}
            onChange={(e) => setPriceRange([0, parseFloat(e.target.value)])}
            className="w-32"
          />
          <span className="text-cyan-400">{priceRange[1]} SOL</span>
        </div>
        
        <div className="flex items-center gap-2">
          <Star className="w-4 h-4 text-slate-500" />
          <span className="text-slate-400">Min Rating:</span>
          <select className="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-300">
            <option>Any</option>
            <option>4+ Stars</option>
            <option>4.5+ Stars</option>
          </select>
        </div>
        
        <div className="flex items-center gap-2">
          <Shield className="w-4 h-4 text-slate-500" />
          <span className="text-slate-400">Verification:</span>
          <select className="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-300">
            <option>Any</option>
            <option>Verified Only</option>
            <option>TEE Attested</option>
          </select>
        </div>
      </div>
    </div>
  );
}

// 统计卡片
export function StatsOverview() {
  const stats = [
    { label: 'Total Agents', value: '2,847', change: '+12%', icon: Zap },
    { label: 'TVL', value: '125.4K SOL', change: '+8.5%', icon: TrendingUp },
    { label: 'Success Rate', value: '97.3%', change: '+0.3%', icon: Shield },
    { label: '24h Volume', value: '3,420 SOL', change: '+15%', icon: TrendingUp },
  ];
  
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      {stats.map((stat, index) => (
        <div key={index} className="bg-slate-900/50 border border-slate-800 rounded-xl p-4 hover:border-cyan-500/50 transition-colors">
          <div className="flex items-center justify-between mb-2">
            <stat.icon className="w-5 h-5 text-cyan-400" />
            <span className="text-xs text-emerald-400">{stat.change}</span>
          </div>
          <div className="text-2xl font-bold text-slate-100">{stat.value}</div>
          <div className="text-xs text-slate-500">{stat.label}</div>
        </div>
      ))}
    </div>
  );
}
