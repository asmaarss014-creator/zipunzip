import os
import sys
import zipfile
import argparse

def compress(input_path, output_zip):
    """Compresses a file or directory into a .zip file."""
    if not os.path.exists(input_path):
        print(f"❌ Error: '{input_path}' does not exist.")
        sys.exit(1)

    print(f"📦 Compressing '{input_path}' into '{output_zip}'...")
    
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if os.path.isdir(input_path):
            for root, dirs, files in os.walk(input_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Keep relative path structure inside the zip
                    arcname = os.path.relpath(file_path, start=input_path)
                    zipf.write(file_path, arcname)
        else:
            zipf.write(input_path, os.path.basename(input_path))
            
    print(f"✅ Compression complete: {output_zip}")

def decompress(input_zip, output_dir):
    """Decompresses a .zip file, overwriting existing files."""
    if not os.path.exists(input_zip):
        print(f"❌ Error: '{input_zip}' does not exist.")
        sys.exit(1)

    print(f"📦 Decompressing '{input_zip}' into '{output_dir}'...")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(input_zip, 'r') as zipf:
        # Extract all files. Python's extractall() overwrites existing files by default.
        # We loop through members to prevent path traversal security issues.
        for member in zipf.infolist():
            target_path = os.path.abspath(os.path.join(output_dir, member.filename))
            
            # Security check: ensure we don't extract outside the target directory
            if not target_path.startswith(os.path.abspath(output_dir)):
                print(f"⚠️ Skipping unsafe path: {member.filename}")
                continue

            zipf.extract(member, output_dir)
            
    print(f"✅ Decompression complete: {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress and Decompress files in repository.")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Compress command
    c_parser = subparsers.add_parser("compress", help="Compress a file/folder into a .zip")
    c_parser.add_argument("input", help="File or directory to compress")
    c_parser.add_argument("output", help="Output .zip file name")

    # Decompress command
    d_parser = subparsers.add_parser("decompress", help="Decompress a .zip file")
    d_parser.add_argument("input", help=".zip file to decompress")
    d_parser.add_argument("output", help="Destination directory (e.g., '.' for root)", nargs="?", default=".")

    args = parser.parse_args()

    if args.command == "compress":
        compress(args.input, args.output)
    elif args.command == "decompress":
        decompress(args.input, args.output)
    else:
        parser.print_help()
