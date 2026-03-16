import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Wallet, ArrowRight, Shield, Clock } from 'lucide-react';

// 交易模态框
export function TransactionModal({ agent, isOpen, onClose, onConfirm }) {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    origin: '',
    destination: '',
    date: '',
    budget: '',
  });
  
  const handleNext = () => {
    if (step < 3) setStep(step + 1);
    else onConfirm(formData);
  };
  
  const steps = [
    { title: 'Task Details', description: 'Enter your requirements' },
    { title: 'Review', description: 'Confirm task and payment' },
    { title: 'Payment', description: 'Lock funds in escrow' },
  ];
  
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="bg-slate-900 border-slate-800 text-slate-100 max-w-lg">
        <DialogHeader>
          <DialogTitle className="text-xl font-bold">
            Hire {agent?.name}
          </DialogTitle>
        </DialogHeader>
        
        {/* 步骤指示器 */}
        <div className="flex items-center justify-between mb-6">
          {steps.map((s, index) => (
            <div key={index} className="flex items-center">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                step > index + 1 ? 'bg-emerald-500 text-white' :
                step === index + 1 ? 'bg-cyan-600 text-white' :
                'bg-slate-800 text-slate-500'
              }`}>
                {step > index + 1 ? '✓' : index + 1}
              </div>
              {index < 2 && (
                <div className={`w-12 h-0.5 mx-2 ${
                  step > index + 1 ? 'bg-emerald-500' : 'bg-slate-800'
                }`} />
              )}
            </div>
          ))}
        </div>
        
        {/* 步骤内容 */}
        <div className="space-y-4">
          {step === 1 && (
            <>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label className="text-slate-400">From</Label>
                  <Input
                    placeholder="NYC"
                    value={formData.origin}
                    onChange={(e) => setFormData({...formData, origin: e.target.value})}
                    className="bg-slate-800 border-slate-700 text-slate-100"
                  />
                </div>
                <div>
                  <Label className="text-slate-400">To</Label>
                  <Input
                    placeholder="LAX"
                    value={formData.destination}
                    onChange={(e) => setFormData({...formData, destination: e.target.value})}
                    className="bg-slate-800 border-slate-700 text-slate-100"
                  />
                </div>
              </div>
              
              <div>
                <Label className="text-slate-400">Date</Label>
                <Input
                  type="date"
                  value={formData.date}
                  onChange={(e) => setFormData({...formData, date: e.target.value})}
                  className="bg-slate-800 border-slate-700 text-slate-100"
                />
              </div>
              
              <div>
                <Label className="text-slate-400">Max Budget (USD)</Label>
                <Input
                  type="number"
                  placeholder="500"
                  value={formData.budget}
                  onChange={(e) => setFormData({...formData, budget: e.target.value})}
                  className="bg-slate-800 border-slate-700 text-slate-100"
                />
              </div>
            </>
          )}
          
          {step === 2 && (
            <div className="bg-slate-800/50 rounded-lg p-4 space-y-3">
              <div className="flex justify-between">
                <span className="text-slate-400">Agent</span>
                <span className="text-slate-100">{agent?.name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Task</span>
                <span className="text-slate-100">Flight Search</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Route</span>
                <span className="text-slate-100">{formData.origin} → {formData.destination}</span>
              </div>
              <div className="border-t border-slate-700 pt-3 flex justify-between">
                <span className="text-slate-400">Service Fee</span>
                <span className="text-cyan-400">{agent?.baseFee} SOL</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-500">Escrow Amount</span>
                <span className="text-slate-400">{agent?.baseFee} SOL</span>
              </div>
            </div>
          )}
          
          {step === 3 && (
            <div className="space-y-4">
              <div className="bg-cyan-950/30 border border-cyan-500/30 rounded-lg p-4">
                <div className="flex items-center gap-3 mb-3">
                  <Shield className="w-5 h-5 text-cyan-400" />
                  <span className="font-medium text-cyan-400">Secure Escrow</span>
                </div>
                <p className="text-sm text-slate-400">
                  Your funds will be locked in a smart contract. 
                  They will only be released to the agent after successful task completion.
                </p>
              </div>
              
              <div className="flex items-center gap-3 p-3 bg-slate-800/50 rounded-lg">
                <Wallet className="w-5 h-5 text-slate-400" />
                <div className="flex-1">
                  <div className="text-sm text-slate-300">Wallet Balance</div>
                  <div className="text-xs text-slate-500">125.5 SOL</div>
                </div>
                <div className="text-emerald-400 text-sm">Connected</div>
              </div>
              
              <div className="flex items-center gap-2 text-sm text-slate-400">
                <Clock className="w-4 h-4" />
                <span>Task timeout: 15 minutes</span>
              </div>
            </div>
          )}
        </div>
        
        {/* 按钮 */}
        <div className="flex gap-3 mt-6">
          {step > 1 && (
            <Button
              variant="outline"
              onClick={() => setStep(step - 1)}
              className="flex-1 border-slate-700 text-slate-300 hover:bg-slate-800"
            >
              Back
            </Button>
          )}
          <Button
            onClick={handleNext}
            className="flex-1 bg-cyan-600 hover:bg-cyan-500 text-white"
          >
            {step === 3 ? (
              <>
                Lock {agent?.baseFee} SOL <ArrowRight className="w-4 h-4 ml-2" />
              </>
            ) : (
              'Next'
            )}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
