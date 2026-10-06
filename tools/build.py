"""Build the password-protected static site.

Encrypts the portal HTML with AES-256-GCM (key from PBKDF2-SHA256, 250k rounds)
so the roster never sits readable on the public host. index.html is a small
unlock page that decrypts in the browser and renders the portal.

usage: python3 build.py <portal.html> <out_dir> <password>
"""
import base64, os, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ITER = 250_000
src, out, pw = sys.argv[1], sys.argv[2], sys.argv[3]
html = open(src, 'rb').read()
salt, iv = os.urandom(16), os.urandom(12)
key = PBKDF2HMAC(hashes.SHA256(), 32, salt, ITER).derive(pw.encode())
ct = AESGCM(key).encrypt(iv, html, None)
os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'portal.bin'), 'wb').write(salt + iv + ct)
tpl = open(os.path.join(os.path.dirname(__file__), 'unlock.html'), encoding='utf-8').read()
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(tpl.replace('__ITER__', str(ITER)))
open(os.path.join(out, 'robots.txt'), 'w').write('User-agent: *\nDisallow: /\n')
open(os.path.join(out, '.nojekyll'), 'w').write('')
print('built', out, len(ct), 'bytes encrypted')
