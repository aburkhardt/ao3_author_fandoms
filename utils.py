# rate limiting tools go here
import time

def process_with_retry(func, total_items, batch_size_fn, max_retries=3, base_backoff=1, max_backoff=60):
    for attempt in range(1, max_retries + 1):
        backoff = base_backoff * 2**(attempt - 1)
        batch_size = batch_size_fn(attempt)
        num_batches = -(-total_items // batch_size)  # Equivalent to ceil(total_items / batch_size)

        print(f"Attempt {attempt}: Processing {total_items} items in {num_batches} batches with batch size {batch_size}")

        for batch_num in range(1, num_batches + 1):
            start_index = (batch_num - 1) * batch_size
            end_index = min(batch_num * batch_size, total_items)
            batch_items = list(range(start_index, end_index))

            try:
                func(batch_items)
                print(f"Batch {batch_num}/{num_batches} completed successfully")
            except Exception as e:
                print(f"Batch {batch_num}/{num_batches} failed with error: {e}")
                if attempt < max_retries:
                    print(f"Retrying in {backoff} seconds...")
                    time.sleep(backoff)
                else:
                    print("Maximum retries exceeded. Exiting...")
                    return

        print("All batches processed successfully!")
        return

# Example batch size function: doubling the batch size with each attempt
def exponential_batch_size(attempt):
    return 2**attempt

# Example function to process batch items
def process_items(batch_items):
    print(f"Processing items: {batch_items}")

# Example usage
total_items = 10
process_with_retry(process_items, total_items, exponential_batch_size)
