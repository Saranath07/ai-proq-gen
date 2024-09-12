from jinja2 import Environment, Template

# Define a custom zip filter
def zip_filter(a, b):
    return zip(a, b)

# Create a Jinja2 environment and add the custom filter
env = Environment()
env.filters['zip'] = zip_filter

# Define the template using the custom filter
output_template = env.from_string('''
{% set list1 = output_json['actual_output'] %}
{% set list2 = output_json['expected_output'] %}

{% for item1, item2 in list1 | zip(list2) %}
    ### Actual Output {{loop.index}}
    {% if item1 == item2 %}
        Passed ✅
    {% else %}
        Expected: {{ item2 }}, but got: {{ item1 }} ❌
    {% endif %}
{% endfor %}
''')

# Sample data to test the template
output_json = {
    'actual_output': ['apple', 'banana', 'grape'],
    'expected_output': ['apple', 'banana', 'cherry']
}

# Render the template with the sample data
rendered_output = output_template.render(output_json=output_json)

# Print the rendered output
print(rendered_output)
