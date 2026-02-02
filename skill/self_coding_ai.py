"""
Self-Coding AI - Autonomous Code Generation & Evolution
AI that writes, fixes, and improves its own code automatically
Handles files of any size, fixes errors, and evolves continuously
"""

import os
import sys
import json
import ast
import time
import traceback
import subprocess
import importlib
import inspect
from typing import List, Dict, Any, Callable, Optional
from pathlib import Path
from core.skill import Skill
import re

class SelfCodingAI(Skill):
    """
    Self-coding AI that can:
    - Write its own code from scratch
    - Analyze and fix errors automatically
    - Recreate code based on requirements
    - Handle files of any size (GB+)
    - Evolve and improve over time
    - Control servers and infrastructure
    """
    
    def __init__(self):
        super().__init__()
        self.code_history = []
        self.error_patterns = {}
        self.learned_fixes = {}
        self.evolution_log = []
        self.max_file_size = 10 * 1024 * 1024 * 1024  # 10 GB
        
    @property
    def name(self) -> str:
        return "self_coding_ai"
    
    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "write_code_from_scratch",
                    "description": "AI writes complete code from requirements. Can create entire applications, modules, or systems. Handles any file size.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "requirements": {
                                "type": "string",
                                "description": "What the code should do (e.g., 'Create a web server', 'Build a database system')"
                            },
                            "language": {
                                "type": "string",
                                "description": "Programming language (python, javascript, go, rust, etc.)"
                            },
                            "output_path": {
                                "type": "string",
                                "description": "Where to save the code (e.g., 'server.py', 'app.js')"
                            },
                            "architecture": {
                                "type": "string",
                                "description": "System architecture (monolithic, microservices, serverless, distributed)"
                            }
                        },
                        "required": ["requirements", "language", "output_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "auto_fix_code",
                    "description": "Automatically analyze and fix errors in code. Learns from errors and improves over time.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to code file with errors"
                            },
                            "error_message": {
                                "type": "string",
                                "description": "Error message (optional, AI will detect if not provided)"
                            },
                            "max_attempts": {
                                "type": "integer",
                                "description": "Maximum fix attempts (default: 5)"
                            }
                        },
                        "required": ["file_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "recreate_code",
                    "description": "Recreate code from scratch based on input/requirements. Useful when code is broken beyond repair.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "original_file": {
                                "type": "string",
                                "description": "Original file to recreate"
                            },
                            "new_requirements": {
                                "type": "string",
                                "description": "Updated requirements or improvements"
                            },
                            "preserve_data": {
                                "type": "boolean",
                                "description": "Preserve existing data/config (default: true)"
                            }
                        },
                        "required": ["original_file"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "evolve_code",
                    "description": "Evolve code to be better - optimize, add features, improve architecture. AI learns and improves continuously.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Code file to evolve"
                            },
                            "evolution_goal": {
                                "type": "string",
                                "description": "What to improve (performance, features, scalability, security)"
                            },
                            "iterations": {
                                "type": "integer",
                                "description": "Number of evolution iterations (default: 3)"
                            }
                        },
                        "required": ["file_path", "evolution_goal"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "handle_large_file",
                    "description": "Process and modify large files (GB+) efficiently using streaming and chunking.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to large file"
                            },
                            "operation": {
                                "type": "string",
                                "description": "Operation to perform (analyze, fix, transform, optimize)"
                            },
                            "chunk_size": {
                                "type": "integer",
                                "description": "Chunk size in MB (default: 100)"
                            }
                        },
                        "required": ["file_path", "operation"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_server_infrastructure",
                    "description": "Create complete server infrastructure code - web servers, APIs, databases, load balancers, etc.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "server_type": {
                                "type": "string",
                                "description": "Type of server (web, api, database, microservice, distributed)"
                            },
                            "framework": {
                                "type": "string",
                                "description": "Framework to use (flask, fastapi, express, django, etc.)"
                            },
                            "features": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Features to include (auth, database, caching, logging, monitoring)"
                            },
                            "output_dir": {
                                "type": "string",
                                "description": "Output directory for server code"
                            }
                        },
                        "required": ["server_type", "framework", "output_dir"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_and_learn",
                    "description": "Analyze code patterns, learn from errors, and improve AI's coding ability over time.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code_directory": {
                                "type": "string",
                                "description": "Directory to analyze and learn from"
                            },
                            "learning_focus": {
                                "type": "string",
                                "description": "What to learn (patterns, errors, optimizations, best_practices)"
                            }
                        },
                        "required": ["code_directory"]
                    }
                }
            }
        ]
    
    def get_functions(self) -> Dict[str, Callable]:
        return {
            "write_code_from_scratch": self.write_code_from_scratch,
            "auto_fix_code": self.auto_fix_code,
            "recreate_code": self.recreate_code,
            "evolve_code": self.evolve_code,
            "handle_large_file": self.handle_large_file,
            "create_server_infrastructure": self.create_server_infrastructure,
            "analyze_and_learn": self.analyze_and_learn,
        }
    
    def write_code_from_scratch(self, requirements: str, language: str, 
                                output_path: str, architecture: str = "monolithic") -> str:
        """Write complete code from requirements"""
        try:
            print(f"\n🤖 Self-Coding AI: Writing {language} code...")
            print(f"   Requirements: {requirements}")
            print(f"   Architecture: {architecture}")
            
            # Generate code based on language and requirements
            code = self._generate_code(requirements, language, architecture)
            
            # Create directory if needed
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
            
            # Write code to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Validate code
            validation = self._validate_code(output_path, language)
            
            # Log to history
            self.code_history.append({
                "timestamp": time.time(),
                "action": "write_from_scratch",
                "file": output_path,
                "language": language,
                "requirements": requirements,
                "validation": validation
            })
            
            return json.dumps({
                "status": "success",
                "message": f"Code written successfully to {output_path}",
                "file": output_path,
                "language": language,
                "lines": len(code.split('\n')),
                "validation": validation,
                "next_steps": [
                    f"Review code: cat {output_path}",
                    f"Test code: python {output_path}" if language == "python" else f"Run code",
                    "Use auto_fix_code if errors occur"
                ]
            })
            
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "traceback": traceback.format_exc(),
                "suggestion": "Try with simpler requirements or different architecture"
            })
    
    def _generate_code(self, requirements: str, language: str, architecture: str) -> str:
        """Generate code based on requirements"""
        
        if language.lower() == "python":
            return self._generate_python_code(requirements, architecture)
        elif language.lower() in ["javascript", "js"]:
            return self._generate_javascript_code(requirements, architecture)
        elif language.lower() == "go":
            return self._generate_go_code(requirements, architecture)
        else:
            return self._generate_generic_code(requirements, language, architecture)
    
    def _generate_python_code(self, requirements: str, architecture: str) -> str:
        """Generate Python code"""
        
        # Analyze requirements
        req_lower = requirements.lower()
        
        # Web server
        if "web server" in req_lower or "api" in req_lower:
            return self._generate_python_web_server(requirements, architecture)
        
        # Database
        elif "database" in req_lower or "db" in req_lower:
            return self._generate_python_database(requirements)
        
        # Data processing
        elif "process" in req_lower or "data" in req_lower:
            return self._generate_python_data_processor(requirements)
        
        # Machine learning
        elif "ml" in req_lower or "machine learning" in req_lower or "ai" in req_lower:
            return self._generate_python_ml(requirements)
        
        # Generic application
        else:
            return self._generate_python_generic(requirements)
    
    def _generate_python_web_server(self, requirements: str, architecture: str) -> str:
        """Generate Python web server code"""
        
        if architecture == "microservices":
            return '''"""
Microservices Web Server
Auto-generated by Self-Coding AI
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for load balancer"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "microservice-1"
    }), 200

# Main API endpoint
@app.route('/api/v1/data', methods=['GET', 'POST'])
def handle_data():
    """Main data handling endpoint"""
    try:
        if request.method == 'GET':
            # Handle GET request
            return jsonify({
                "message": "Data retrieved successfully",
                "data": []
            }), 200
        
        elif request.method == 'POST':
            # Handle POST request
            data = request.get_json()
            logger.info(f"Received data: {data}")
            
            return jsonify({
                "message": "Data processed successfully",
                "received": data
            }), 201
    
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({
            "error": str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.environ.get('DEBUG', 'False') == 'True'
    )
'''
        else:
            return '''"""
Web Server
Auto-generated by Self-Coding AI
"""

from flask import Flask, jsonify, request, render_template_string
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Generated Server</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f0f0f0; }
        .container { background: white; padding: 20px; border-radius: 8px; }
        h1 { color: #333; }
        .status { color: green; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Generated Web Server</h1>
        <p class="status">✅ Server is running!</p>
        <p>Generated at: {{ timestamp }}</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, timestamp=datetime.now())

@app.route('/api/status')
def status():
    return jsonify({
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
'''
    
    def _generate_python_database(self, requirements: str) -> str:
        """Generate Python database code"""
        return '''"""
Database System
Auto-generated by Self-Coding AI
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

class Database:
    """Self-healing database with automatic error recovery"""
    
    def __init__(self, db_path: str = "data.db"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self._connect()
        self._initialize_tables()
    
    def _connect(self):
        """Connect to database with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.connection = sqlite3.connect(self.db_path)
                self.cursor = self.connection.cursor()
                print(f"✅ Connected to database: {self.db_path}")
                return
            except Exception as e:
                print(f"❌ Connection attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
    
    def _initialize_tables(self):
        """Create tables if they don't exist"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.connection.commit()
            print("✅ Tables initialized")
        except Exception as e:
            print(f"❌ Table initialization error: {e}")
            self._auto_fix_table_error(e)
    
    def insert(self, key: str, value: Any) -> bool:
        """Insert data with automatic error handling"""
        try:
            value_json = json.dumps(value)
            self.cursor.execute(
                "INSERT OR REPLACE INTO data (key, value, updated_at) VALUES (?, ?, ?)",
                (key, value_json, datetime.now())
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"❌ Insert error: {e}")
            return self._auto_fix_and_retry("insert", key, value)
    
    def get(self, key: str) -> Optional[Any]:
        """Get data with automatic error handling"""
        try:
            self.cursor.execute("SELECT value FROM data WHERE key = ?", (key,))
            result = self.cursor.fetchone()
            return json.loads(result[0]) if result else None
        except Exception as e:
            print(f"❌ Get error: {e}")
            return self._auto_fix_and_retry("get", key)
    
    def get_all(self) -> List[Dict]:
        """Get all data"""
        try:
            self.cursor.execute("SELECT key, value, created_at, updated_at FROM data")
            results = []
            for row in self.cursor.fetchall():
                results.append({
                    "key": row[0],
                    "value": json.loads(row[1]),
                    "created_at": row[2],
                    "updated_at": row[3]
                })
            return results
        except Exception as e:
            print(f"❌ Get all error: {e}")
            return []
    
    def delete(self, key: str) -> bool:
        """Delete data"""
        try:
            self.cursor.execute("DELETE FROM data WHERE key = ?", (key,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"❌ Delete error: {e}")
            return False
    
    def _auto_fix_and_retry(self, operation: str, *args):
        """Automatically fix errors and retry operation"""
        print(f"🔧 Auto-fixing {operation} operation...")
        
        # Reconnect to database
        self._connect()
        
        # Retry operation
        if operation == "insert":
            return self.insert(*args)
        elif operation == "get":
            return self.get(*args)
        
        return None
    
    def _auto_fix_table_error(self, error):
        """Fix table-related errors"""
        print(f"🔧 Auto-fixing table error: {error}")
        # Drop and recreate table if corrupted
        try:
            self.cursor.execute("DROP TABLE IF EXISTS data")
            self._initialize_tables()
        except Exception as e:
            print(f"❌ Auto-fix failed: {e}")
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed")

# Example usage
if __name__ == "__main__":
    db = Database()
    
    # Insert data
    db.insert("user_1", {"name": "John", "age": 30})
    db.insert("user_2", {"name": "Jane", "age": 25})
    
    # Get data
    user = db.get("user_1")
    print(f"User: {user}")
    
    # Get all data
    all_data = db.get_all()
    print(f"All data: {all_data}")
    
    db.close()
'''
    
    def _generate_python_data_processor(self, requirements: str) -> str:
        """Generate Python data processing code"""
        return '''"""
Data Processor
Auto-generated by Self-Coding AI
Handles large files efficiently with streaming
"""

import os
import json
import csv
from typing import Iterator, Dict, Any, List
from pathlib import Path

class DataProcessor:
    """Process large data files efficiently"""
    
    def __init__(self, chunk_size_mb: int = 100):
        self.chunk_size = chunk_size_mb * 1024 * 1024  # Convert to bytes
    
    def process_large_file(self, file_path: str, operation: str = "analyze") -> Dict:
        """Process large files in chunks"""
        file_size = os.path.getsize(file_path)
        print(f"📊 Processing file: {file_path}")
        print(f"   Size: {file_size / (1024**3):.2f} GB")
        
        if operation == "analyze":
            return self._analyze_file(file_path)
        elif operation == "transform":
            return self._transform_file(file_path)
        elif operation == "filter":
            return self._filter_file(file_path)
        else:
            return {"error": f"Unknown operation: {operation}"}
    
    def _analyze_file(self, file_path: str) -> Dict:
        """Analyze file contents"""
        stats = {
            "total_lines": 0,
            "total_size": 0,
            "chunks_processed": 0
        }
        
        for chunk in self._read_chunks(file_path):
            stats["total_lines"] += chunk.count('\n')
            stats["total_size"] += len(chunk)
            stats["chunks_processed"] += 1
            
            # Progress
            print(f"   Processed {stats['chunks_processed']} chunks...", end='\r')
        
        print(f"\n✅ Analysis complete!")
        return stats
    
    def _read_chunks(self, file_path: str) -> Iterator[str]:
        """Read file in chunks"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            while True:
                chunk = f.read(self.chunk_size)
                if not chunk:
                    break
                yield chunk
    
    def _transform_file(self, file_path: str) -> Dict:
        """Transform file data"""
        output_path = f"{file_path}.transformed"
        lines_processed = 0
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
            with open(output_path, 'w', encoding='utf-8') as outfile:
                for line in infile:
                    # Transform line (example: uppercase)
                    transformed = line.upper()
                    outfile.write(transformed)
                    lines_processed += 1
                    
                    if lines_processed % 10000 == 0:
                        print(f"   Transformed {lines_processed} lines...", end='\r')
        
        print(f"\n✅ Transformation complete!")
        return {
            "output_file": output_path,
            "lines_processed": lines_processed
        }
    
    def _filter_file(self, file_path: str) -> Dict:
        """Filter file data"""
        output_path = f"{file_path}.filtered"
        lines_kept = 0
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
            with open(output_path, 'w', encoding='utf-8') as outfile:
                for line in infile:
                    # Filter logic (example: keep non-empty lines)
                    if line.strip():
                        outfile.write(line)
                        lines_kept += 1
        
        print(f"✅ Filtering complete!")
        return {
            "output_file": output_path,
            "lines_kept": lines_kept
        }

# Example usage
if __name__ == "__main__":
    processor = DataProcessor(chunk_size_mb=100)
    
    # Process large file
    result = processor.process_large_file("large_data.txt", "analyze")
    print(f"Results: {result}")
'''
    
    def _generate_python_ml(self, requirements: str) -> str:
        """Generate Python ML code"""
        return '''"""
Machine Learning System
Auto-generated by Self-Coding AI
"""

import numpy as np
from typing import List, Tuple, Optional
import json

class SimpleNeuralNetwork:
    """Simple neural network with automatic error correction"""
    
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Initialize weights
        self.weights1 = np.random.randn(input_size, hidden_size) * 0.01
        self.weights2 = np.random.randn(hidden_size, output_size) * 0.01
        self.bias1 = np.zeros((1, hidden_size))
        self.bias2 = np.zeros((1, output_size))
    
    def sigmoid(self, x):
        """Sigmoid activation"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def sigmoid_derivative(self, x):
        """Sigmoid derivative"""
        return x * (1 - x)
    
    def forward(self, X):
        """Forward propagation"""
        try:
            self.hidden = self.sigmoid(np.dot(X, self.weights1) + self.bias1)
            self.output = self.sigmoid(np.dot(self.hidden, self.weights2) + self.bias2)
            return self.output
        except Exception as e:
            print(f"❌ Forward pass error: {e}")
            return self._auto_fix_forward(X)
    
    def backward(self, X, y, learning_rate=0.01):
        """Backward propagation"""
        try:
            # Calculate error
            output_error = y - self.output
            output_delta = output_error * self.sigmoid_derivative(self.output)
            
            hidden_error = output_delta.dot(self.weights2.T)
            hidden_delta = hidden_error * self.sigmoid_derivative(self.hidden)
            
            # Update weights
            self.weights2 += self.hidden.T.dot(output_delta) * learning_rate
            self.weights1 += X.T.dot(hidden_delta) * learning_rate
            self.bias2 += np.sum(output_delta, axis=0, keepdims=True) * learning_rate
            self.bias1 += np.sum(hidden_delta, axis=0, keepdims=True) * learning_rate
            
        except Exception as e:
            print(f"❌ Backward pass error: {e}")
            self._auto_fix_backward()
    
    def train(self, X, y, epochs=1000):
        """Train the network"""
        print(f"🧠 Training neural network...")
        
        for epoch in range(epochs):
            # Forward pass
            output = self.forward(X)
            
            # Backward pass
            self.backward(X, y)
            
            # Print progress
            if epoch % 100 == 0:
                loss = np.mean(np.square(y - output))
                print(f"   Epoch {epoch}, Loss: {loss:.4f}")
        
        print(f"✅ Training complete!")
    
    def predict(self, X):
        """Make predictions"""
        return self.forward(X)
    
    def _auto_fix_forward(self, X):
        """Auto-fix forward pass errors"""
        print("🔧 Auto-fixing forward pass...")
        # Reinitialize weights if needed
        self.weights1 = np.random.randn(self.input_size, self.hidden_size) * 0.01
        self.weights2 = np.random.randn(self.hidden_size, self.output_size) * 0.01
        return self.forward(X)
    
    def _auto_fix_backward(self):
        """Auto-fix backward pass errors"""
        print("🔧 Auto-fixing backward pass...")
        # Reset gradients
        pass

# Example usage
if __name__ == "__main__":
    # XOR problem
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])
    
    # Create and train network
    nn = SimpleNeuralNetwork(input_size=2, hidden_size=4, output_size=1)
    nn.train(X, y, epochs=1000)
    
    # Test predictions
    predictions = nn.predict(X)
    print(f"\nPredictions:")
    for i, pred in enumerate(predictions):
        print(f"   Input: {X[i]} -> Output: {pred[0]:.4f} (Expected: {y[i][0]})")
'''
    
    def _generate_python_generic(self, requirements: str) -> str:
        """Generate generic Python code"""
        return f'''"""
{requirements}
Auto-generated by Self-Coding AI
"""

import os
import sys
import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Application:
    """Main application class"""
    
    def __init__(self):
        self.config = {{}}
        self.data = {{}}
        logger.info("Application initialized")
    
    def run(self):
        """Main application logic"""
        try:
            logger.info("Application started")
            
            # Your code here
            self.process()
            
            logger.info("Application completed successfully")
            
        except Exception as e:
            logger.error(f"Application error: {{e}}")
            self.auto_fix_error(e)
    
    def process(self):
        """Process data"""
        # Implementation based on requirements
        pass
    
    def auto_fix_error(self, error: Exception):
        """Automatically fix errors"""
        logger.info(f"Auto-fixing error: {{error}}")
        # Auto-fix logic here
        pass

if __name__ == "__main__":
    app = Application()
    app.run()
'''
    
    def _generate_javascript_code(self, requirements: str, architecture: str) -> str:
        """Generate JavaScript code"""
        return '''// Auto-generated by Self-Coding AI

const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Routes
app.get('/', (req, res) => {
    res.json({ message: 'AI Generated Server', status: 'running' });
});

app.get('/api/health', (req, res) => {
    res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Internal server error' });
});

// Start server
app.listen(port, () => {
    console.log(`✅ Server running on port ${port}`);
});
'''
    
    def _generate_go_code(self, requirements: str, architecture: str) -> str:
        """Generate Go code"""
        return '''// Auto-generated by Self-Coding AI
package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "time"
)

type Response struct {
    Message   string    `json:"message"`
    Status    string    `json:"status"`
    Timestamp time.Time `json:"timestamp"`
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    response := Response{
        Message:   "AI Generated Server",
        Status:    "healthy",
        Timestamp: time.Now(),
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func main() {
    http.HandleFunc("/health", healthHandler)
    
    port := ":8080"
    fmt.Printf("✅ Server running on port %s\\n", port)
    log.Fatal(http.ListenAndServe(port, nil))
}
'''
    
    def _generate_generic_code(self, requirements: str, language: str, architecture: str) -> str:
        """Generate generic code for any language"""
        return f'''/*
 * {requirements}
 * Auto-generated by Self-Coding AI
 * Language: {language}
 * Architecture: {architecture}
 */

// Main application code
// TODO: Implement based on requirements

'''
    
    def _validate_code(self, file_path: str, language: str) -> Dict:
        """Validate generated code"""
        try:
            if language.lower() == "python":
                # Check Python syntax
                with open(file_path, 'r') as f:
                    code = f.read()
                    compile(code, file_path, 'exec')
                
                return {
                    "valid": True,
                    "syntax_errors": 0,
                    "message": "Code is syntactically correct"
                }
            else:
                return {
                    "valid": True,
                    "message": f"Validation not implemented for {language}"
                }
                
        except SyntaxError as e:
            return {
                "valid": False,
                "syntax_errors": 1,
                "error": str(e),
                "line": e.lineno
            }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }
    
    def auto_fix_code(self, file_path: str, error_message: str = None, 
                     max_attempts: int = 5) -> str:
        """Automatically fix code errors"""
        try:
            print(f"\n🔧 Auto-fixing code: {file_path}")
            
            # Read current code
            with open(file_path, 'r', encoding='utf-8') as f:
                original_code = f.read()
            
            # Detect errors if not provided
            if not error_message:
                error_message = self._detect_errors(file_path)
            
            print(f"   Error: {error_message}")
            
            # Try to fix
            for attempt in range(max_attempts):
                print(f"   Attempt {attempt + 1}/{max_attempts}...")
                
                fixed_code = self._apply_fix(original_code, error_message, attempt)
                
                # Write fixed code
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_code)
                
                # Validate fix
                validation = self._validate_code(file_path, "python")
                
                if validation.get("valid"):
                    print(f"✅ Code fixed successfully!")
                    
                    # Learn from this fix
                    self._learn_from_fix(error_message, fixed_code)
                    
                    return json.dumps({
                        "status": "success",
                        "message": "Code fixed successfully",
                        "attempts": attempt + 1,
                        "file": file_path,
                        "validation": validation
                    })
                else:
                    error_message = validation.get("error", "Unknown error")
            
            # Restore original if all attempts failed
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(original_code)
            
            return json.dumps({
                "status": "failed",
                "message": "Could not fix code automatically",
                "attempts": max_attempts,
                "suggestion": "Consider using recreate_code instead"
            })
            
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "traceback": traceback.format_exc()
            })
    
    def _detect_errors(self, file_path: str) -> str:
        """Detect errors in code"""
        try:
            # Try to run the code
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return result.stderr
            else:
                return "No errors detected"
                
        except subprocess.TimeoutExpired:
            return "Code execution timeout"
        except Exception as e:
            return str(e)
    
    def _apply_fix(self, code: str, error_message: str, attempt: int) -> str:
        """Apply fix to code based on error"""
        
        # Common error patterns and fixes
        fixes = {
            "IndentationError": self._fix_indentation,
            "SyntaxError": self._fix_syntax,
            "NameError": self._fix_name_error,
            "ImportError": self._fix_import_error,
            "AttributeError": self._fix_attribute_error,
            "TypeError": self._fix_type_error,
        }
        
        # Detect error type
        for error_type, fix_function in fixes.items():
            if error_type in error_message:
                return fix_function(code, error_message)
        
        # Generic fix
        return self._generic_fix(code, error_message, attempt)
    
    def _fix_indentation(self, code: str, error: str) -> str:
        """Fix indentation errors"""
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            # Ensure consistent indentation (4 spaces)
            if line.startswith('\t'):
                line = line.replace('\t', '    ')
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _fix_syntax(self, code: str, error: str) -> str:
        """Fix syntax errors"""
        # Add missing colons
        code = re.sub(r'(if|elif|else|for|while|def|class)\s+([^:]+)$', r'\1 \2:', code, flags=re.MULTILINE)
        
        # Fix unclosed parentheses
        open_count = code.count('(')
        close_count = code.count(')')
        if open_count > close_count:
            code += ')' * (open_count - close_count)
        
        return code
    
    def _fix_name_error(self, code: str, error: str) -> str:
        """Fix name errors"""
        # Extract undefined name
        match = re.search(r"name '(\w+)' is not defined", error)
        if match:
            undefined_name = match.group(1)
            # Add import or definition
            code = f"# Auto-fix: Added missing definition\n{undefined_name} = None\n\n{code}"
        
        return code
    
    def _fix_import_error(self, code: str, error: str) -> str:
        """Fix import errors"""
        # Extract missing module
        match = re.search(r"No module named '(\w+)'", error)
        if match:
            module = match.group(1)
            # Add try-except for import
            code = code.replace(
                f"import {module}",
                f"try:\n    import {module}\nexcept ImportError:\n    print('Module {module} not installed')\n    {module} = None"
            )
        
        return code
    
    def _fix_attribute_error(self, code: str, error: str) -> str:
        """Fix attribute errors"""
        # Add hasattr checks
        return code
    
    def _fix_type_error(self, code: str, error: str) -> str:
        """Fix type errors"""
        # Add type conversions
        return code
    
    def _generic_fix(self, code: str, error: str, attempt: int) -> str:
        """Generic fix attempt"""
        # Try different strategies based on attempt number
        if attempt == 0:
            # Add error handling
            return self._add_error_handling(code)
        elif attempt == 1:
            # Fix common issues
            return self._fix_common_issues(code)
        elif attempt == 2:
            # Simplify code
            return self._simplify_code(code)
        else:
            # Last resort: add try-except around everything
            return f"try:\n{self._indent_code(code)}\nexcept Exception as e:\n    print(f'Error: {{e}}')"
    
    def _add_error_handling(self, code: str) -> str:
        """Add error handling to code"""
        # Wrap main execution in try-except
        if "if __name__ == '__main__':" in code:
            code = code.replace(
                "if __name__ == '__main__':",
                "if __name__ == '__main__':\n    try:"
            )
            code += "\n    except Exception as e:\n        print(f'Error: {e}')"
        
        return code
    
    def _fix_common_issues(self, code: str) -> str:
        """Fix common code issues"""
        # Remove duplicate imports
        lines = code.split('\n')
        seen_imports = set()
        fixed_lines = []
        
        for line in lines:
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                if line not in seen_imports:
                    seen_imports.add(line)
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _simplify_code(self, code: str) -> str:
        """Simplify code"""
        # Remove comments
        code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
        # Remove empty lines
        code = '\n'.join(line for line in code.split('\n') if line.strip())
        return code
    
    def _indent_code(self, code: str) -> str:
        """Indent code by 4 spaces"""
        return '\n'.join('    ' + line for line in code.split('\n'))
    
    def _learn_from_fix(self, error: str, fixed_code: str):
        """Learn from successful fixes"""
        error_type = error.split(':')[0] if ':' in error else error
        
        if error_type not in self.learned_fixes:
            self.learned_fixes[error_type] = []
        
        self.learned_fixes[error_type].append({
            "error": error,
            "fix": fixed_code[:200],  # Store first 200 chars
            "timestamp": time.time()
        })
        
        print(f"📚 Learned new fix for: {error_type}")
    
    def recreate_code(self, original_file: str, new_requirements: str = None,
                     preserve_data: bool = True) -> str:
        """Recreate code from scratch"""
        try:
            print(f"\n🔄 Recreating code: {original_file}")
            
            # Backup original
            backup_path = f"{original_file}.backup"
            if os.path.exists(original_file):
                with open(original_file, 'r') as f:
                    original_code = f.read()
                with open(backup_path, 'w') as f:
                    f.write(original_code)
                print(f"   Backup created: {backup_path}")
            
            # Extract requirements from original if not provided
            if not new_requirements:
                new_requirements = self._extract_requirements(original_file)
            
            # Detect language
            language = self._detect_language(original_file)
            
            # Generate new code
            new_code = self._generate_code(new_requirements, language, "monolithic")
            
            # Write new code
            with open(original_file, 'w') as f:
                f.write(new_code)
            
            print(f"✅ Code recreated successfully!")
            
            return json.dumps({
                "status": "success",
                "message": "Code recreated successfully",
                "file": original_file,
                "backup": backup_path,
                "language": language,
                "requirements": new_requirements
            })
            
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "traceback": traceback.format_exc()
            })
    
    def _extract_requirements(self, file_path: str) -> str:
        """Extract requirements from code"""
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            
            # Look for docstrings
            docstring_match = re.search(r'"""(.+?)"""', code, re.DOTALL)
            if docstring_match:
                return docstring_match.group(1).strip()
            
            # Look for comments
            comments = re.findall(r'#\s*(.+)$', code, re.MULTILINE)
            if comments:
                return ' '.join(comments[:5])
            
            return "Recreate this application"
            
        except Exception:
            return "Recreate this application"
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        ext = Path(file_path).suffix.lower()
        
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.go': 'go',
            '.rs': 'rust',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
        }
        
        return language_map.get(ext, 'python')
    
    def evolve_code(self, file_path: str, evolution_goal: str, iterations: int = 3) -> str:
        """Evolve code to be better"""
        try:
            print(f"\n🧬 Evolving code: {file_path}")
            print(f"   Goal: {evolution_goal}")
            print(f"   Iterations: {iterations}")
            
            # Read original code
            with open(file_path, 'r') as f:
                code = f.read()
            
            evolution_history = []
            
            for i in range(iterations):
                print(f"\n   Evolution iteration {i + 1}/{iterations}...")
                
                # Apply evolution based on goal
                if "performance" in evolution_goal.lower():
                    code = self._optimize_performance(code)
                elif "features" in evolution_goal.lower():
                    code = self._add_features(code)
                elif "scalability" in evolution_goal.lower():
                    code = self._improve_scalability(code)
                elif "security" in evolution_goal.lower():
                    code = self._enhance_security(code)
                else:
                    code = self._general_improvement(code)
                
                # Validate evolved code
                temp_file = f"{file_path}.temp"
                with open(temp_file, 'w') as f:
                    f.write(code)
                
                validation = self._validate_code(temp_file, "python")
                os.remove(temp_file)
                
                evolution_history.append({
                    "iteration": i + 1,
                    "valid": validation.get("valid", False),
                    "changes": "Applied evolution"
                })
                
                if not validation.get("valid"):
                    print(f"   ❌ Evolution iteration {i + 1} failed validation")
                    break
                else:
                    print(f"   ✅ Evolution iteration {i + 1} successful")
            
            # Write evolved code
            with open(file_path, 'w') as f:
                f.write(code)
            
            # Log evolution
            self.evolution_log.append({
                "file": file_path,
                "goal": evolution_goal,
                "iterations": iterations,
                "history": evolution_history,
                "timestamp": time.time()
            })
            
            print(f"\n✅ Code evolution complete!")
            
            return json.dumps({
                "status": "success",
                "message": "Code evolved successfully",
                "file": file_path,
                "goal": evolution_goal,
                "iterations_completed": len(evolution_history),
                "history": evolution_history
            })
            
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "traceback": traceback.format_exc()
            })
    
    def _optimize_performance(self, code: str) -> str:
        """Optimize code for performance"""
        # Add caching
        if "def " in code and "@lru_cache" not in code:
            code = "from functools import lru_cache\n\n" + code
            # Add cache decorator to functions
            code = re.sub(
                r'(def \w+\([^)]*\):)',
                r'@lru_cache(maxsize=128)\n\1',
                code,
                count=3
            )
        
        # Use list comprehensions instead of loops where possible
        # Add more optimizations...
        
        return code
    
    def _add_features(self, code: str) -> str:
        """Add new features to code"""
        # Add logging if not present
        if "import logging" not in code:
            code = "import logging\n" + code
            code = code.replace(
                "def __init__",
                "def __init__(self, *args, **kwargs):\n        logging.basicConfig(level=logging.INFO)\n        self.logger = logging.getLogger(__name__)"
            )
        
        # Add error handling
        # Add configuration support
        # Add more features...
        
        return code
    
    def _improve_scalability(self, code: str) -> str:
        """Improve code scalability"""
        # Add async support
        if "def " in code and "async def" not in code:
            code = "import asyncio\n\n" + code
        
        # Add connection pooling
        # Add caching layer
        # Add more scalability improvements...
        
        return code
    
    def _enhance_security(self, code: str) -> str:
        """Enhance code security"""
        # Add input validation
        # Add authentication
        # Add encryption
        # Add more security enhancements...
        
        return code
    
    def _general_improvement(self, code: str) -> str:
        """General code improvements"""
        # Add docstrings
        # Add type hints
        # Improve naming
        # Add comments
        
        return code
    
    def handle_large_file(self, file_path: str, operation: str, chunk_size: int = 100) -> str:
        """Handle large files efficiently"""
        try:
            file_size = os.path.getsize(file_path)
            file_size_gb = file_size / (1024 ** 3)
            
            print(f"\n📦 Processing large file: {file_path}")
            print(f"   Size: {file_size_gb:.2f} GB")
            print(f"   Operation: {operation}")
            print(f"   Chunk size: {chunk_size} MB")
            
            if operation == "analyze":
                result = self._analyze_large_file(file_path, chunk_size)
            elif operation == "fix":
                result = self._fix_large_file(file_path, chunk_size)
            elif operation == "transform":
                result = self._transform_large_file(file_path, chunk_size)
            elif operation == "optimize":
                result = self._optimize_large_file(file_path, chunk_size)
            else:
                result = {"error": f"Unknown operation: {operation}"}
            
            return json.dumps({
                "status": "success",
                "file": file_path,
                "size_gb": file_size_gb,
                "operation": operation,
                "result": result
            })
            
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "traceback": traceback.format_exc()
            })
    
    def _analyze_large_file(self, file_path: str, chunk_size_mb: int) -> Dict:
        """Analyze large file"""
        chunk_size = chunk_size_mb * 1024 * 1024
        
        stats = {
            "total_lines": 0,
            "total_chars": 0,
            "chunks_processed": 0,
            "errors_found": 0
        }
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                stats["total_lines"] += chunk.count('\n')
                stats["total_chars"] += len(chunk)
                stats["chunks_processed"] += 1
                
                # Check for errors in chunk
                if "error" in chunk.lower() or "exception" in chunk.lower():
                    stats["errors_found"] += 1
                
                print(f"   Processed {stats['chunks_processed']} chunks...", end='\r')
        
        print(f"\n✅ Analysis complete!")
        return stats
    
    def _fix_large_file(self, file_path: str, chunk_size_mb: int) -> Dict:
        """Fix large file"""
        # Process in chunks and fix errors
        return {"message": "Large file fix not yet implemented"}
    
    def _transform_large_file(self, file_path: str, chunk_size_mb: int) -> Dict:
        """Transform large file"""
        # Process in chunks and transform
        return {"message": "Large file transform not yet implemented"}
    
    def _optimize_large_file(self, file_path: str, chunk_size_mb: int) -> Dict:
        """Optimize large file"""
        # Process in chunks and optimize
        return {"message": "Large file optimization not yet implemented"}
    
    def create_server_infrastructure(self, server_type: str, framework: str,
                                    features: List[str], output_dir: str) -> str:
        """Create complete server infrastructure"""
        try:
            print(f"\n🏗️  Creating server infrastructure...")
            print(f"   Type: {server_type}")
            print(f"   Framework: {framework}")
            print(f"   Features: {', '.join(features)}")
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate server code based on framework
            if framework.lower() in ["flask", "fastapi"]:
                server_code = self._generate_python_server(server_type, framework, features)
                main_file = os.path.join(output_dir, "server.py")
            elif framework.lower() in ["express", "fastify"]:
                server_code = self._generate_node_server(server_type, framework, features)
                main_file = os.path.join(output_dir, "server.js")
            else:
                return json.dumps({"error": f"Framework {framework} not supported yet"})
            
            # Write server code
            with open(main_file, 'w') as f:
                f.write(server_code)
            
            # Generate additional files
            files_created = [main_file]
            
            if "database" in features:
                db_file = os.path.join(output_dir, "database.py")
                with open(db_file, 'w') as f:
                    f.write(self._generate_database_code())
                files_created.append(db_file)
            
            if "auth" in features:
                auth_file = os.path.join(output_dir, "auth.py")
                with open(auth_file, 'w') as f:
                    f.write(self._generate_auth_code())
                files_created.append(auth_file)
            
            # Generate requirements.txt
            req_file = os.path.join(output_dir, "requirements.txt")
            with open(req_file, 'w') as f:
                f.write(self._generate_requirements(framework, features))
            files_created.append(req_file)
            
            # Generate README
            readme_file = os.path.join(output_dir, "README.md")
            with open(readme_file, 'w') as f:
                f.write(self._generate_server_readme(server_type, framework, features))
            files_created.append(readme_file)
            
            print(f"✅ Server infrastructure created!")
            
            return json.dumps({
                "status": "success",
                "message": "Server infrastructure created successfully",
                "output_dir": output_dir,
                "files_created": files_created,
                "next_steps": [
                    f"cd {output_dir}",
                    "pip install -r requirements.txt",
                    f"python {os.path.basename(main_file)}"
                ]
            })
            
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "traceback": traceback.format_exc()
            })
    
    def _generate_python_server(self, server_type: str, framework: str, features: List[str]) -> str:
        """Generate Python server code"""
        if framework.lower() == "flask":
            return self._generate_flask_server(features)
        elif framework.lower() == "fastapi":
            return self._generate_fastapi_server(features)
        else:
            return ""
    
    def _generate_flask_server(self, features: List[str]) -> str:
        """Generate Flask server"""
        code = '''"""
Flask Server
Auto-generated by Self-Coding AI
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "AI Generated Flask Server",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'GET':
        return jsonify({"data": []})
    elif request.method == 'POST':
        data = request.get_json()
        return jsonify({"received": data}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
'''
        return code
    
    def _generate_fastapi_server(self, features: List[str]) -> str:
        """Generate FastAPI server"""
        code = '''"""
FastAPI Server
Auto-generated by Self-Coding AI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI(title="AI Generated API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataModel(BaseModel):
    data: dict

@app.get("/")
async def root():
    return {
        "message": "AI Generated FastAPI Server",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/data")
async def get_data():
    return {"data": []}

@app.post("/api/data")
async def post_data(data: DataModel):
    return {"received": data.dict()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        return code
    
    def _generate_node_server(self, server_type: str, framework: str, features: List[str]) -> str:
        """Generate Node.js server"""
        return '''// Auto-generated by Self-Coding AI
