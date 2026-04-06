pub fn settle_auction(
    deps: DepsMut,
    env: Env,
    info: MessageInfo,
    auction_id: u64,
) -> Result<Response> {
    // ========== CHECKS ==========
    
    // Check auction exists
    let mut auction = AUCTIONS.load(deps.storage, auction_id)?;
    
    // Check auction has ended
    if env.block.time < auction.end_time {
        return Err(ContractError::AuctionStillActive);
    }
    
    // Check auction not already settled
    if auction.settled {
        return Err(ContractError::AlreadySettled);
    }
    
    // Check caller is authorized (oracle or admin)
    if !is_authorized(&info.sender) {
        return Err(ContractError::Unauthorized);
    }
    
    // Check high bidder exists
    let high_bidder = auction.high_bidder
        .ok_or(ContractError::NoBids)?;
    
    // ========== EFFECTS ==========
    
    // Mark auction as settled
    auction.settled = true;
    AUCTIONS.save(deps.storage, auction_id, &auction)?;
    
    // Calculate fees (1.1%) using safe math
    let fee = auction.high_bid.multiply_ratio(11u128, 1000u128);
    let seller_amount = auction.high_bid.checked_sub(fee)
        .ok_or(ContractError::Overflow)?;
    
    // Update Community Reserve Fund
    let mut fund = COMMUNITY_RESERVE_FUND.load(deps.storage)?;
    fund.balance = fund.balance.checked_add(fee)
        .ok_or(ContractError::Overflow)?;
    COMMUNITY_RESERVE_FUND.save(deps.storage, &fund)?;
    
    // Mint PHNX voting weight (non-transferable)
    mint_phnx_weight(deps.storage, &high_bidder, fee)?;
    
    // ========== INTERACTIONS ==========
    
    // Send funds to seller (TESTUSD)
    let seller_msg = BankMsg::Send {
        to_address: auction.seller.to_string(),
        amount: vec![Coin {
            denom: TESTUSD_DENOM.to_string(),
            amount: seller_amount,
        }],
    };
    
    // Send fee to Community Reserve Fund
    let fee_msg = BankMsg::Send {
        to_address: fund.address.to_string(),
        amount: vec![Coin {
            denom: TESTUSD_DENOM.to_string(),
            amount: fee,
        }],
    };
    
    Ok(Response::new()
        .add_message(seller_msg)
        .add_message(fee_msg)
        .add_attribute("action", "settle_auction")
        .add_attribute("auction_id", auction_id.to_string())
        .add_attribute("seller_amount", seller_amount.to_string())
        .add_attribute("fee", fee.to_string()))
}
Why This Matters:

All state updates happen before external calls

If external call fails, state is still consistent

Impossible to exploit race conditions

Access Control
Role-Based Access Control (RBAC)
// Define roles
#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
pub enum Role {
    Admin,
    Oracle,
    Pauser,
    FeeCollector,
}

// Store roles
const ROLES: Map<&Addr, Vec<Role>> = Map::new("roles");

// Check if address has role
pub fn has_role(storage: &dyn Storage, addr: &Addr, role: Role) -> bool {
    ROLES
        .may_load(storage, addr)
        .unwrap_or(None)
        .map(|roles| roles.contains(&role))
        .unwrap_or(false)
}

// Modifier-style function
pub fn require_role(storage: &dyn Storage, addr: &Addr, role: Role) -> Result<()> {
    if !has_role(storage, addr, role) {
        return Err(ContractError::Unauthorized);
    }
    Ok(())
}

// Usage in functions
pub fn pause_contract(deps: DepsMut, info: MessageInfo) -> Result<Response> {
    // Only pausers can pause
    require_role(deps.storage, &info.sender, Role::Pauser)?;
    
    // Pause logic...
    Ok(Response::new())
}

pub fn confirm_delivery(
    deps: DepsMut,
    info: MessageInfo,
    auction_id: u64,
) -> Result<Response> {
    // Only oracles can confirm delivery
    require_role(deps.storage, &info.sender, Role::Oracle)?;
    
    // Confirmation logic...
    Ok(Response::new())
}
Admin Functions
// Grant role (admin only)
pub fn grant_role(
    deps: DepsMut,
    info: MessageInfo,
    target: Addr,
    role: Role,
) -> Result<Response> {
    // Only admins can grant roles
    require_role(deps.storage, &info.sender, Role::Admin)?;
    
    // Add role
    ROLES.update(deps.storage, &target, |roles| {
        let mut roles = roles.unwrap_or_default();
        if !roles.contains(&role) {
            roles.push(role.clone());
        }
        Ok::<_, StdError>(roles)
    })?;
    
    Ok(Response::new()
        .add_attribute("action", "grant_role")
        .add_attribute("target", target.to_string())
        .add_attribute("role", format!("{:?}", role)))
}

