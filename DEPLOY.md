# Putting the First Gen portal demo on a domain

## What is in this folder

- `site/` is the whole website. Upload exactly this folder's contents to any static host.
  - `index.html`: a small unlock page (password box).
  - `portal.bin`: the full portal, encrypted with AES-256-GCM. The key comes from the password (PBKDF2-SHA256, 250,000 rounds), so nobody can read the roster from the public files without the password.
  - `robots.txt` plus a `noindex` tag keep search engines out.
  - `.nojekyll` stops GitHub Pages from processing the files.
- `tools/build.py` and `tools/unlock.html` rebuild `site/` after the portal changes:
  `python3 tools/build.py ../First_Gen_Employer_Portal_POC.html site "<password>"`

The plain, unencrypted portal HTML never goes into the repo or onto the host. Because of that, the GitHub repo can be public (free GitHub Pages) without exposing anything.

"Remember on this device" saves the password in that browser so returning visitors skip the box. Changing the password means rebuilding `site/` and re-publishing.

## Hosting: GitHub Pages (recommended)

1. Repo `FirstGen212/first-gen-portal-demo` (public), containing `site/` contents at the root plus `tools/`.
2. Settings > Pages: deploy from branch `main`, folder `/ (root)`.
3. It is live at `https://firstgen212.github.io/first-gen-portal-demo/` within a minute or two.
4. Custom domain: Settings > Pages > Custom domain, enter the domain (this writes a `CNAME` file), then add the DNS records below. Tick "Enforce HTTPS" once the certificate is issued (can take up to an hour after DNS resolves).

Recommended: verify the domain in GitHub (profile Settings > Pages > Add a domain) so nobody else can claim it for their own Pages site.

## DNS records

At the registrar or DNS host for the domain (GoDaddy, Namecheap, Cloudflare, Google/Squarespace, etc.):

### A subdomain such as `demo.example.com` (simplest)

| Type  | Name / Host | Value                  |
|-------|-------------|------------------------|
| CNAME | `demo`      | `firstgen212.github.io` |

### The bare domain `example.com`

| Type | Name / Host | Value             |
|------|-------------|-------------------|
| A    | `@`         | `185.199.108.153` |
| A    | `@`         | `185.199.109.153` |
| A    | `@`         | `185.199.110.153` |
| A    | `@`         | `185.199.111.153` |
| AAAA | `@`         | `2606:50c0:8000::153` |
| AAAA | `@`         | `2606:50c0:8001::153` |
| AAAA | `@`         | `2606:50c0:8002::153` |
| AAAA | `@`         | `2606:50c0:8003::153` |
| CNAME | `www`      | `firstgen212.github.io` |

Remove any existing A, AAAA or CNAME records on the same name first (registrars often add a "parking" record). If the DNS host is Cloudflare, set these records to "DNS only" (grey cloud) until GitHub has issued the HTTPS certificate.

Check propagation: `dig demo.example.com +short` should return `firstgen212.github.io` and the 185.199.x.153 addresses.

## Alternatives

Cloudflare Pages, Netlify and Vercel all take the same `site/` folder as a drag-and-drop upload and support custom domains with free HTTPS. Cloudflare Pages also offers Cloudflare Access (free up to 50 users), which can replace the password with "sign in with your work email", a stronger gate for a client-facing demo.
