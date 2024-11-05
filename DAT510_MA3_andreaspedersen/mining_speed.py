import time
import matplotlib.pyplot as plt
from blockchain import Blockchain
from wallet import Wallet

# Function to mine blocks and measure time taken
def measure_mining_time(difficulty, max_tx_per_block=10, total_transactions=10):
    blockchain = Blockchain(max_transactions_per_block=max_tx_per_block, difficulty=difficulty)

    # Create wallets for users
    users = {}
    for i in range(10):
        user_id = f"User_{i}"
        users[user_id] = Wallet()

    # Generate and add signed transactions
    transactions = []  # Store all created transactions for testing
    for i in range(1, total_transactions + 1):
        sender_id = f"User_{i % 10}"
        recipient_id = f"User_{(i + 1) % 10}"
        amount = i * 0.1
        sender_wallet = users[sender_id]
        recipient_wallet = users[recipient_id]

        transaction = sender_wallet.create_transaction(recipient_wallet.address, amount)
        transactions.append(transaction)  # Keep track of transactions

        if blockchain.add_transaction(transaction):
            print(f"Transaction {i} added: {transaction}")
        else:
            print(f"Transaction {i} is invalid and was discarded.")

    # Mine the transactions and measure the time
    print(f"Mining started with difficulty level {difficulty}...")
    start_time = time.time()  # Start timing
    block_index = blockchain.mine()
    end_time = time.time()  # End timing

    mining_time = end_time - start_time
    if block_index:
        print(f"Mining completed. Blocks up to {block_index} have been added to the blockchain in {mining_time:.2f} seconds.")
    else:
        print("No transactions to mine or mining failed.")

    return mining_time


# Define a list of difficulty levels to test
difficulty_levels = [1, 2, 3, 4, 5]  # Adjust as needed
results = []

# Measure mining time for each difficulty level
for difficulty in difficulty_levels:
    time_taken = measure_mining_time(difficulty)
    results.append((difficulty, time_taken))

# Present results
print("\nMining Time Results:")
print("Difficulty Level | Time Taken (seconds)")
for difficulty, time_taken in results:
    print(f"{difficulty:<17} | {time_taken:.4f}")


# Extracting time taken values
time_taken = [time for difficulty, time in results]

# Define difficulty levels just for labeling
difficulty_labels = ['1', '2', '3', '4', '5']

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(difficulty_labels, time_taken, marker='o', linestyle='-', color='b')

# Adding title and labels
plt.title('Mining Time vs. Difficulty', fontsize=16)
plt.xlabel('Difficulty', fontsize=14)
plt.ylabel('Mining Time (seconds)', fontsize=14)
plt.grid(True)

# Show the plot
plt.savefig('mining_time_vs_difficulty.png')  # Save the figure as a PNG file
plt.show()
