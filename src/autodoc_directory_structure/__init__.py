from pathlib import Path
import subprocess

from docutils import nodes
from docutils.parsers.rst import Directive, directives


class AutodocDirectoryStructureDirective(Directive):
    """ReST directive to generate a directory structure with descriptions.
    
    Options:
        gitignore: Exclude files that are gitignored.

    """

    has_content = False
    required_arguments = 1
    option_spec = {
        "gitignore": directives.flag
    }

    def run(self) -> list:
        root_dir = Path(self.arguments[0]).resolve()
        tree_structure = self.build_tree(root_dir=root_dir)
        return [tree_structure]

    def build_tree(
        self,
        *,
        root_dir: Path,
        relative_to: Path | None = None,
        prefix: str = "",  # TODO: Remove
    ) -> nodes.bullet_list:
        """Generate a directory structure with descriptions.

        Descriptions are generated from any README files present.
        """
        if not relative_to:
            relative_to = root_dir

        ul = nodes.bullet_list()

        for item in sorted(root_dir.iterdir()):
            if "gitignore" in self.options:
                gitignored = subprocess.run(
                    ["git", "check-ignore", str(item)],
                    capture_output=True,
                ).stdout
                if gitignored:
                    continue

            li = nodes.list_item()
            paragraph = nodes.paragraph()
            paragraph += nodes.Text(prefix)

            item_text = str(item.relative_to(relative_to))
            if item.is_dir():
                item_text += "/"
            paragraph += nodes.literal(text=item_text)

            # Check if a README file exists
            # TODO: Parse the README file (support md or rst)
            description_path = item / "README"
            if description_path.is_file():
                with open(description_path, "r", encoding="utf-8") as f:
                    # Use first line as a short description
                    description = f.readline().strip()
                paragraph += nodes.Text(f" - {description}")

            li += paragraph

            # If it's a directory, recurse
            if item.is_dir():
                li += self.build_tree(root_dir=item, relative_to=relative_to, prefix="    ")

            ul += li

        return ul


def setup(app):
    app.add_directive("autodoc_directory_structure", AutodocDirectoryStructureDirective)
