# First Gen Employer Portal (demo)

Password-protected static build of the First Gen Employer Portal proof of concept. All people and data are fictitious.

The portal is stored encrypted in `portal.bin`; `index.html` asks for the password and decrypts it in the browser. See `DEPLOY.md` for hosting and DNS steps, and `tools/build.py` to rebuild after the portal changes.
