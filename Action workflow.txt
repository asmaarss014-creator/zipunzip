name: Universal ZIP Preparer

on:
  workflow_dispatch:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  unzip:
    runs-on: ubuntu-latest

    steps:

      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0


      - name: Install Archive Tools
        continue-on-error: true
        run: |
          sudo apt-get update -y || true
          sudo apt-get install -y \
            unzip \
            zip \
            p7zip-full \
            tar \
            gzip \
            xz-utils \
            rsync || true


      - name: Create Extraction Folder
        run: |
          mkdir -p extracted


      - name: Extract ZIP Files
        continue-on-error: true
        run: |
          find . -type f -iname "*.zip" | while read file
          do
            echo "Extracting $file"

            unzip -o "$file" -d extracted || true
          done


      - name: Extract Other Archives
        continue-on-error: true
        run: |

          find . -type f -iname "*.7z" | while read file
          do
            echo "Extracting $file"
            7z x "$file" -oextracted || true
          done


          find . -type f -iname "*.tar.gz" | while read file
          do
            echo "Extracting $file"
            tar -xzf "$file" -C extracted || true
          done


      - name: Move Extracted Files Into Repository
        continue-on-error: true
        run: |
          rsync -av extracted/ ./ || true


      - name: Remove Empty Extraction Folder
        continue-on-error: true
        run: |
          rm -rf extracted || true


      - name: Commit Extracted Files
        continue-on-error: true
        run: |
          git config --global user.name "github-actions"
          git config --global user.email "github-actions@github.com"

          git add .

          git commit -m "Auto extract archive files" || true

          git push || true


      - name: Completed
        run: |
          echo "Archive extraction completed."
          echo "Extracted files were saved into the repository."
          echo "Unsupported files were skipped."
