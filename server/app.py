from flask import Flask, request, jsonify
import traceback
import sys

app = Flask(__name__)

@app.route('/run_code', methods=['POST'])
def run_code():
    code = request.json.get('code', '')

    try:
        # Create a restricted environment for executing the code
        local_namespace = {}
        compiled_code = compile(code, '<string>', 'exec')
        exec(compiled_code, {"__builtins__": None}, local_namespace)
    except Exception as e:
        # Catch any exception and format the traceback
        exc_type, exc_value, exc_tb = sys.exc_info()
        formatted_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': formatted_traceback
        }), 400

    return jsonify({
        'success': True,
        'message': 'Code executed successfully.',
        'namespace': local_namespace  # Optionally return variables from execution
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
