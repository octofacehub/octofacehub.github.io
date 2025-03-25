# Contributing to OctoFaceHub

Thank you for your interest in contributing to OctoFaceHub! This guide explains how to add your models to the repository.

## Permission Model

OctoFaceHub uses a directory-based permission model:

1. Each GitHub user can only add or modify files within their own directory: `models/YOUR_USERNAME/`
2. Pull requests that modify files outside your directory will be automatically rejected
3. You cannot modify other users' models or metadata

## Adding a Model

### Option 1: Using the OctoFace CLI (Recommended)

1. Install the OctoFace CLI:

   ```bash
   pip install octoface
   ```

2. Set up your GitHub token (needed for authentication):

   ```bash
   export GITHUB_API_TOKEN="your-personal-access-token"
   ```

3. For uploading a model to IPFS and generating the files:

   ```bash
   octoface upload --path ./path/to/model --name "My Model" --description "A description" --tags "tag1,tag2"
   ```

4. If you don't have push access, the CLI will provide instructions to fork the repository and submit a PR.

### Option 2: Generate Files Only

If you've already uploaded your model to IPFS or want to generate the files separately:

```bash
octoface generate-files --cid "your-ipfs-cid" --name "My Model" --description "A description" --tags "tag1,tag2"
```

Then follow the instructions in the generated GUIDE.md file.

### Option 3: Manual Submission

1. Fork the repository
2. Clone your fork locally
3. Create the necessary files in your user directory:
   ```
   models/
   └── your-github-username/
       └── your-model-name/
           ├── metadata.json
           └── README.md
   ```
4. Add your model details to the metadata.json file (see example below)
5. Create a README.md file with information about your model
6. Commit your changes and create a pull request

## Metadata Format

Your `metadata.json` file should follow this format:

```json
{
  "name": "Your Model Name",
  "author": "your-github-username",
  "description": "A detailed description of your model",
  "tags": ["tag1", "tag2", "tag3"],
  "ipfs_cid": "your-ipfs-cid",
  "size_mb": 100.5,
  "created_at": "2023-07-31T12:00:00Z",
  "license": "MIT",
  "homepage": "https://github.com/your-username/your-model",
  "download_url": "https://w3s.link/ipfs/your-ipfs-cid"
}
```

## Automated Processes

When you submit a pull request:

1. Our GitHub Actions workflow will validate that you're only modifying files in your directory
2. If you're adding or updating model metadata, our system will automatically update the central model-map.json
3. Your model will appear in the catalog after the PR is merged

## Need Help?

If you have any questions or need assistance, please open an issue in the repository or reach out to the maintainers.
