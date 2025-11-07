import pkg_resources

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

installed = {pkg.key for pkg in pkg_resources.working_set}
required = {pkg_resources.Requirement.parse(r).key for r in requirements}

missing = required - installed
extra = installed - required

print("✅ Installed from requirements:", required & installed)
print("❌ Missing:", missing)
print("⚠️ Extra packages not in requirements:", extra)
