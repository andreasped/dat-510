import time
import matplotlib.pyplot as plt
from blockchain import Blockchain
from wallet import Wallet


def measure_transaction_rate(blockchain, num_transactions):
    # Create wallets for users
    users = {}
    for i in range(10):  # Adjust number of users as needed
        user_id = f"User_{i}"
        users[user_id] = Wallet()

    transactions = []  # Store all created transactions
    start_time = time.time()

    for i in range(1, num_transactions + 1):
        sender_id = f"User_{i % 10}"
        recipient_id = f"User_{(i + 1) % 10}"
        amount = i * 0.1
        sender_wallet = users[sender_id]
        recipient_wallet = users[recipient_id]

        transaction = sender_wallet.create_transaction(recipient_wallet.address, amount)
        transactions.append(transaction)

        # Attempt to add transaction to the blockchain
        blockchain.add_transaction(transaction)

    end_time = time.time()
    time_taken = end_time - start_time
    transaction_rate = num_transactions / time_taken
    return transaction_rate, time_taken


# Initialize the blockchain
max_tx_per_block = 10
difficulty = 3
blockchain = Blockchain(max_transactions_per_block=max_tx_per_block, difficulty=difficulty)

# Measure transaction rate for a certain number of transactions
num_transactions = 100  # Adjust as needed
transaction_rate, time_taken = measure_transaction_rate(blockchain, num_transactions)

print(f"Transaction Rate: {transaction_rate:.2f} transactions/second")
print(f"Total Time Taken: {time_taken:.2f} seconds")




# Test increasing number of transactions
transaction_counts = [100, 200, 500, 1000, 2000]
results = []

for count in transaction_counts:
    rate, time_taken = measure_transaction_rate(blockchain, count)
    results.append((count, rate, time_taken))
    print(f"Processed {count} transactions: Rate = {rate:.2f} transactions/second, Time Taken = {time_taken:.2f} seconds")

# Analyze results
for count, rate, time_taken in results:
    print(f"Transaction Count: {count}, Rate: {rate:.2f}, Time: {time_taken:.2f} seconds")



####### MAX TRANSACTIONS PER BLOCK #######

# List of block sizes to test
transaction_limits = [10, 20, 50, 100]
transaction_count = 100
difficulty = 3

# Experiment results
experiment_results = []

for max_tx_per_block in transaction_limits:
    print(f"\n--- Testing with max {max_tx_per_block} transactions per block ---\n")

    # Initialize blockchain and users
    blockchain = Blockchain(max_transactions_per_block=max_tx_per_block, difficulty=difficulty)
    users = {f"User_{i}": Wallet() for i in range(10)}

    # Generate and add 100 signed transactions
    transactions = []
    start_time = time.time()

    for i in range(1, transaction_count + 1):
        sender_id = f"User_{i % 10}"
        recipient_id = f"User_{(i + 1) % 10}"
        amount = i * 0.1
        transaction = users[sender_id].create_transaction(users[recipient_id].address, amount)
        transactions.append(transaction)
        
        blockchain.add_transaction(transaction)

    # Calculate transaction adding time and TPS
    transaction_time = time.time() - start_time
    transactions_per_second = transaction_count / transaction_time
    print(f"Time taken to add {transaction_count} transactions: {transaction_time:.2f} seconds")
    print(f"Transactions per second (TPS): {transactions_per_second:.2f}")

    # Mine the transactions
    print("Mining started...")
    mining_start = time.time()
    block_index = blockchain.mine()
    mining_time = time.time() - mining_start
    if block_index:
        print(f"Mining completed. Blocks up to {block_index} added.")
    else:
        print("Mining failed.")

    # Store results for this block size
    experiment_results.append({
        'max_tx_per_block': max_tx_per_block,
        'transaction_time': transaction_time,
        'transactions_per_second': transactions_per_second,
        'mining_time': mining_time,
    })

# Display experiment results
print("\n--- Experiment Results ---")
for result in experiment_results:
    print(
        f"Max TX per Block: {result['max_tx_per_block']} | "
        f"Transaction Time: {result['transaction_time']:.2f}s | "
        f"Transactions per Second: {result['transactions_per_second']:.2f} TPS | "
        f"Mining Time: {result['mining_time']:.2f}s"
    )
