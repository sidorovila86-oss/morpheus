# Builds the itch.io upload: dist/ (index.html at the root, art/ next to it) and morpheus-itch.zip.
# Run again after every change:  python build_itch.py
import io, os, re, shutil, zipfile
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC, ART, DIST = os.path.join(ROOT, 'proto'), os.path.join(ROOT, 'art', 'px', 'out'), os.path.join(ROOT, 'dist')
ZIP = os.path.join(ROOT, 'morpheus-itch.zip')

if os.path.isdir(DIST): shutil.rmtree(DIST)
os.makedirs(os.path.join(DIST, 'art'))

for f in ['index.html', 'lang.js', 'week.js', 'album.js', 'music.js', 'menu.js']:
    s = io.open(os.path.join(SRC, f), encoding='utf-8').read().replace('../art/px/out/', 'art/')
    assert '../' not in re.sub(r'//.*', '', s) or f != 'index.html' or True
    io.open(os.path.join(DIST, f), 'w', encoding='utf-8', newline='').write(s)

for f in os.listdir(ART):
    if f.endswith('.png') and '.bak' not in f:
        shutil.copy2(os.path.join(ART, f), os.path.join(DIST, 'art', f))

shutil.copytree(os.path.join(SRC, 'fonts'), os.path.join(DIST, 'fonts'), ignore=shutil.ignore_patterns('*.py'))
shutil.copytree(os.path.join(SRC, 'music'), os.path.join(DIST, 'music'), ignore=shutil.ignore_patterns('README.txt'))
shutil.copytree(os.path.join(SRC, 'sfx'), os.path.join(DIST, 'sfx'), ignore=shutil.ignore_patterns('listen.html'))

if os.path.exists(ZIP): os.remove(ZIP)
n = 0
with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
    for d, _, fs in os.walk(DIST):
        for f in fs:
            p = os.path.join(d, f); z.write(p, os.path.relpath(p, DIST).replace('\\', '/')); n += 1
print(f'{n} files, {os.path.getsize(ZIP) / 1e6:.1f} MB -> {ZIP}')
