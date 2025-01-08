
# Initialize the converter with default settings
from src.fast_html2md.converter import HTMLToMarkdown


converter = HTMLToMarkdown()

# Example HTML (from test.html)
html = """
<!DOCTYPE html>
<html>
<body>
  <h1 id="title" data-updated="20201101">Hi there</h1>
  <div class="post">
    Lorem Ipsum is simply dummy text of the printing and typesetting industry.
  </div>
  <div class="post">
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
  </div>
</body>
</html>
"""

# Convert HTML to Markdown
markdown = converter.convert(html)

# Count tokens in the result
token_count = converter.count_tokens(markdown)

# Calculate cost
cost = converter.compute_cost(token_count)

print(f"Converted Markdown: {markdown}")
print(f"Token count: {token_count}")
print(f"Estimated cost: ${cost:.6f}")
