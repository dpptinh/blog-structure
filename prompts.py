summary_prompt = """

## Tweets content: \n
{content}

## Task:
Please analyze the provided tweets and create a comprehensive summary that captures all key information and highlights. Follow these guidelines:

## Content summarization
2. Key Information Retention
   - Preserve all URLs and external links
   - Maintain exact numerical data and statistics
   - Keep all comparison tables or data visualizations mentioned
   - Retain specific metrics, percentages, and quantitative information

3. Highlight Emphasis
   - Bold (**) key phrases or critical points
   - Use bullet points for listing multiple related items
   - Create sections for different themes or topics if applicable
   
4. Main Themes
   - Identify and categorize recurring topics
   - Note any evolving narratives across multiple tweets

5. Data Presentation
   - Present numerical data in an organized format
   - If multiple statistics are present, consider creating a small table

6. Reference Tracking
   - Note any mentioned individuals, organizations, or events
   - Preserve context for any referenced external content

## Special Considerations
    - Maintain any industry-specific terminology
    - Preserve the tone and voice of the original tweets

## Output Format:
    - Provide only the detailed blog post in Vietnamese in MARKDOWN format and nothing else. 
    - Do not add any other explanations or notes.
    - Do not include ```markdown and ``` in the output.

"""
# Tweet Entity Extraction Prompt


information_extraction_prompt = """
## Tweet content: \n
{content}

## Task:
Extract entities and information from the provided tweet into a structured JSON format. The output should be a valid JSON object with dynamic keys based on the tweet content.

## Instructions
   
2. Identify and extract the types of entities and entities (if present):
   - Cryptocurrencies/tokens
   - Events (hackathons, conferences, AMAs, etc.)
   - Projects or protocols
   - Dates and times
   - Numerical figures (prices, percentages, etc.)
   - People or organizations
   - Technology terms
   - Blockchain networks
   - .
   - .
   - .
   - .
   
3. Output Format:
    {{"keyName1": ["entity1", "entity2"], "keyName2": ["entity3", "entity4"],...}}

4. Formatting Rules:
   - Output must be a single, valid JSON object
   - Use dynamic keys based on found information types
   - All values must be arrays of strings
   - Remove any duplicate entries in arrays
   - Preserve exact formatting of extracted entities
   - Do not include explanations or additional text outside the JSON
   - Only include keys for information types that are actually found in the tweet. The JSON should be the only output, with no additional text or explanation.
   - Do not include ```json and ``` in the output.
"""
