use anchor_lang::prelude::*;

// ATN Protocol - 简化版智能合约
// 用于MVP演示

declare_id!("ATNProtocol1111111111111111111111111111111");

#[program]
pub mod atn_protocol {
    use super::*;

    // 初始化协议
    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        let protocol = &mut ctx.accounts.protocol;
        protocol.authority = ctx.accounts.authority.key();
        protocol.total_tasks = 0;
        protocol.total_volume = 0;
        
        msg!("ATN Protocol initialized");
        Ok(())
    }

    // 创建任务
    pub fn create_task(
        ctx: Context<CreateTask>,
        task_id: String,
        amount: u64,
    ) -> Result<()> {
        let task = &mut ctx.accounts.task;
        let protocol = &mut ctx.accounts.protocol;
        
        task.task_id = task_id;
        task.buyer = ctx.accounts.buyer.key();
        task.seller = ctx.accounts.seller.key();
        task.amount = amount;
        task.status = TaskStatus::Created;
        task.created_at = Clock::get()?.unix_timestamp;
        
        protocol.total_tasks += 1;
        protocol.total_volume += amount;
        
        msg!("Task created: {}", task.task_id);
        Ok(())
    }

    // 锁定资金
    pub fn lock_funds(ctx: Context<LockFunds>) -> Result<()> {
        let task = &mut ctx.accounts.task;
        
        require!(
            task.status == TaskStatus::Created,
            ErrorCode::InvalidTaskStatus
        );
        
        task.status = TaskStatus::Locked;
        
        // 转账到托管账户
        let cpi_accounts = anchor_lang::system_program::Transfer {
            from: ctx.accounts.buyer.to_account_info(),
            to: ctx.accounts.escrow.to_account_info(),
        };
        let cpi_ctx = CpiContext::new(
            ctx.accounts.system_program.to_account_info(),
            cpi_accounts,
        );
        anchor_lang::system_program::transfer(cpi_ctx, task.amount)?;
        
        msg!("Funds locked: {} lamports", task.amount);
        Ok(())
    }

    // 完成任务
    pub fn complete_task(ctx: Context<CompleteTask>) -> Result<()> {
        let task = &mut ctx.accounts.task;
        
        require!(
            task.status == TaskStatus::Locked,
            ErrorCode::InvalidTaskStatus
        );
        
        task.status = TaskStatus::Completed;
        
        // 释放资金给卖方
        **ctx.accounts.escrow.to_account_info().try_borrow_mut_lamports()? -= task.amount;
        **ctx.accounts.seller.to_account_info().try_borrow_mut_lamports()? += task.amount;
        
        msg!("Task completed, funds released");
        Ok(())
    }

    // 退款
    pub fn refund(ctx: Context<Refund>) -> Result<()> {
        let task = &mut ctx.accounts.task;
        let clock = Clock::get()?;
        
        require!(
            task.status == TaskStatus::Locked,
            ErrorCode::InvalidTaskStatus
        );
        
        // 检查超时 (简化版，实际应使用更复杂的逻辑)
        require!(
            clock.unix_timestamp > task.created_at + 3600,
            ErrorCode::TimeoutNotReached
        );
        
        task.status = TaskStatus::Refunded;
        
        // 退款给买方
        **ctx.accounts.escrow.to_account_info().try_borrow_mut_lamports()? -= task.amount;
        **ctx.accounts.buyer.to_account_info().try_borrow_mut_lamports()? += task.amount;
        
        msg!("Refund processed");
        Ok(())
    }
}

// 账户结构
#[account]
pub struct Protocol {
    pub authority: Pubkey,
    pub total_tasks: u64,
    pub total_volume: u64,
}

#[account]
pub struct Task {
    pub task_id: String,
    pub buyer: Pubkey,
    pub seller: Pubkey,
    pub amount: u64,
    pub status: TaskStatus,
    pub created_at: i64,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, PartialEq)]
pub enum TaskStatus {
    Created,
    Locked,
    Completed,
    Refunded,
}

// 指令上下文
#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = authority, space = 8 + 32 + 8 + 8)]
    pub protocol: Account<'info, Protocol>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct CreateTask<'info> {
    #[account(init, payer = buyer, space = 8 + 64 + 32 + 32 + 8 + 1 + 8)]
    pub task: Account<'info, Task>,
    #[account(mut)]
    pub buyer: Signer<'info>,
    /// CHECK: Seller pubkey
    pub seller: AccountInfo<'info>,
    #[account(mut)]
    pub protocol: Account<'info, Protocol>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct LockFunds<'info> {
    #[account(mut)]
    pub task: Account<'info, Task>,
    #[account(mut)]
    pub buyer: Signer<'info>,
    /// CHECK: Escrow account
    #[account(mut)]
    pub escrow: AccountInfo<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct CompleteTask<'info> {
    #[account(mut)]
    pub task: Account<'info, Task>,
    #[account(mut)]
    pub seller: Signer<'info>,
    /// CHECK: Escrow account
    #[account(mut)]
    pub escrow: AccountInfo<'info>,
}

#[derive(Accounts)]
pub struct Refund<'info> {
    #[account(mut)]
    pub task: Account<'info, Task>,
    #[account(mut)]
    pub buyer: Signer<'info>,
    /// CHECK: Escrow account
    #[account(mut)]
    pub escrow: AccountInfo<'info>,
}

// 错误码
#[error_code]
pub enum ErrorCode {
    #[msg("Invalid task status")]
    InvalidTaskStatus,
    #[msg("Timeout not reached")]
    TimeoutNotReached,
}
