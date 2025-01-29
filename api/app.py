from flask import Flask
from flask_graphql import GraphQLView
from schema import schema
from models import init_db

app = Flask(__name__)

# Initialize the database
init_db(app)

# Set up the GraphQL endpoint
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable GraphiQL for testing
    )
)

if __name__ == "__main__":
    app.run(debug=True)
