use anchor_lang::prelude::*;

// ATN Protocol - AgentTrust Nexus Smart Contract
// Solana Devnet MVP

declare_id!("6azcDVHXEm8ejGYWPfu7QLRQiXktJvnBBAtnp7qbEqzv");

#[program]
pub mod atn_protocol {
    use super::*;

    // Initialize protocol
    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        let protocol = &mut ctx.accounts.protocol;
        protocol.authority = ctx.accounts.authority.key();
        protocol.total_tasks = 0;
        protocol.total_volume = 0;

        msg!("ATN Protocol initialized");
        Ok(())
    }

    // Create task
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

    // Lock funds in escrow
    pub fn lock_funds(ctx: Context<LockFunds>) -> Result<()> {
        let task = &mut ctx.accounts.task;

        require!(
            task.status == TaskStatus::Created,
            ATNError::InvalidTaskStatus
        );

        task.status = TaskStatus::Locked;

        // Transfer to escrow account
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

    // Complete task and release funds
    pub fn complete_task(ctx: Context<CompleteTask>) -> Result<()> {
        let task = &mut ctx.accounts.task;

        require!(
            task.status == TaskStatus::Locked,
            ATNError::InvalidTaskStatus
        );

        task.status = TaskStatus::Completed;

        // Release funds to seller
        **ctx.accounts.escrow.to_account_info().try_borrow_mut_lamports()? -= task.amount;
        **ctx.accounts.seller.to_account_info().try_borrow_mut_lamports()? += task.amount;

        msg!("Task completed, funds released");
        Ok(())
    }

    // Refund buyer
    pub fn refund(ctx: Context<Refund>) -> Result<()> {
        let task = &mut ctx.accounts.task;
        let clock = Clock::get()?;

        require!(
            task.status == TaskStatus::Locked,
            ATNError::InvalidTaskStatus
        );

        // Check timeout (simplified)
        require!(
            clock.unix_timestamp > task.created_at + 3600,
            ATNError::TimeoutNotReached
        );

        task.status = TaskStatus::Refunded;

        // Refund to buyer
        **ctx.accounts.escrow.to_account_info().try_borrow_mut_lamports()? -= task.amount;
        **ctx.accounts.buyer.to_account_info().try_borrow_mut_lamports()? += task.amount;

        msg!("Refund processed");
        Ok(())
    }
}

// Account structures
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

// Instruction contexts
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

// Error codes
#[error_code]
pub enum ATNError {
    #[msg("Invalid task status")]
    InvalidTaskStatus,
    #[msg("Timeout not reached")]
    TimeoutNotReached,
}
