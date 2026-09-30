import os

def inject_badge():
    readme_path = "README.md"
    
    badge_markdown = """[![Sponsor RobDoe Pty Ltd](https://img.shields.io/badge/Sponsor-%F0%9F%92%9C%20Buy%20Me%20a%20Coffee-ffdd54?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/robdoe)

"""

    if os.path.exists(readme_path):
        with open(readme_path, "r") as f:
            content = f.read()
        
        # Check if badge is already there
        if "buymeacoffee.com/robdoe" in content:
            print("[+] Badge already exists in README.md. Skipping injection.")
            return

        new_content = badge_markdown + content
    else:
        # Create a clean README if none exists
        new_content = badge_markdown + "# RobDoe Pty Ltd / AiAgency101\n\nSovereign Grid & Decentralized Technical Workspace.\n"

    with open(readme_path, "w") as f:
        f.f.write(new_content) if hasattr(f, 'f') else f.write(new_content)

    print("\n==========================================================")
    print("          README BADGE INJECTION COMPLETE                 ")
    print("==========================================================")
    print(f"[+] Target File         : {readme_path}")
    print("[+] Status              : Sponsor Badge Prepended")
    print("==========================================================\n")

if __name__ == "__main__":
    inject_badge()
