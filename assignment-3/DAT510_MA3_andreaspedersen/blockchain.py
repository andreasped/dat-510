from block import Block


# Blockchain Class with Transaction Limit and Signature Verification
class Blockchain:

    def __init__(self, max_transactions_per_block=10, difficulty=3):
        self.unconfirmed_transactions = []  # Transactions to be mined
        self.chain = []  # List of blocks in the blockchain
        self.max_transactions_per_block = (
            max_transactions_per_block  # Max transactions per block
        )
        self.difficulty = difficulty
        self.create_genesis_block()  # Create the genesis block

    def __str__(self):
        blockchain_summary = (
            f"Blockchain(length={len(self.chain)}, difficulty={self.difficulty})\n"
        )
        blockchain_summary += "Blocks:\n"
        for block in self.chain:
            blockchain_summary += f"  {block}\n"
        return blockchain_summary

    def create_genesis_block(self):
        """
        Generate the genesis block and add it to the chain.

        Steps:
        - Create a new Block with index 0, empty transactions, and previous_hash "0".
        - Compute the hash of the genesis block.
        - Append the genesis block to the chain.
        """
        genesis_block = Block(0, [], "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        """
        Return the last block in the chain.
        """
        return self.chain[-1]

    def add_transaction(self, transaction):
        """
        Add a valid transaction to the list of unconfirmed transactions.

        Steps:
        - Verify if the transaction is valid by calling transaction.is_valid().
        - If valid, append it to unconfirmed_transactions and return True.
        - If invalid, return False.
        """
        if transaction.is_valid():
            self.unconfirmed_transactions.append(transaction)
            return True
        else:
            return False

    def proof_of_work(self, block):
        """
        Perform the proof-of-work algorithm to find a valid hash for the block.

        Steps:
        - Initialize the block's nonce to 0.
        - Compute the hash of the block.
        - While the hash does not start with the required number of zeros (based on difficulty):
            - Increment the nonce by 1.
            - Recompute the hash.
        - Once a valid hash is found, update the block's hash and return the hash.
        """
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith("0" * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
            if computed_hash.startswith("0" * self.difficulty):
                block.hash = computed_hash
                return computed_hash

    def add_block(self, block, proof):
        """
        Validate and add the block to the chain.

        Steps:
        - Get the hash of the last block and compare it with block.previous_hash.
          If they are not equal, return False.
        - Validate the proof by calling is_valid_proof(block, proof).
          If not valid, return False.
        - Append the block to the chain.
        - Return True to indicate success.
        """
        if block.previous_hash != self.last_block.hash:
            return False
        is_valid = self.is_valid_proof(block, proof)
        if not is_valid:
            return False
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """
        Check if the block_hash is a valid hash of the block and satisfies the difficulty criteria.

        Steps:
        - Check if block_hash starts with the required number of zeros (based on difficulty).
        - Recompute the hash of the block and compare it with block_hash.
        - Return True if both conditions are met; otherwise, return False.
        """
        if block_hash.startswith("0" * self.difficulty):
            recomputed_hash = block.compute_hash()
            if recomputed_hash == block_hash:
                return True
            else:
                return False

    def mine(self):
        """
        Mine the unconfirmed transactions.

        Steps:
        - Check if there are unconfirmed transactions. If not, return False.
        - While there are transactions to be mined:
            - Select transactions up to max_transactions_per_block (if set).
            - Verify each transaction. If invalid, discard it.
            - Create a new Block with the selected transactions.
            - Perform proof of work to find a valid hash.
            - Add the block to the chain by calling add_block().
            - Remove the mined transactions from unconfirmed_transactions.
            - If max_transactions_per_block is None, break after mining one block.
        - Return the index of the last mined block.
        """
        if not self.unconfirmed_transactions:
            return False
        while self.unconfirmed_transactions:
            selected_transactions = self.unconfirmed_transactions[:self.max_transactions_per_block]
            for transaction in selected_transactions:
                if not transaction.is_valid():
                    selected_transactions.remove(transaction)
            block = Block(
                index=self.last_block.index + 1,
                transactions=selected_transactions,
                previous_hash=self.last_block.hash
            )
            proof = self.proof_of_work(block)
            self.add_block(block, proof)
            for transaction in selected_transactions:
                self.unconfirmed_transactions.remove(transaction)
            if self.max_transactions_per_block is None:
                break
        return self.last_block.index

    def is_chain_valid(self):
        """
        Validate the entire blockchain.

        Steps:
        - Iterate over the chain starting from the second block.
        - For each block:
            - Check if the block's hash matches its computed hash.
              If not, return False.
            - Check if the block's previous_hash matches the hash of the previous block.
              If not, return False.
            - Verify each transaction in the block by calling transaction.is_valid().
              If any transaction is invalid, return False.
        - If all checks pass, return True.
        """
        for i in range(1, len(self.chain)):
            block = self.chain[i]
            if block.hash != block.compute_hash():
                return False
            if block.previous_hash != self.chain[i-1].hash:
                return False
            for transaction in block.transactions:
                if not transaction.is_valid():
                    return False
        return True

    def is_transaction_in_block(self, transaction, block_index):
        # First, check if the block index is valid
        if block_index < 0 or block_index >= len(self.chain):
            return False

        # Retrieve the block by its index
        block = self.chain[block_index]

        # Use the `has_transaction` method of the Block class
        return block.has_transaction(transaction)

    def is_transaction_in_chain(self, transaction):
        # Check through every block in the chain
        for block in self.chain:
            if block.has_transaction(transaction):
                return True
        return False
