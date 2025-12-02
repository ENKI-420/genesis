"""Init command for GENESIS CLI."""

from typing import Optional


def init_command(
    project_name: str = "genesis-project",
    directory: Optional[str] = None,
    template: str = "default",
) -> int:
    """
    Initialize a new GENESIS project.
    
    Args:
        project_name: Name of the project.
        directory: Directory to create project in.
        template: Project template to use.
        
    Returns:
        Exit code (0 for success).
    """
    import os
    
    # Determine project directory
    if directory:
        project_dir = os.path.join(directory, project_name)
    else:
        project_dir = project_name
    
    print(f"Initializing GENESIS project: {project_name}")
    
    # Create directory structure
    directories = [
        "",
        "src",
        "tests",
        "config",
        "organisms",
        "docs",
    ]
    
    for d in directories:
        path = os.path.join(project_dir, d)
        print(f"  Creating: {path}")
    
    # Create configuration file
    config_content = f"""# GENESIS Project Configuration
project:
  name: {project_name}
  version: 0.1.0

genesis:
  version: "1.0.0"
  
agents:
  enabled:
    - AIDEN
    - AURA
    - PALS

metrics:
  ccce:
    enabled: true
    threshold: 0.8
"""
    
    print(f"\nProject '{project_name}' initialized successfully!")
    print(f"\nTo get started:")
    print(f"  cd {project_dir}")
    print(f"  genesis status")
    
    return 0
