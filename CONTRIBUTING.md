# Contributing to Lecture Sleep Club

We welcome community contributions to improve transcription accuracy! All corrections go through a review process to maintain quality.

## 🎯 Ways to Contribute

### Method 1: Direct Pull Request (For Experienced Contributors)
**Best for:** Multiple corrections, formatting fixes, or trusted contributors

### Method 2: GitHub Issue Report (For Everyone)
**Best for:** Single corrections, suggestions, or if you're new to Git

### Method 3: GitHub Discussions
**Best for:** Questions, general feedback, or discussing transcription approaches

---

## 📝 Method 1: Pull Request Workflow

### Step 1: Find and Verify the Error
- Play the corresponding video/audio file
- Note the exact timestamp (HH:MM:SS format)
- Identify the incorrect transcription
- Verify your correction by listening multiple times

### Step 2: Fork and Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/lecture_sleep_club.git
cd lecture_sleep_club
git checkout -b fix-transcription-heidegger-lecture-01
```

### Step 3: Make Your Correction
1. Navigate to the correct course folder
2. Edit the appropriate `.srt` file
3. **Only change the transcription text** - keep timestamps exactly as they are
4. Ensure proper SRT format is maintained

Example correction:
```srt
42
00:05:23,456 --> 00:05:25,789
- Before: "phenomenological reduction"
+ After:  "phenomenological reduction"
```

### Step 4: Test Your Changes
```bash
# Validate SRT format (if available)
python tools/validate_srt.py courses/philosophy-185-heidegger/lecture-01.srt

# Or manually check:
# - Timestamps are in HH:MM:SS,mmm --> HH:MM:SS,mmm format
# - No extra blank lines between subtitle blocks
# - Text encoding is UTF-8
```

### Step 5: Commit and Push
```bash
git add courses/philosophy-185-heidegger/lecture-01.srt
git commit -m "Fix transcription error in Heidegger lecture 01

- Timestamp: 00:05:23
- Change: 'phenomenlogical' → 'phenomenological'
- Verified by listening to audio at 5:23 mark"
git push origin fix-transcription-heidegger-lecture-01
```

### Step 6: Create Pull Request
1. Go to GitHub and create a Pull Request
2. Use this title format: `Fix: [Course] Lecture XX - [Brief Description]`
3. Include:
   - **Timestamp** of the error
   - **Before/After** examples
   - **Audio verification** confirmation
   - **Source** (which audio file you referenced)

---

## 🐛 Method 2: Issue Report (Easiest)

For simple corrections or if you're new to Git:

1. **Go to [Issues](https://github.com/teslat0mic/lecture_sleep_club/issues)**
2. **Click "New Issue"**
3. **Use the "Transcription Correction" template**
4. **Fill out the form:**
   - Course name
   - Lecture number
   - Timestamp (HH:MM:SS)
   - Current incorrect text
   - Your suggested correction
   - How you verified it

**We'll review and implement approved corrections!**

---

## 🏗️ Review and Approval Process

### For Pull Requests:
1. **Automated Checks** ✅
   - SRT format validation
   - Timestamp integrity check

2. **Community Review** 👥
   - Other contributors can review and comment
   - Minimum 1 approval required

3. **Maintainer Review** 👑
   - Final quality check
   - Audio verification when needed
   - Merge approval

### For Issue Reports:
1. **Initial Review** (24-48 hours)
   - Validate the correction suggestion
   - Check audio reference

2. **Implementation**
   - Create fix branch
   - Apply correction
   - Test validation

3. **Merge and Close**
   - Merge correction
   - Close issue with reference

---

## 📊 Quality Standards

### ✅ Approved Corrections Must:
- **Match Audio Exactly** - Verified by listening to the referenced timestamp
- **Maintain Format** - SRT format, timestamps, and encoding preserved
- **Be Factual** - Only correct actual transcription errors
- **Be Precise** - Fix only the specific error mentioned

### ❌ Rejected Corrections:
- Unverified changes (no timestamp/audio reference)
- Formatting changes without content fixes
- Multiple unrelated fixes in one PR
- Spelling preferences (vs. actual errors)

---

## 🎯 Correction Priorities

1. **High Priority:** Factual errors, proper names, technical terms
2. **Medium Priority:** Minor spelling corrections, punctuation
3. **Low Priority:** Stylistic preferences, formatting cleanup

---

## 💬 Communication

- **Questions?** Use [GitHub Discussions](https://github.com/teslat0mic/lecture_sleep_club/discussions)
- **Issues?** Report via [GitHub Issues](https://github.com/teslat0mic/lecture_sleep_club/issues)
- **Chat?** Join our community discussions

---

## 🙏 Recognition

Contributors will be:
- ✅ Listed in our [Contributors](../CONTRIBUTORS.md) file
- ✅ Mentioned in release notes
- ✅ Featured in our community acknowledgments

**Thank you for helping improve philosophy lecture transcriptions!** 🎓📚