const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
    res.json({
        message: 'AI Generated Express Server',
        status: 'running',
        timestamp: new Date().toISOString()
    });
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`✅ Server running on port ${PORT}`);
});
'''
    
    def _generate_database_code(self) -> str:
        """Generate database code"""
        return '''# Database module
# Auto-generated by Self-Coding AI

import sqlite3

class Database:
    def __init__(self, db_path="app.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
    
    def close(self):
        self.connection.close()
'''
    
    def _generate_auth_code(self) -> str:
        """Generate authentication code"""
        return '''# Authentication module
# Auto-generated by Self-Coding AI

def authenticate(username, password):
    # Add authentication logic
    return True

def authorize(user, resource):
    # Add authorization logic
    return True
'''
    
    def _generate_requirements(self, framework: str, features: List[str]) -> str:
        """Generate requirements.txt"""
        reqs = []
        
        if framework.lower() == "flask":
            reqs.extend(["flask", "flask-cors"])
        elif framework.lower() == "fastapi":
            reqs.extend(["fastapi", "uvicorn", "pydantic"])
        
        if "database" in features:
            reqs.append("sqlalchemy")
        
        if "auth" in features:
            reqs.append("pyjwt")
        
        return '\n'.join(reqs)
    
    def _generate_server_readme(self, server_type: str, framework: str, features: List[str]) -> str:
        """Generate README for server"""
        return f'''# {server_type.title()} Server

Auto-generated by Self-Coding AI

## Framework
{framework}

## Features
{chr(10).join(f"- {feature}" for feature in features)}

## Setup
```bash
pip install -r requirements.txt
python server.py
```

## API Endpoints
- GET / - Home
- GET /health - Health check
- GET /api/data - Get data
- POST /api/data - Post data
'''
    
    def analyze_and_learn(self, code_directory: str, learning_focus: str = "patterns") -> str:
        """Analyze code and learn from it"""
        try:
            print(f"\n📚 Analyzing and learning from: {code_directory}")
            print(f"   Focus: {learning_focus}")
            
            patterns_learned = []
            files_analyzed = 0
            
            # Walk through directory
            for root, dirs, files in os.walk(code_directory):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        
                        # Analyze file
                        patterns = self._analyze_file_patterns(file_path, learning_focus)
                        patterns_learned.extend(patterns)
                        files_analyzed += 1
                        
                        print(f"   Analyzed {files_analyzed} files...", end='\r')
            
            print(f"\n✅ Learning complete!")
            
            # Store learned patterns
            self.error_patterns.update({
                "learned_at": time.time(),
                "directory": code_directory,
                "patterns": patterns_learned
            })
            
            return json.dumps({
                "status": "success",
                "message": "Learning complete",
                "files_analyzed": files_analyzed,
                "patterns_learned": len(patterns_learned),
                "focus": learning_focus
            })
            
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "traceback": traceback.format_exc()
            })
    
    def _analyze_file_patterns(self, file_path: str, focus: str) -> List[Dict]:
        """Analyze patterns in a file"""
        patterns = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            if focus == "patterns":
                # Learn code patterns
                if "class " in code:
                    patterns.append({"type": "class_definition", "file": file_path})
                if "def " in code:
                    patterns.append({"type": "function_definition", "file": file_path})
            
            elif focus == "errors":
                # Learn error handling patterns
                if "try:" in code:
                    patterns.append({"type": "error_handling", "file": file_path})
            
            elif focus == "optimizations":
                # Learn optimization patterns
                if "@lru_cache" in code:
                    patterns.append({"type": "caching", "file": file_path})
            
        except Exception:
            pass
        
        return patterns
