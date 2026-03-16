import React, { useState, useEffect } from 'react';
import { Scale, Gavel, Users, Clock, AlertCircle, CheckCircle } from 'lucide-react';

// 仲裁面板组件
export function ArbitrationPanel() {
  const [activeCases, setActiveCases] = useState([
    {
      id: 'DISPUTE_001',
      taskId: 'TASK_789',
      agentName: 'DataScout',
      reason: 'Delivery timeout - promised in 5min, took 45min',
      status: 'voting',
      jurors: [
        { id: 'juror_001', status: 'voted', vote: 'fraud' },
        { id: 'juror_002', status: 'voted', vote: 'fraud' },
        { id: 'juror_003', status: 'pending', vote: null },
      ],
      timeRemaining: '12 min',
      escrowAmount: 0.05,
    },
    {
      id: 'DISPUTE_002',
      taskId: 'TASK_456',
      agentName: 'ContentForge',
      reason: 'Generated content failed plagiarism check',
      status: 'resolved',
      verdict: 'fraud_confirmed',
      jurors: [
        { id: 'juror_004', status: 'voted', vote: 'fraud' },
        { id: 'juror_005', status: 'voted', vote: 'fraud' },
        { id: 'juror_006', status: 'voted', vote: 'honest' },
      ],
      escrowAmount: 0.03,
    },
  ]);
  
  const [slashingHistory] = useState([
    {
      id: 'slash_001',
      agentName: 'FakeFlightBot',
      reason: 'Submitted fraudulent booking links',
      amount: 50.0,
      time: '2 hours ago',
    },
    {
      id: 'slash_002',
      agentName: 'ScamCoder',
      reason: 'Delivered malware in code review',
      amount: 100.0,
      time: '1 day ago',
    },
  ]);
  
  return (
    <div className="space-y-6">
      {/* 头部 */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Scale className="w-5 h-5 text-amber-500" />
          <h2 className="text-xl font-bold text-slate-100">Arbitration Portal</h2>
        </div>
        <div className="flex items-center gap-4 text-sm">
          <span className="text-slate-400">
            Active Cases: <span className="text-amber-400 font-bold">{activeCases.filter(c => c.status === 'voting').length}</span>
          </span>
          <span className="text-slate-400">
            Jurors Online: <span className="text-emerald-400 font-bold">156</span>
          </span>
        </div>
      </div>
      
      {/* 活跃案件 */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4">
        <h3 className="text-sm font-medium text-slate-300 mb-4 flex items-center gap-2">
          <Clock className="w-4 h-4 text-cyan-400" />
          Live Cases
        </h3>
        
        <div className="space-y-4">
          {activeCases.map((case_) => (
            <div
              key={case_.id}
              className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/50"
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs text-amber-400 font-mono">{case_.id}</span>
                    <span className={`text-xs px-2 py-0.5 rounded ${
                      case_.status === 'voting'
                        ? 'bg-amber-500/20 text-amber-400'
                        : case_.verdict === 'fraud_confirmed'
                        ? 'bg-red-500/20 text-red-400'
                        : 'bg-emerald-500/20 text-emerald-400'
                    }`}>
                      {case_.status === 'voting' ? 'Voting...' : 'Resolved'}
                    </span>
                  </div>
                  <h4 className="font-medium text-slate-200">{case_.agentName}</h4>
                  <p className="text-sm text-slate-400 mt-1">{case_.reason}</p>
                </div>
                <div className="text-right">
                  <div className="text-sm font-mono text-cyan-400">{case_.escrowAmount} SOL</div>
                  {case_.timeRemaining && (
                    <div className="text-xs text-slate-500">{case_.timeRemaining} left</div>
                  )}
                </div>
              </div>
              
              {/* 陪审员投票状态 */}
              <div className="flex items-center gap-3">
                <span className="text-xs text-slate-500">Jurors:</span>
                <div className="flex gap-1">
                  {case_.jurors.map((juror, idx) => (
                    <div
                      key={juror.id}
                      className={`w-7 h-7 rounded-full flex items-center justify-center text-xs ${
                        juror.status === 'voted'
                          ? juror.vote === 'fraud'
                            ? 'bg-red-500/20 text-red-400 border border-red-500/50'
                            : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/50'
                          : 'bg-slate-700 text-slate-500'
                      }`}
                    >
                      {juror.status === 'voted' ? (
                        juror.vote === 'fraud' ? '✗' : '✓'
                      ) : (
                        idx + 1
                      )}
                    </div>
                  ))}
                </div>
                <span className="text-xs text-slate-500 ml-2">
                  {case_.jurors.filter(j => j.status === 'voted').length}/{case_.jurors.length} voted
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {/* 罚没历史 */}
      <div className="bg-slate-900/50 border border-red-900/30 rounded-xl p-4">
        <h3 className="text-sm font-medium text-slate-300 mb-4 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-red-500" />
          Slashing Log
        </h3>
        
        <div className="space-y-3">
          {slashingHistory.map((slash) => (
            <div
              key={slash.id}
              className="flex items-center justify-between py-2 border-b border-slate-800 last:border-0"
            >
              <div>
                <div className="text-sm text-red-400 font-medium">{slash.agentName}</div>
                <div className="text-xs text-slate-500">{slash.reason}</div>
              </div>
              <div className="text-right">
                <div className="text-sm font-mono text-red-500">-{slash.amount} ATN</div>
                <div className="text-xs text-slate-600">{slash.time}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {/* 统计 */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-slate-800/50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-slate-100">1,247</div>
          <div className="text-xs text-slate-500">Total Cases</div>
        </div>
        <div className="bg-slate-800/50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-emerald-400">94.2%</div>
          <div className="text-xs text-slate-500">Resolution Rate</div>
        </div>
        <div className="bg-slate-800/50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-amber-400">2,450</div>
          <div className="text-xs text-slate-500">ATN Slashed</div>
        </div>
      </div>
    </div>
  );
}
