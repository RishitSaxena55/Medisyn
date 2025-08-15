from chroma import vector_store


def store_docs(all_splits):
    batch_size = 5000

    # Create an empty list to store all document IDs
    all_document_ids = []

    # Loop through the documents in batches
    for i in range(0, len(all_splits), batch_size):
        # Get the current batch of documents
        batch = all_splits[i:i + batch_size]

        # Add the batch to the vector store
        document_ids = vector_store.add_documents(documents=batch)

        # Add the new document IDs to the main list
        all_document_ids.extend(document_ids)

    print(all_document_ids[:3])

    return all_document_ids