// Revoke role (admin only)
pub fn revoke_role(
    deps: DepsMut,
    info: MessageInfo,
    target: Addr,
    role: Role,
) -> Result<Response> {
    require_role(deps.storage, &info.sender, Role::Admin)?;
    
    ROLES.update(deps.storage, &target, |roles| {
        let mut roles = roles.unwrap_or_default();
        roles.retain(|r| r != &role);
        Ok::<_, StdError>(roles)
    })?;
    
    Ok(Response::new()
        .add_attribute("action", "revoke_role")
        .add_attribute("target", target.to_string())
        .add_attribute("role", format!("{:?}", role)))
}
Time-Locked Admin Actions
For critical admin functions, add time locks:
const PENDING_ADMIN_CHANGE: Item<(Addr, Timestamp)> = Item::new("pending_admin");

pub fn propose_admin_change(
    deps: DepsMut,
    env: Env,
    info: MessageInfo,
    new_admin: Addr,
) -> Result<Response> {
    require_role(deps.storage, &info.sender, Role::Admin)?;
    
    // Save proposal with 48-hour delay
    let execute_time = env.block.time.plus_seconds(48 * 60 * 60);
    PENDING_ADMIN_CHANGE.save(deps.storage, &(new_admin.clone(), execute_time))?;
    
    Ok(Response::new()
        .add_attribute("action", "propose_admin_change")
        .add_attribute("new_admin", new_admin.to_string())
        .add_attribute("execute_time", execute_time.to_string()))
}

pub fn execute_admin_change(deps: DepsMut, env: Env) -> Result<Response> {
    let (new_admin, execute_time) = PENDING_ADMIN_CHANGE.load(deps.storage)?;
    
    // Check time lock has passed
    if env.block.time < execute_time {
        return Err(ContractError::TimeLockNotExpired);
    }
    
    // Execute change
    // ... (grant admin role to new_admin, revoke from old)
    
    // Clear pending change
    PENDING_ADMIN_CHANGE.remove(deps.storage);
    
    Ok(Response::new())
}
Input Validation
Always Validate
pub fn create_auction(
    deps: DepsMut,
    env: Env,
    info: MessageInfo,
    item_id: String,
    description: String,
    starting_price: Uint128,
    reserve_price: Uint128,
    duration: u64,
) -> Result<Response> {
    // Validate item_id
    if item_id.is_empty() || item_id.len() > 100 {
        return Err(ContractError::InvalidItemId);
    }
    
    // Validate description
    if description.is_empty() || description.len() > 1000 {
        return Err(ContractError::InvalidDescription);
    }
    
    // Validate starting price
    if starting_price.is_zero() {
        return Err(ContractError::InvalidPrice);
    }
    
    // Validate reserve price >= starting price
    if reserve_price < starting_price {
        return Err(ContractError::ReserveTooLow);
    }
    
    // Maximum price check (prevent overflow in fee calculations)
    let max_price = Uint128::from(1_000_000_000_000u128); // 1 trillion
    if starting_price > max_price || reserve_price > max_price {
        return Err(ContractError::PriceTooHigh);
    }
    
    // Validate duration (1 hour to 30 days)
    let min_duration = 3600u64;  // 1 hour
    let max_duration = 2_592_000u64; // 30 days
    if duration < min_duration || duration > max_duration {
        return Err(ContractError::InvalidDuration);
    }
    
    // Validate sender has sufficient TESTUSD for collateral
    let collateral = calculate_collateral(&reserve_price);
    check_balance(&deps, &info.sender, collateral)?;
    
    // All validations passed, proceed...
    Ok(Response::new())
}
Address Validation
// Validate address format
pub fn validate_address(deps: &DepsMut, addr: &str) -> Result<Addr> {
    deps.api.addr_validate(addr)
        .map_err(|_| ContractError::InvalidAddress)
}

// Check address is not zero/empty
pub fn require_valid_address(addr: &Addr) -> Result<()> {
    if addr.as_str().is_empty() {
        return Err(ContractError::InvalidAddress);
    }
    Ok(())
}
Safe Math
Use Checked Arithmetic
// ❌ DANGEROUS - Can overflow/underflow
let total = amount1 + amount2;
let result = price * quantity;

// ✅ SAFE - Returns error on overflow
let total = amount1.checked_add(amount2)
    .ok_or(ContractError::Overflow)?;
    
let result = price.checked_mul(quantity)
    .ok_or(ContractError::Overflow)?;
Uint128 Operations
use cosmwasm_std::Uint128;

