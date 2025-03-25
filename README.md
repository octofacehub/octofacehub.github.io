# OctoFaceHub

A decentralized repository for machine learning models stored on IPFS.

## About

OctoFaceHub is a platform for sharing machine learning models using IPFS for storage and GitHub Pages for discovery. Models added to this repository are stored permanently on IPFS and can be easily downloaded with the `octoface` CLI tool.

## Browse Models

Visit our [GitHub Pages site](https://octofacehub.github.io) to browse available models.

## Adding Your Model

To add your model to OctoFaceHub, you have two options:

### Option 1: Using the OctoFace CLI (Recommended)

1. Install the OctoFace CLI:

   ```bash
   pip install octoface
   ```

2. Upload your model:

   ```bash
   octoface upload ./path/to/model --name "My Model" --description "A description" --tags "tag1,tag2"
   ```

3. If you don't have push access, use:
   ```bash
   octoface generate-files --path ./path/to/model --name "My Model" --description "A description" --tags "tag1,tag2"
   ```
   Then follow the instructions in the generated GUIDE.md file.

### Option 2: Manual Submission

1. Fork this repository
2. Add your model to the `models` directory following this structure:
   ```
   models/
   └── your-github-username/
       └── your-model-name/
           ├── metadata.json
           └── README.md
   ```
3. Create a pull request

## Organization

Models are organized by GitHub username to ensure ownership and access control. Only the original model submitter (matching GitHub username) can modify their models through pull requests.

## License

All model metadata in this repository is licensed under MIT.
Individual models may have their own licenses as specified in their metadata.
