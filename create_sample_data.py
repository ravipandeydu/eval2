import asyncio
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db, init_db
from cruds import user_crud, transaction_crud, transfer_crud
from schemas.user_schema import UserCreate
from schemas.transaction_schema import TransactionCreate


async def create_sample_data():
    """Create sample data for testing the API"""
    print("Initializing database...")
    await init_db()
    
    # Get database session
    async for db in get_db():
        try:
            print("Creating sample users...")
            
            # Create 6 sample users
            users_data = [
                {
                    "username": "alice_smith",
                    "email": "alice@example.com",
                    "password": "password123",
                    "phone_number": "+1234567890",
                    "balance": 1000.00
                },
                {
                    "username": "bob_johnson",
                    "email": "bob@example.com",
                    "password": "password123",
                    "phone_number": "+1234567891",
                    "balance": 1500.00
                },
                {
                    "username": "charlie_brown",
                    "email": "charlie@example.com",
                    "password": "password123",
                    "phone_number": "+1234567892",
                    "balance": 750.00
                },
                {
                    "username": "diana_prince",
                    "email": "diana@example.com",
                    "password": "password123",
                    "phone_number": "+1234567893",
                    "balance": 2000.00
                },
                {
                    "username": "eve_adams",
                    "email": "eve@example.com",
                    "password": "password123",
                    "phone_number": "+1234567894",
                    "balance": 500.00
                },
                {
                    "username": "frank_miller",
                    "email": "frank@example.com",
                    "password": "password123",
                    "phone_number": "+1234567895",
                    "balance": 1200.00
                }
            ]
            
            created_users = []
            for user_data in users_data:
                user_create = UserCreate(**user_data)
                try:
                    user = await user_crud.create_user(db, user_create)
                    created_users.append(user)
                    print(f"Created user: {user.username} (ID: {user.id}) with balance: ${user.balance}")
                except Exception as e:
                    print(f"User {user_data['username']} might already exist: {e}")
                    # Try to get existing user
                    existing_user = await user_crud.get_user_by_username(db, user_data['username'])
                    if existing_user:
                        created_users.append(existing_user)
            
            if len(created_users) < 2:
                print("Not enough users created for transactions")
                return
            
            print("\nCreating sample transactions...")
            
            # Create various types of transactions
            transactions_count = 0
            
            # 1. Add money transactions (CREDIT)
            credit_transactions = [
                {"user_id": created_users[0].id, "amount": 200.00, "description": "Salary deposit"},
                {"user_id": created_users[1].id, "amount": 150.00, "description": "Freelance payment"},
                {"user_id": created_users[2].id, "amount": 300.00, "description": "Gift money"},
                {"user_id": created_users[3].id, "amount": 500.00, "description": "Bonus payment"},
                {"user_id": created_users[4].id, "amount": 100.00, "description": "Cashback reward"},
            ]
            
            for tx_data in credit_transactions:
                try:
                    result = await user_crud.add_money_in_wallet(
                        db, tx_data["user_id"], tx_data["amount"], tx_data["description"]
                    )
                    transactions_count += 1
                    print(f"Added ${tx_data['amount']} to user {tx_data['user_id']}: {tx_data['description']}")
                except Exception as e:
                    print(f"Error adding money: {e}")
            
            # 2. Withdraw money transactions (DEBIT)
            debit_transactions = [
                {"user_id": created_users[0].id, "amount": 50.00, "description": "ATM withdrawal"},
                {"user_id": created_users[1].id, "amount": 75.00, "description": "Online purchase"},
                {"user_id": created_users[2].id, "amount": 25.00, "description": "Coffee shop"},
                {"user_id": created_users[3].id, "amount": 100.00, "description": "Grocery shopping"},
                {"user_id": created_users[4].id, "amount": 30.00, "description": "Gas station"},
            ]
            
            for tx_data in debit_transactions:
                try:
                    result = await user_crud.subtract_money_from_wallet(
                        db, tx_data["user_id"], tx_data["amount"], tx_data["description"]
                    )
                    transactions_count += 1
                    print(f"Withdrew ${tx_data['amount']} from user {tx_data['user_id']}: {tx_data['description']}")
                except Exception as e:
                    print(f"Error withdrawing money: {e}")
            
            # 3. Transfer transactions (TRANSFER_IN/TRANSFER_OUT)
            transfer_transactions = [
                {"sender": created_users[0].id, "recipient": created_users[1].id, "amount": 100.00, "description": "Dinner split"},
                {"sender": created_users[1].id, "recipient": created_users[2].id, "amount": 50.00, "description": "Book payment"},
                {"sender": created_users[2].id, "recipient": created_users[3].id, "amount": 75.00, "description": "Movie tickets"},
                {"sender": created_users[3].id, "recipient": created_users[4].id, "amount": 200.00, "description": "Rent contribution"},
                {"sender": created_users[4].id, "recipient": created_users[5].id, "amount": 25.00, "description": "Coffee money"},
                {"sender": created_users[5].id, "recipient": created_users[0].id, "amount": 150.00, "description": "Loan repayment"},
                {"sender": created_users[1].id, "recipient": created_users[3].id, "amount": 80.00, "description": "Gift"},
                {"sender": created_users[2].id, "recipient": created_users[5].id, "amount": 40.00, "description": "Taxi fare"},
                {"sender": created_users[4].id, "recipient": created_users[0].id, "amount": 60.00, "description": "Lunch money"},
                {"sender": created_users[5].id, "recipient": created_users[2].id, "amount": 90.00, "description": "Utility bill split"},
            ]
            
            for tx_data in transfer_transactions:
                try:
                    result = await transfer_crud.transfer_money(
                        db, 
                        tx_data["sender"], 
                        tx_data["recipient"], 
                        tx_data["amount"], 
                        tx_data["description"]
                    )
                    transactions_count += 2  # Each transfer creates 2 transactions
                    print(f"Transferred ${tx_data['amount']} from user {tx_data['sender']} to user {tx_data['recipient']}: {tx_data['description']}")
                except Exception as e:
                    print(f"Error transferring money: {e}")
            
            print(f"\nSample data creation completed!")
            print(f"Created {len(created_users)} users")
            print(f"Created approximately {transactions_count} transactions")
            
            # Display final balances
            print("\nFinal user balances:")
            for user in created_users:
                balance = await user_crud.get_wallet_balance(db, user.id)
                print(f"  {user.username}: ${balance}")
                
        except Exception as e:
            print(f"Error creating sample data: {e}")
        finally:
            await db.close()
            break


if __name__ == "__main__":
    asyncio.run(create_sample_data())