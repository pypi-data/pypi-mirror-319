
import json
import pickle
import os
import subprocess

from datetime import datetime
from jinja2 import Template


class ArtifactManager:
    def __init__(self, experiment_name, cache_dir=None):
        """
        Initialize the ArtifactManager for managing artifacts during experiments.

        Args:
            experiment_name (str): Name of the experiment.
            cache_dir (str, optional): Directory to save the artifacts. Defaults to '~/.cache/torchevent'.
        """
        self.experiment_name = experiment_name
        self.cache_dir = cache_dir or os.path.expanduser("~/.cache/torchevent")
        self.artifacts = {}
        os.makedirs(self.cache_dir, exist_ok=True)

    def __setitem__(self, key, value):
        """
        Add or update an artifact using dictionary-like syntax.

        Args:
            key (str): Key for the artifact.
            value: Value of the artifact.
        """
        self.artifacts[key] = value

    def __getitem__(self, key):
        """
        Retrieve an artifact using dictionary-like syntax.

        Args:
            key (str): Key of the artifact to retrieve.

        Returns:
            The value of the requested artifact.
        """
        return self.artifacts.get(key, None)

    def __delitem__(self, key):
        """
        Remove an artifact using dictionary-like syntax.

        Args:
            key (str): Key of the artifact to delete.
        """
        if key in self.artifacts:
            del self.artifacts[key]

    def __contains__(self, key):
        """
        Check if an artifact exists using the `in` keyword.

        Args:
            key (str): Key of the artifact to check.

        Returns:
            bool: True if the artifact exists, False otherwise.
        """
        return key in self.artifacts

    def save(self):
        """
        Save all artifacts to a pickle file with a unique name.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.experiment_name}_{timestamp}.pkl"
        save_path = os.path.join(self.cache_dir, filename)

        try:
            with open(save_path, "wb") as f:
                pickle.dump(self.artifacts, f)
            print(f"Artifacts saved successfully to {save_path}")
        except Exception as e:
            print(f"Error while saving artifacts: {e}")

    def load(self, filename):
        """
        Load artifacts from a specified pickle file.

        Args:
            filename (str): Name of the file to load the artifacts from.

        Returns:
            dict: The loaded artifacts.
        """
        load_path = os.path.join(self.cache_dir, filename)
        
        if not os.path.exists(load_path):
            raise FileNotFoundError(f"Artifacts file not found at {load_path}")

        try:
            with open(load_path, "rb") as f:
                self.artifacts = pickle.load(f)
            print(f"Artifacts loaded successfully from {load_path}")
            return self.artifacts
        except Exception as e:
            print(f"Error while loading artifacts: {e}")
            return None

    def generate_report(self):
        """
        Generate a LaTeX report and compile it into a PDF.
        """
        template = Template(r"""
        \documentclass{article}
        \usepackage{graphicx}
        \usepackage{hyperref}

        \title{Experiment Report: {{ experiment_name }}}
        \author{}
        \date{\today}

        \begin{document}

        \maketitle

        \section*{Summary}
        \begin{verbatim}
        {{ summary }}
        \end{verbatim}

        \section*{Training Recipes}
        \begin{verbatim}
        {{ train_recipes }}
        \end{verbatim}

        \section*{Learning Curves}
        \begin{verbatim}
        {{ learning_curves }}
        \end{verbatim}

        \section*{Evaluation Metrics}
        \begin{verbatim}
        {{ eval_metric }}
        \end{verbatim}

        \end{document}
        """
        )

        report_data = {
            "experiment_name": self.experiment_name,
            "summary": json.dumps(self.artifacts.get('summary', {}), indent=4),
            "train_recipes": json.dumps(self.artifacts.get('train_recipes', {}), indent=4),
            "learning_curves": json.dumps(self.artifacts.get('learning_curves', []), indent=4),
            "eval_metric": json.dumps(self.artifacts.get('eval_metric', {}), indent=4),
        }

        latex_content = template.render(report_data)
        tex_file_path = os.path.join(self.cache_dir, f"{self.experiment_name}_report.tex")
        with open(tex_file_path, "w") as f:
            f.write(latex_content)

        print(f"LaTeX report generated at {tex_file_path}")

        # Compile LaTeX to PDF
        try:
            subprocess.run(["pdflatex", "-output-directory", self.cache_dir, tex_file_path], check=True)
            print(f"PDF report generated at {os.path.join(self.cache_dir, f'{self.experiment_name}_report.pdf')}")
        except subprocess.CalledProcessError as e:
            print(f"Error compiling LaTeX to PDF: {e}")
