# Contributing to Lecture Sleep Club

## How to Submit Transcription Corrections

### Step 1: Find the Error
- Play the corresponding video/audio
- Note the timestamp and incorrect text
- Identify the correct transcription

### Step 2: Make the Correction
1. Fork this repository
2. Navigate to the course folder
3. Edit the appropriate `.srt` file
4. Ensure timestamp format remains: `HH:MM:SS,mmm --> HH:MM:SS,mmm`

### Step 3: Validate Your Changes
```bash
# Run validation script
python tools/validate_srt.py courses/philosophy-185-heidegger/lectures/lecture-01.srt
```

### Step 4: Submit
- Create a descriptive pull request title
- Include timestamp and before/after examples
- Reference the course and lecture number