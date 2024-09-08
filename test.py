from neo4j import GraphDatabase

# Initialize Neo4j driver (assuming you've set up the connection already)
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

# Function to extract relevant nodes using similarity with queryNodeEmbedding and nodeEmbedding
def extract_relevant_nodes(query_embedding):
    with driver.session() as session:
        # Search for nodes with embeddings similar to the query
        result = session.run("""
        MATCH (n)
        WITH n, gds.alpha.similarity.cosine($query_embedding, n.Embeddingnode) AS similarity
        WHERE similarity > 0.8
        RETURN n, similarity
        ORDER BY similarity DESC
        LIMIT 10
        """, query_embedding=query_embedding)
        
        # Collect nodes and their embeddings
        relevant_nodes = [record['n'] for record in result]
    return relevant_nodes

# Function to extract relevant adjacent nodes using similarity with description embeddings
def extract_relevant_adjacent_nodes(relevant_nodes, query_embedding):
    with driver.session() as session:
        node_ids = [n.id for n in relevant_nodes]  # Get the node IDs
        
        # Find adjacent nodes based on description embedding similarity
        result = session.run("""
        MATCH (n)-[r:relation]->(adjacent)
        WHERE id(n) IN $node_ids
        WITH adjacent, gds.alpha.similarity.cosine($query_embedding, adjacent.Embeddingdescription) AS description_similarity
        WHERE description_similarity > 0.8
        RETURN adjacent, description_similarity
        ORDER BY description_similarity DESC
        LIMIT 10
        """, node_ids=node_ids, query_embedding=query_embedding)
        
        # Collect adjacent nodes
        adjacent_nodes = [record['adjacent'] for record in result]
    return adjacent_nodes

# Function to extract nodes using similarity with queryEmbedding and descriptionEmbedding
def extract_nodes_with_description_similarity(query_embedding):
    with driver.session() as session:
        # Search for nodes whose description embeddings are similar to the query
        result = session.run("""
        MATCH (n)
        WITH n, gds.alpha.similarity.cosine($query_embedding, n.Embeddingdescription) AS description_similarity
        WHERE description_similarity > 0.8
        RETURN n, description_similarity
        ORDER BY description_similarity DESC
        LIMIT 10
        """, query_embedding=query_embedding)
        
        # Collect nodes
        relevant_description_nodes = [record['n'] for record in result]
    return relevant_description_nodes

# Function to remove duplicate nodes
def remove_duplicates(nodes):
    # Remove duplicate nodes based on their ID
    unique_nodes = {node.id: node for node in nodes}.values()
    return list(unique_nodes)

# Function to answer the user query by combining nodes, descriptions, and relations
def answer_user_query(relevant_nodes, query_embedding):
    with driver.session() as session:
        node_ids = [n.id for n in relevant_nodes]
        
        # Get relations between final relevant nodes and adjacent nodes
        result = session.run("""
        MATCH (n)-[r:relation]->(adjacent)
        WHERE id(n) IN $node_ids
        RETURN n, adjacent, r
        """, node_ids=node_ids)
        
        # Collect the final results (nodes and relationships)
        final_results = []
        for record in result:
            node = record['n']
            adjacent_node = record['adjacent']
            relation = record['r']
            final_results.append({
                "node": node,
                "adjacent_node": adjacent_node,
                "relation": relation
            })
            
        return final_results

# Main function to execute the search and return the answer
def execute_query(user_query):
    # Step 1: Extract entities from user query (not implemented)
    entities = get_entities(user_query)
    
    # Step 2: Generate query embedding
    query_embedding = get_embedding(user_query)
    
    # Step 3: Extract relevant nodes based on similarity of embeddings
    relevant_nodes = extract_relevant_nodes(query_embedding)
    
    # Step 4: Extract relevant adjacent nodes based on description similarity
    adjacent_nodes = extract_relevant_adjacent_nodes(relevant_nodes, query_embedding)
    
    # Step 5: Extract relevant nodes using similarity with description embeddings
    description_nodes = extract_nodes_with_description_similarity(query_embedding)
    
    # Step 6: Combine all nodes and remove duplicates
    all_nodes = relevant_nodes + adjacent_nodes + description_nodes
    unique_nodes = remove_duplicates(all_nodes)
    
    # Step 7: Use final available nodes and relationships to answer the query
    final_answer = answer_user_query(unique_nodes, query_embedding)
    
    return final_answer

# Example user query execution
user_query = "Your user query here"
result = execute_query(user_query)
print(result)  # Output the final response
