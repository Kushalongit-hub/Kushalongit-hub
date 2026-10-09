# Install the animated ASCII Archive GitHub profile

1. Create the public repository `Kushalongit-hub/Kushalongit-hub`, if it doesn't exist.
2. Upload `README.md` and `assets/` to the repository root. Leave the paths unchanged.
3. On Windows PowerShell, from the directory containing README.md:

```powershell
git init
git branch -M main
git add README.md assets/
git commit -m "feat: animated ASCII archive profile"
git remote add origin https://github.com/Kushalongit-hub/Kushalongit-hub.git
git push -u origin main
```

If the repository already exists, clone it first, copy in `README.md` and `assets/`, then run `git add README.md assets/; git commit -m "style: animate ASCII profile"; git push`.

## Notes
- The animations are self-hosted GIFs. No external animation service, script, HTML canvas, or GitHub Action is required.
- Markdown text, clickable project links, and accessibility alt text stay present.
- GitHub does not support arbitrary interactive JS/CSS in README files.
- People with reduced-motion settings may still see GIF playback depending on their browser. A static alternative is not automatically selected in this version.
- To update the art, install Pillow (`pip install pillow`) and run `python build_animations.py`. Do not upload this generator to the profile repo unless desired.
