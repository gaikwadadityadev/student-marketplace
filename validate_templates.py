#!/usr/bin/env python3
"""Validate all Jinja2 templates for syntax errors"""
import os
from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError

template_dir = './templates'
env = Environment(loader=FileSystemLoader(template_dir))

template_files = [f for f in os.listdir(template_dir) if f.endswith('.html')]

print(f"Validating {len(template_files)} templates...\n")

errors = []
for template_file in sorted(template_files):
    try:
        env.get_template(template_file)
        print(f"✓ {template_file}")
    except TemplateSyntaxError as e:
        error_msg = f"✗ {template_file}: Line {e.lineno} - {e.message}"
        print(error_msg)
        errors.append(error_msg)

if errors:
    print(f"\n❌ {len(errors)} template(s) with syntax errors:")
    for error in errors:
        print(f"  {error}")
else:
    print(f"\n✅ All {len(template_files)} templates are valid!")
