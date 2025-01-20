import os

import connexion
from flask import jsonify

SERVICE_NAME = 'coinsurfer_server'
DEFAULT_SPEC_DIR = "spec/src/main/_api.yml"

def create_app(debug: bool=True):
    """
    Create and configure the Connexion application.
    """
    # Resolve the specification path
    spec_file = resolve_spec_path(DEFAULT_SPEC_DIR)

    # Initialize the Connexion app
    connexion_app = connexion.FlaskApp(SERVICE_NAME, specification_dir=os.path.dirname(spec_file))

    # Add the OpenAPI specification
    connexion_app.add_api(
        os.path.basename(spec_file),
        strict_validation=True,
        validate_responses=True,
        pythonic_params=True,
    )
    connexion_app.app.debug=debug

    # Register a global error handler for unknown server errors
    @connexion_app.app.errorhandler(500)
    def handle_internal_server_error(e):
        """
        Handle uncaught internal server errors.
        :param e: The exception that was raised.
        :return: JSON response with error details.
        """
        response = {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred on the server.",
        }
        return jsonify(response), 500

    return connexion_app

def resolve_spec_path(spec_path: str) -> str:
    """
    Resolve the absolute path to the OpenAPI specification file.
    Ensures the file exists and handles runtime changes to the working directory.
    :param spec_path: Path to the OpenAPI spec file.
    :return: Absolute path to the spec file.
    :raises FileNotFoundError: If the file doesn't exist.
    """
    abs_path = os.path.abspath(spec_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"OpenAPI specification file not found at: {abs_path}")
    return abs_path
