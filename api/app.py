from flask import Flask, request, send_file, jsonify
import subprocess
import uuid
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/generate-report', methods=['POST'])

def generate_report():
    try:
        req = request.get_json()
        data_file = req.get('data_file') or "data/pid_002_data.csv" # Whatever your data being used is called
        config_file = req.get('config_file') or "config/sample_config.yml"

        job_id = str(uuid.uuid4())
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)

        output_filename = f"report_{job_id}.pdf"

        qmd_path = Path(__file__).parent.parent / "templates" / "1pager_template.qmd"

        cmd = [
            "quarto", "render", str(qmd_path),
            "--to", "pdf",
            "--output", output_filename,
            "--execute"
        ]

        result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=str(output_dir))

        return send_file(str(output_dir / output_filename), as_attachment=True)

    except subprocess.CalledProcessError as e:
        error_message = f"Quarto render failed:\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
        return jsonify({"error": error_message}), 500
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
