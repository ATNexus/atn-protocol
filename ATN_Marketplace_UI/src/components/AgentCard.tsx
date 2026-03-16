import React from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Zap, Clock, TrendingUp, Shield } from 'lucide-react';

interface Agent {
  id: string;
  name: string;
  did: string;
  avatar: string;
  tier: 'bronze' | 'silver' | 'gold' | 'platinum';
  sbtScore: number;
  successRate: number;
  avgResponseTime: number;
  totalEarnings: number;
  status: 'online' | 'busy' | 'offline';
  category: string;
  taskTypes: string[];
  baseFee: number;
}

const getTierColor = (tier: string) => {
  switch (tier) {
    case 'bronze':
      return 'text-amber-600 bg-amber-950/50 border-amber-700';
    case 'silver':
      return 'text-slate-300 bg-slate-800/50 border-slate-600';
    case 'gold':
      return 'text-yellow-400 bg-yellow-950/50 border-yellow-600';
    case 'platinum':
      return 'text-cyan-400 bg-cyan-950/50 border-cyan-600';
    default:
      return 'text-gray-400 bg-gray-800/50 border-gray-600';
  }
};

const getTierIcon = (tier: string) => {
  switch (tier) {
    case 'bronze':
      return '🥉';
    case 'silver':
      return '🥈';
    case 'gold':
      return '🥇';
    case 'platinum':
      return '💎';
    default:
      return '⚪';
  }
};

interface AgentCardProps {
  agent: Agent;
  onHire: (agent: Agent) => void;
}

export function AgentCard({ agent, onHire }: AgentCardProps) {
  const tierColorClass = getTierColor(agent.tier);
  
  return (
    <Card className="group relative overflow-hidden bg-slate-900/80 border-slate-800 hover:border-cyan-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-cyan-500/10">
      {/* 状态指示器 */}
      <div className={`absolute top-3 right-3 w-2 h-2 rounded-full animate-pulse ${
        agent.status === 'online' ? 'bg-emerald-500' :
        agent.status === 'busy' ? 'bg-amber-500' : 'bg-slate-500'
      }`} />
      
      <div className="p-5">
        {/* 头部：头像和基本信息 */}
        <div className="flex items-start gap-4">
          <div className="relative">
            <img
              src={agent.avatar}
              alt={agent.name}
              className="w-16 h-16 rounded-lg bg-slate-800"
            />
            <div className={`absolute -bottom-1 -right-1 w-6 h-6 rounded-full flex items-center justify-center text-xs border-2 border-slate-900 ${tierColorClass}`}>
              {getTierIcon(agent.tier)}
            </div>
          </div>
          
          <div className="flex-1 min-w-0">
            <h3 className="font-bold text-slate-100 truncate group-hover:text-cyan-400 transition-colors">
              {agent.name}
            </h3>
            <p className="text-xs text-slate-500 font-mono">
              {agent.did.slice(0, 20)}...
            </p>
            <div className="flex items-center gap-2 mt-1">
              <Badge variant="outline" className={`text-xs ${tierColorClass}`}>
                {agent.tier.toUpperCase()}
              </Badge>
              <span className="text-xs text-slate-400">{agent.category}</span>
            </div>
          </div>
        </div>
        
        {/* SBT 分数 */}
        <div className="mt-4 flex items-center gap-3">
          <div className="flex-1">
            <div className="flex items-center justify-between text-xs mb-1">
              <span className="text-slate-400">SBT Score</span>
              <span className={`font-mono font-bold ${
                agent.sbtScore >= 2000 ? 'text-cyan-400' :
                agent.sbtScore >= 500 ? 'text-yellow-400' :
                agent.sbtScore >= 100 ? 'text-slate-300' : 'text-amber-600'
              }`}>
                {agent.sbtScore.toLocaleString()}
              </span>
            </div>
            <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
              <div 
                className={`h-full rounded-full transition-all duration-500 ${
                  agent.tier === 'platinum' ? 'bg-cyan-500' :
                  agent.tier === 'gold' ? 'bg-yellow-500' :
                  agent.tier === 'silver' ? 'bg-slate-400' : 'bg-amber-600'
                }`}
                style={{ width: `${Math.min((agent.sbtScore / 3000) * 100, 100)}%` }}
              />
            </div>
          </div>
        </div>
        
        {/* 核心指标 */}
        <div className="mt-4 grid grid-cols-3 gap-2">
          <div className="bg-slate-800/50 rounded-lg p-2 text-center">
            <div className="flex items-center justify-center gap-1 text-emerald-400 mb-1">
              <Shield className="w-3 h-3" />
              <span className="text-xs font-bold">{agent.successRate}%</span>
            </div>
            <span className="text-[10px] text-slate-500">Success</span>
          </div>
          
          <div className="bg-slate-800/50 rounded-lg p-2 text-center">
            <div className="flex items-center justify-center gap-1 text-cyan-400 mb-1">
              <Clock className="w-3 h-3" />
              <span className="text-xs font-bold">{agent.avgResponseTime}s</span>
            </div>
            <span className="text-[10px] text-slate-500">Response</span>
          </div>
          
          <div className="bg-slate-800/50 rounded-lg p-2 text-center">
            <div className="flex items-center justify-center gap-1 text-amber-400 mb-1">
              <TrendingUp className="w-3 h-3" />
              <span className="text-xs font-bold">{agent.totalEarnings.toFixed(1)}</span>
            </div>
            <span className="text-[10px] text-slate-500">SOL Earned</span>
          </div>
        </div>
        
        {/* 任务类型 */}
        <div className="mt-3 flex flex-wrap gap-1">
          {agent.taskTypes.slice(0, 3).map((task) => (
            <span key={task} className="text-[10px] px-2 py-0.5 bg-slate-800 text-slate-400 rounded">
              {task.replace('_', ' ')}
            </span>
          ))}
        </div>
        
        {/* 底部：价格和操作 */}
        <div className="mt-4 flex items-center justify-between pt-3 border-t border-slate-800">
          <div>
            <span className="text-xs text-slate-500">Base Fee</span>
            <div className="flex items-center gap-1 text-cyan-400">
              <Zap className="w-3 h-3" />
              <span className="font-bold">{agent.baseFee} SOL</span>
            </div>
          </div>
          
          <Button 
            size="sm"
            onClick={() => onHire(agent)}
            disabled={agent.status === 'offline'}
            className={`${
              agent.status === 'offline' 
                ? 'bg-slate-700 text-slate-500' 
                : 'bg-cyan-600 hover:bg-cyan-500 text-white'
            }`}
          >
            {agent.status === 'busy' ? 'Queue' : 'Hire Now'}
          </Button>
        </div>
      </div>
    </Card>
  );
}
