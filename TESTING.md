# JARVIS Testing Guide

This guide helps you test all the features of JARVIS to ensure everything is working correctly.

## Prerequisites
- Make sure you have set up your `.env` file with `GROQ_API_KEY`
- All dependencies installed via `pip install -r requirements.txt`

## Basic Commands to Test

### 1. Opening Websites (Direct Commands - Most Reliable)
These commands work without AI processing for maximum reliability:

```
"Jarvis, open YouTube"
"Jarvis, open Gmail"
"Jarvis, open Google"
"Jarvis, open Facebook"
"Jarvis, open Twitter"
"Jarvis, open Instagram"
"Jarvis, open Reddit"
"Jarvis, open GitHub"
"Jarvis, open LinkedIn"
"Jarvis, open Netflix"
"Jarvis, open Spotify"
"Jarvis, open Amazon"
"Jarvis, open WhatsApp"
"Jarvis, open Discord"
"Jarvis, open Slack"
```

### 2. Opening macOS Applications
```
"Jarvis, open Safari"
"Jarvis, open Chrome"
"Jarvis, open Firefox"
"Jarvis, open Notes"
"Jarvis, open Calendar"
"Jarvis, open Music"
"Jarvis, open Messages"
```

### 3. Search Commands
```
"Jarvis, search Python tutorials"
"Jarvis, search for best restaurants near me"
"Jarvis, google artificial intelligence"
```

### 4. Volume Control
```
"Jarvis, volume 50"
"Jarvis, set volume 75"
"Jarvis, volume 100"
```

### 5. Conversational Commands
You can also use natural language:
```
"Jarvis, what's the weather?"
"Jarvis, what time is it?"
"Jarvis, who are you?"
"Jarvis, hello"
"Jarvis, thank you"
```

## Command Variations

JARVIS understands multiple ways to say the same thing:

### Opening Apps/Sites:
- "open YouTube"
- "launch YouTube"
- "start YouTube"
- "open up YouTube"

### Searching:
- "search Python"
- "google Python"
- "find Python tutorials"
- "look up Python"

## Wake Word

JARVIS responds to:
1. **"Jarvis"** - Main wake word
2. **Direct commands** - Commands starting with action words like "open", "search", "volume", etc.

Examples:
- ✅ "Jarvis, open YouTube" (with wake word)
- ✅ "Open YouTube" (direct command)
- ❌ "I want to watch videos" (too vague, will be ignored)

## Text Mode Testing

For debugging without voice, run in text mode:
```bash
python main.py --text
```

Then type commands directly:
```
YOU: open youtube
YOU: search python tutorials
YOU: volume 50
```

## Troubleshooting

### If commands don't work:

1. **Check Console Output**
   - Look for "Processing: [your command]"
   - Check for any error messages

2. **Verify GROQ_API_KEY**
   - Make sure it's set in `.env` file
   - Check if API key is valid

3. **Test Direct Commands First**
   - Try simple commands like "open YouTube"
   - These bypass AI and should always work

4. **Check Microphone (Voice Mode)**
   - Ensure microphone permissions are granted
   - Speak clearly and wait for "Listening..." prompt

5. **Try Text Mode**
   - Run with `--text` flag to eliminate voice recognition issues
   - Helps isolate if problem is with voice or command processing

## Expected Behavior

### Successful Command:
```
Listening...
Recognizing...
Processing: open youtube
Opening Youtube, sir.
```

### Ignored Input (No Wake Word):
```
Listening...
Recognizing...
Ignored: random conversation
```

### Error Handling:
```
Listening...
Recognizing...
Processing: open youtube
Groq API Error: [error details]
Opening Youtube, sir.  # Falls back to direct command handling
```

## Advanced Testing

### Test Skill Loading:
When JARVIS starts, you should see:
```
Loaded skill: system_skill
Loaded skill: web_skill
Loaded skill: [other skills]
```

### Test Error Recovery:
JARVIS has built-in error recovery. Even if Groq API fails, direct commands should still work.

## Performance Tips

1. **Speak clearly** - Enunciate wake word "Jarvis"
2. **Wait for prompt** - Let JARVIS finish listening before speaking
3. **Use direct commands** - "Open YouTube" is more reliable than "I want to watch videos"
4. **Keep it simple** - Short, clear commands work best

## Common Issues

| Issue | Solution |
|-------|----------|
| "Ignored: [command]" | Add "Jarvis" wake word or use direct command verb |
| "I am having trouble connecting to the brain" | Check GROQ_API_KEY, but direct commands should still work |
| App doesn't open | Check app name spelling, try exact name from Applications folder |
| Website doesn't open | Check internet connection, try different browser |

## Success Criteria

✅ JARVIS should successfully:
- Open all listed websites in browser
- Open macOS applications
- Perform Google searches
- Control system volume
- Respond to conversational queries
- Handle errors gracefully with fallback to direct commands

---

**Note**: The direct command system ensures that basic operations (open, search, volume) work even if AI processing fails. This makes JARVIS more reliable and responsive.