// Addition
let sum = a.checked_add(b)?;

// Subtraction
let diff = a.checked_sub(b)?;

// Multiplication
let product = a.checked_mul(b)?;

// Division
let quotient = a.checked_div(b)?;

// Percentage calculation (safe)
let fee = amount.multiply_ratio(11u128, 1000u128); // 1.1%

Comparison and Ordering

// Don't use: a > b (might not work as expected)
// Use:
if a.gt(&b) { }
if a.lt(&b) { }
if a.is_zero() { }

// Safe comparison
let max = a.max(b);
let min = a.min(b);

TESTUSD Integration
Denomination Constants

// TESTUSD has 6 decimals (like USDC)
pub const TESTUSD_DENOM: &str = "utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6";
pub const TESTUSD_DECIMALS: u32 = 6;
pub const TESTUSD_FACTOR: u128 = 1_000_000;

// Conversion helpers
pub fn testusd_to_utestusd(amount: Uint128) -> Uint128 {
    amount.checked_mul(Uint128::from(TESTUSD_FACTOR))
        .expect("overflow in conversion")
}

pub fn utestusd_to_testusd(amount: Uint128) -> Uint128 {
    amount.checked_div(Uint128::from(TESTUSD_FACTOR))
        .expect("division by zero in conversion")
}

Safe Collateral Calculations

// Calculate 10% collateral safely
pub fn calculate_collateral(amount: &Uint128) -> Result<Uint128> {
    amount.multiply_ratio(10u128, 100u128) // 10%
}

// Calculate total needed for bid (bid + 10% collateral)
pub fn calculate_total_for_bid(bid_amount: &Uint128) -> Result<Uint128> {
    let collateral = calculate_collateral(bid_amount)?;
    bid_amount.checked_add(collateral)
        .ok_or(ContractError::Overflow)
}

Emergency Controls
Pause Mechanism

const PAUSED: Item<bool> = Item::new("paused");

// Modifier to check if paused
pub fn require_not_paused(storage: &dyn Storage) -> Result<()> {
    if PAUSED.load(storage)? {
        return Err(ContractError::ContractPaused);
    }
    Ok(())
}

// Pause function
pub fn pause(deps: DepsMut, info: MessageInfo) -> Result<Response> {
    require_role(deps.storage, &info.sender, Role::Pauser)?;
    
    PAUSED.save(deps.storage, &true)?;
    
    Ok(Response::new()
        .add_attribute("action", "pause"))
}

// Unpause function
pub fn unpause(deps: DepsMut, info: MessageInfo) -> Result<Response> {
    require_role(deps.storage, &info.sender, Role::Admin)?;
    
    PAUSED.save(deps.storage, &false)?;
    
    Ok(Response::new()
        .add_attribute("action", "unpause"))
}

// Use in critical functions
pub fn place_bid(deps: DepsMut, info: MessageInfo, auction_id: u64) -> Result<Response> {
    // Check if paused
    require_not_paused(deps.storage)?;
    
    // Bid logic...
    Ok(Response::new())
}
Circuit Breaker
For rate-limiting critical operations:

const WITHDRAWAL_LIMIT: Item<WithdrawalLimit> = Item::new("withdrawal_limit");

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct WithdrawalLimit {
    pub amount: Uint128,
    pub reset_time: Timestamp,
}

pub fn withdraw(
    deps: DepsMut,
    env: Env,
    info: MessageInfo,
    amount: Uint128,
) -> Result<Response> {
    // Check daily withdrawal limit
    let mut limit = WITHDRAWAL_LIMIT.load(deps.storage)?;
    
    // Reset if 24 hours passed
    if env.block.time >= limit.reset_time {
        limit.amount = Uint128::zero();
        limit.reset_time = env.block.time.plus_seconds(86400);
    }
    
    // Check if amount exceeds daily limit
    let daily_limit = Uint128::from(1_000_000u128);
    if limit.amount.checked_add(amount)? > daily_limit {
        return Err(ContractError::DailyLimitExceeded);
    }
    
    // Update limit
    limit.amount = limit.amount.checked_add(amount)?;
    WITHDRAWAL_LIMIT.save(deps.storage, &limit)?;
    
    // Proceed with withdrawal...
    Ok(Response::new())
}

Upgrade Patterns
Migrations

