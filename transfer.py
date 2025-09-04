#!/usr/bin/env python3
"""
Fixed SRT File Migration Script

Copies SRT transcription files from project directories directly into course folders.
No 'lectures' subfolder - files go directly in each course directory.
"""

import os
import shutil
import re
from pathlib import Path
from typing import Dict, List

class SRTMigrator:
    def __init__(self, workflow_dir: str, github_dir: str):
        self.workflow_dir = Path(workflow_dir)
        self.github_dir = Path(github_dir)
        
        # Mapping from source project directories to target course directories
        self.project_mapping = {
            'division_1': 'philosophy-185-heidegger',
            'division_2': 'basic-problems-phenomenology',
            'from-god-to-gods-and-back': 'philosophy-6-from-god-to-gods',
            'MerleauPontysPhenomenologyOfPerception': 'philosophy-188-merleau-ponty',
            'Phil_7_2': 'philosophy-7-part2',
            'Phil_7_Existentialism_in_Literature_and_Film': 'philosophy-7-existentialism'
        }
        
        # Track migration results
        self.results = {
            'copied': [],
            'skipped': [],
            'errors': []
        }
    
    def extract_lecture_number(self, filename: str) -> int:
        """
        Extract lecture number from various filename formats.
        
        Examples:
        - "_Lecture_01_Phil_185-Lecture_1_20422_enhanced_trimmed.srt" -> 1
        - "Lecture_01_of_31_Hubert_Dreyfus_on_Merleau_Ponty_s_Phenomenology_of_Perception_enhanced_trimmed.srt" -> 1
        - "01_Introduction_What_is_Existentialism_15358_enhanced_trimmed.srt" -> 1
        """
        # Remove file extension and clean up
        name = filename.replace('.srt', '').replace('_enhanced_trimmed', '')
        
        # Pattern 1: _Lecture_XX_
        match = re.search(r'_Lecture_(\d+)', name)
        if match:
            return int(match.group(1))
        
        # Pattern 2: Lecture_XX_of_
        match = re.search(r'Lecture_(\d+)_of_', name)
        if match:
            return int(match.group(1))
        
        # Pattern 3: XX_ at beginning
        match = re.search(r'^(\d+)', name)
        if match:
            return int(match.group(1))
        
        # Pattern 4: Look for any standalone number
        match = re.search(r'(\d+)', name)
        if match:
            num = int(match.group(1))
            # Only use if it's a reasonable lecture number (1-99)
            if 1 <= num <= 99:
                return num
        
        return None
    
    def migrate_project(self, project_name: str) -> bool:
        """
        Migrate all SRT files from a single project.
        
        Args:
            project_name: Name of the source project directory
            
        Returns:
            bool: True if migration successful
        """
        if project_name not in self.project_mapping:
            print(f"⚠️  Skipping {project_name} - no mapping found")
            return False
        
        target_course = self.project_mapping[project_name]
        
        # Source and target paths
        source_srt_dir = self.workflow_dir / "projects" / project_name / "04_transcribed" / "srt"
        target_course_dir = self.github_dir / "courses" / target_course
        
        # Ensure target directory exists (no lectures subfolder)
        target_course_dir.mkdir(parents=True, exist_ok=True)
        
        if not source_srt_dir.exists():
            print(f"❌ Source directory not found: {source_srt_dir}")
            return False
        
        # Get all SRT files
        srt_files = list(source_srt_dir.glob("*.srt"))
        
        if not srt_files:
            print(f"⚠️  No SRT files found in {source_srt_dir}")
            return False
        
        print(f"📂 Migrating {len(srt_files)} SRT files from {project_name} to {target_course}")
        
        for srt_file in sorted(srt_files):
            try:
                lecture_num = self.extract_lecture_number(srt_file.name)
                
                if lecture_num is None:
                    print(f"⚠️  Could not extract lecture number from: {srt_file.name}")
                    self.results['skipped'].append(str(srt_file))
                    continue
                
                # Create standardized filename
                target_filename = f"lecture-{lecture_num:02d}.srt"
                target_path = target_course_dir / target_filename
                
                # Copy the file
                shutil.copy2(srt_file, target_path)
                
                print(f"  ✅ {srt_file.name} → {target_filename}")
                self.results['copied'].append({
                    'source': str(srt_file),
                    'target': str(target_path),
                    'project': project_name,
                    'course': target_course
                })
                
            except Exception as e:
                print(f"  ❌ Error copying {srt_file.name}: {e}")
                self.results['errors'].append({
                    'file': str(srt_file),
                    'error': str(e)
                })
        
        return True
    
    def migrate_all_projects(self) -> None:
        """Migrate SRT files from all available projects."""
        print("🚀 Starting SRT file migration...")
        print(f"📁 Source: {self.workflow_dir / 'projects'}")
        print(f"📁 Target: {self.github_dir / 'courses'}")
        print()
        
        # Get all project directories
        projects_dir = self.workflow_dir / "projects"
        if not projects_dir.exists():
            print(f"❌ Projects directory not found: {projects_dir}")
            return
        
        # Find all project directories (exclude lecture_sleep_club and other non-project dirs)
        project_dirs = []
        for item in projects_dir.iterdir():
            if item.is_dir() and item.name not in ['lecture_sleep_club', '_template']:
                project_dirs.append(item.name)
        
        print(f"📋 Found {len(project_dirs)} project directories:")
        for project in sorted(project_dirs):
            print(f"  • {project}")
        print()
        
        # Migrate each project
        successful_migrations = 0
        for project_name in sorted(project_dirs):
            if self.migrate_project(project_name):
                successful_migrations += 1
            print()
        
        # Print summary
        print("📊 Migration Summary:")
        print(f"  ✅ Successfully migrated: {len(self.results['copied'])} files")
        print(f"  ⚠️  Skipped: {len(self.results['skipped'])} files")
        print(f"  ❌ Errors: {len(self.results['errors'])} files")
        print(f"  📂 Projects processed: {successful_migrations}/{len(project_dirs)}")
        
        if self.results['errors']:
            print("\n🚨 Errors encountered:")
            for error in self.results['errors']:
                print(f"  • {error['file']}: {error['error']}")
        
        print("\n🎉 Migration complete!")
    
    def create_course_readmes(self) -> None:
        """Create basic README files for each course directory."""
        course_info = {
            'philosophy-185-heidegger': {
                'title': 'Philosophy 185: Heidegger',
                'lecturer': 'Hubert Dreyfus',
                'description': 'Lectures on Martin Heidegger\'s philosophy',
                'source': 'UC Berkeley, Fall 2007'
            },
            'philosophy-188-merleau-ponty': {
                'title': 'Philosophy 188: Merleau-Ponty\'s Phenomenology of Perception',
                'lecturer': 'Hubert Dreyfus',
                'description': 'Lectures on Maurice Merleau-Ponty\'s phenomenology',
                'source': 'UC Berkeley, Spring 2005'
            },
            'philosophy-6-from-god-to-gods': {
                'title': 'Philosophy 6: From God to Gods and Back',
                'lecturer': 'Hubert Dreyfus',
                'description': 'Exploration of religious and philosophical themes',
                'source': 'UC Berkeley, Spring 2007'
            },
            'philosophy-7-existentialism': {
                'title': 'Philosophy 7: Existentialism in Literature and Film',
                'lecturer': 'Hubert Dreyfus',
                'description': 'Existentialist themes in literature and film',
                'source': 'UC Berkeley'
            },
            'basic-problems-phenomenology': {
                'title': 'Basic Problems of Phenomenology',
                'lecturer': 'Hubert Dreyfus',
                'description': 'Heidegger\'s Basic Problems of Phenomenology',
                'source': 'UC Berkeley'
            },
            'philosophy-7-part2': {
                'title': 'Philosophy 7: Part 2',
                'lecturer': 'Hubert Dreyfus',
                'description': 'Additional Philosophy 7 lectures',
                'source': 'UC Berkeley'
            }
        }
        
        for course_slug, info in course_info.items():
            course_dir = self.github_dir / "courses" / course_slug
            readme_path = course_dir / "README.md"
            
            if not readme_path.exists():
                readme_content = f"""# {info['title']}

**Lecturer:** {info['lecturer']}  
**Institution:** {info['source']}

## 📖 Course Description

{info['description']}

## 📝 Lecture Files

This directory contains SRT subtitle files for each lecture in the course.
Files are named using the format: `lecture-XX.srt`

## 🔗 Source Material

Original audio sourced from UC Berkeley Open Course materials.

## 🤝 Contributing

Found a transcription error? See the main repository [CONTRIBUTING.md](../CONTRIBUTING.md) for instructions on how to submit corrections.
"""
                
                readme_path.parent.mkdir(parents=True, exist_ok=True)
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(readme_content)
                
                print(f"📄 Created README for {course_slug}")


def main():
    """Main migration function."""
    # Adjust these paths as needed
    workflow_dir = "/Users/tintin/patrick/workflow_audio"
    github_dir = "/Users/tintin/patrick/workflow_audio/projects/lecture_sleep_club"
    
    migrator = SRTMigrator(workflow_dir, github_dir)
    
    # Migrate all SRT files
    migrator.migrate_all_projects()
    
    # Create course READMEs
    print("\n📝 Creating course README files...")
    migrator.create_course_readmes()
    
    print("\n✅ Migration complete! Ready to commit and push to GitHub.")


if __name__ == "__main__":
    main()