import React, { useEffect, useState, useRef } from 'react';
import { Activity, ArrowRightLeft, CheckCircle2, AlertCircle } from 'lucide-react';

interface Transaction {
  id: string;
  agentId: string;
  agentName: string;
  agentAvatar: string;
  buyer: string;
  taskType: string;
  amount: number;
  result: string;
  timestamp: number;
  status: 'completed' | 'pending' | 'disputed';
}

// 模拟交易数据生成
const generateRandomTransaction = (): Transaction => {
  const agents = [
    { name: 'FlightFinder Pro', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=flight' },
    { name: 'CodeAuditor AI', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=code' },
    { name: 'DataScout', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=data' },
    { name: 'DeFi Guardian', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=defi' },
  ];
  
  const taskTypes = [
    'Found $480 flight NYC→LAX',
    'Audited 500 lines of Solidity',
    'Optimized DeFi strategy +12% APY',
    'Generated 2000-word article',
    'Analyzed 10K user records',
  ];
  
  const agent = agents[Math.floor(Math.random() * agents.length)];
  
  return {
    id: `tx_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    agentId: `agent_${Math.floor(Math.random() * 100)}`,
    agentName: agent.name,
    agentAvatar: agent.avatar,
    buyer: `0x${Math.random().toString(36).substr(2, 6)}...${Math.random().toString(36).substr(2, 4)}`,
    taskType: taskTypes[Math.floor(Math.random() * taskTypes.length)],
    amount: Number((Math.random() * 0.5 + 0.01).toFixed(3)),
    result: 'Success',
    timestamp: Date.now(),
    status: Math.random() > 0.9 ? 'disputed' : 'completed',
  };
};

const formatTimeAgo = (timestamp: number): string => {
  const seconds = Math.floor((Date.now() - timestamp) / 1000);
  if (seconds < 60) return `${seconds}s ago`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  return `${Math.floor(seconds / 3600)}h ago`;
};

export function PulseWall() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);
  
  // 初始化一些交易
  useEffect(() => {
    const initial = Array.from({ length: 5 }, generateRandomTransaction);
    setTransactions(initial);
  }, []);
  
  // 每3秒生成新交易
  useEffect(() => {
    const interval = setInterval(() => {
      const newTx = generateRandomTransaction();
      setTransactions(prev => [newTx, ...prev].slice(0, 20));
    }, 3000);
    
    return () => clearInterval(interval);
  }, []);
  
  const totalVolume = transactions.reduce((sum, tx) => sum + tx.amount, 0);
  
  return (
    <div className="bg-slate-900/50 border border-slate-800 rounded-xl overflow-hidden">
      {/* 头部 */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800 bg-slate-900/80">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-cyan-400 animate-pulse" />
          <h3 className="font-bold text-slate-100">The Pulse</h3>
          <span className="text-xs text-slate-500">Live Transactions</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
          <span className="text-xs text-emerald-400">Real-time</span>
        </div>
      </div>
      
      {/* 交易列表 */}
      <div 
        ref={containerRef}
        className="h-80 overflow-y-auto scrollbar-hide"
      >
        <div className="p-2 space-y-1">
          {transactions.map((tx, index) => (
            <div
              key={tx.id}
              className={`flex items-center gap-3 p-3 rounded-lg transition-all duration-500 ${
                index === 0 ? 'bg-cyan-950/30 border border-cyan-500/20' : 'bg-slate-800/30 hover:bg-slate-800/50'
              }`}
            >
              {/* Agent 头像 */}
              <img
                src={tx.agentAvatar}
                alt=""
                className="w-8 h-8 rounded bg-slate-700"
              />
              
              {/* 交易信息 */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-slate-300 font-medium truncate">
                    {tx.agentName}
                  </span>
                  <ArrowRightLeft className="w-3 h-3 text-slate-600" />
                  <span className="text-slate-500 text-xs">
                    {tx.buyer}
                  </span>
                </div>
                <p className="text-xs text-cyan-400/80 truncate mt-0.5">
                  {tx.taskType}
                </p>
              </div>
              
              {/* 金额和状态 */}
              <div className="text-right">
                <div className={`flex items-center gap-1 text-sm font-mono ${
                  tx.status === 'disputed' ? 'text-red-400' : 'text-emerald-400'
                }`}>
                  {tx.status === 'disputed' ? (
                    <AlertCircle className="w-3 h-3" />
                  ) : (
                    <CheckCircle2 className="w-3 h-3" />
                  )}
                  {tx.status === 'disputed' ? 'DISPUTED' : `+${tx.amount} SOL`}
                </div>
                <span className="text-[10px] text-slate-500">
                  {formatTimeAgo(tx.timestamp)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {/* 底部统计 */}
      <div className="px-4 py-2 border-t border-slate-800 bg-slate-900/80 flex items-center justify-between text-xs">
        <span className="text-slate-500">
          {transactions.length} recent transactions
        </span>
        <span className="text-cyan-400">
          {totalVolume.toFixed(3)} SOL volume
        </span>
      </div>
    </div>
  );
}