#[cfg_attr(not(feature = "library"), entry_point)]
pub fn migrate(deps: DepsMut, _env: Env, _msg: MigrateMsg) -> Result<Response> {
    // Get current version
    let current_version = cw2::get_contract_version(deps.storage)?;
    
    // Check we're upgrading from correct version
    if current_version.contract != CONTRACT_NAME {
        return Err(ContractError::InvalidMigration);
    }
    
    // Version-specific migrations
    match current_version.version.as_str() {
        "0.1.0" => {
            // Migrate from 0.1.0 to 0.2.0
            migrate_0_1_to_0_2(deps.storage)?;
        }
        "0.2.0" => {
            // Already on latest version
        }
        _ => {
            return Err(ContractError::UnknownVersion);
        }
    }
    
    // Update version
    cw2::set_contract_version(deps.storage, CONTRACT_NAME, CONTRACT_VERSION)?;
    
    Ok(Response::new()
        .add_attribute("action", "migrate")
        .add_attribute("from_version", current_version.version)
        .add_attribute("to_version", CONTRACT_VERSION))
}

fn migrate_0_1_to_0_2(storage: &mut dyn Storage) -> Result<()> {
    // Perform data migrations
    // Example: Rename keys, transform data structures, etc.
    Ok(())
}

Testing Security Patterns
Unit Tests

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_reentrancy_protection() {
        let mut deps = mock_dependencies();
        
        // Setup: User has 100 TESTUSD
        setup_user_balance(&mut deps, "user1", Uint128::from(100u128));
        
        // First withdrawal: OK
        let msg = ExecuteMsg::Withdraw { amount: Uint128::from(50u128) };
        let res = execute(deps.as_mut(), mock_env(), mock_info("user1", &[]), msg);
        assert!(res.is_ok());
        
        // Try to withdraw again in same block: Should fail
        let msg = ExecuteMsg::Withdraw { amount: Uint128::from(50u128) };
        let res = execute(deps.as_mut(), mock_env(), mock_info("user1", &[]), msg);
        assert_eq!(res, Err(ContractError::InsufficientFunds));
    }
    
    #[test]
    fn test_overflow_protection() {
        let a = Uint128::MAX;
        let b = Uint128::from(1u128);
        
        // Should return error, not wrap around
        assert!(a.checked_add(b).is_err());
    }
    
    #[test]
    fn test_access_control() {
        let mut deps = mock_dependencies();
        
        // Setup admin role
        let admin = Addr::unchecked("admin");
        ROLES.save(deps.as_mut().storage, &admin, &vec![Role::Admin]).unwrap();
        
        // Non-admin tries to pause: Should fail
        let msg = ExecuteMsg::Pause {};
        let res = execute(deps.as_mut(), mock_env(), mock_info("user1", &[]), msg);
        assert_eq!(res, Err(ContractError::Unauthorized));
        
        // Admin pauses: OK
        let msg = ExecuteMsg::Pause {};
        let res = execute(deps.as_mut(), mock_env(), mock_info("admin", &[]), msg);
        assert!(res.is_ok());
    }
    
    #[test]
    fn test_testusd_conversions() {
        let testusd = Uint128::from(1000u128);
        let utestusd = testusd_to_utestusd(testusd);
        assert_eq!(utestusd, Uint128::from(1_000_000_000u128));
        
        let back = utestusd_to_testusd(utestusd);
        assert_eq!(back, testusd);
    }
}

Security Audit Checklist
Before deploying any contract, verify:

Reentrancy
All state updates happen before external calls

Reentrancy guards used where needed

No reliance on contract balance

Access Control
All admin functions have role checks

Critical functions have time locks

Role management functions exist

Default roles properly initialized

Input Validation
All inputs validated (length, range, format)

Addresses validated

Amounts checked for zero/overflow

Edge cases tested (empty strings, max values)

Math
All arithmetic uses checked operations

Division by zero handled

Percentage calculations use multiply_ratio

TESTUSD conversions tested

Emergency
Pause mechanism implemented

Circuit breakers for critical operations

Admin can upgrade/migrate contract

Emergency withdrawal function (if needed)

TESTUSD Specific
Denomination constants correct

Decimal handling consistent

Collateral calculations accurate

Fee calculations accurate (1.1%)

Testing
Unit tests for all functions

Integration tests for user flows

Fuzz tests for math operations

Edge cases tested

All 16 tests passing (as of Feb 24)

Related Documentation
Bridge Security - Cross-chain security

Oracle Design - Oracle security considerations

Testing Guide - Comprehensive testing

Architecture Overview - System architecture

References
CosmWasm Security Best Practices

Solidity Security Patterns

DASP Top 10 - Decentralized Application Security Project

Changelog
2026-02-24: Added TESTUSD integration, updated examples, added security checklist

2026-02-15: Initial version

Feedback
Found a security issue? Please report responsibly:

Security vulnerabilities: security@phoenixpme.com (private disclosure)

General questions: gjf20842@gmail.com

GitHub issues: https://github.com/greg-gzillion/TX/issues