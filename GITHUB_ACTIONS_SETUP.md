# GitHub Actions Setup for Automatic Docker Build and Push

This repository is configured with GitHub Actions to automatically build and push Docker images to Docker Hub whenever code is pushed to the `main` branch.

## 🔧 Setup Instructions

### 1. Create Docker Hub Access Token

1. Go to [Docker Hub](https://hub.docker.com/)
2. Login with your account (`bbotella`)
3. Go to **Account Settings** → **Security** → **Access Tokens**
4. Click **New Access Token**
5. Name: `GitHub Actions - Recetas Tía Carmen`
6. Permissions: **Read, Write, Delete**
7. Click **Generate**
8. **Copy the token** (you won't see it again!)

### 2. Add Secret to GitHub Repository

1. Go to your GitHub repository: `https://github.com/bbotella/recetas`
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `DOCKER_HUB_ACCESS_TOKEN`
5. Value: Paste the Docker Hub access token
6. Click **Add secret**

### 3. Verify Setup

Once configured, the GitHub Action will:
- ✅ Trigger on every push to `main` branch
- ✅ Build multi-architecture Docker images (AMD64 + ARM64)
- ✅ Push to Docker Hub automatically
- ✅ Update Docker Hub repository description
- ✅ Use GitHub cache for faster builds

## 🚀 How It Works

### Trigger Events
- **Push to main**: Builds and pushes `latest` tag
- **Pull requests**: Builds image for testing (doesn't push)
- **Manual trigger**: Can be run manually from GitHub Actions tab

### Image Tags Created
- `latest` - Always points to the latest main branch
- `main-<sha>` - Specific commit SHA from main branch
- `pr-<number>` - Pull request builds (testing only)

### Features
- **Multi-architecture**: Supports both AMD64 and ARM64
- **Layer caching**: Uses GitHub Actions cache for faster builds
- **Automatic README**: Updates Docker Hub description from README.md
- **Security**: Uses access tokens, not passwords

## 📋 Monitoring

### Check Build Status
- Go to **Actions** tab in your GitHub repository
- Each push will show a new workflow run
- Green checkmark = successful build and push
- Red X = failed build (check logs)

### Docker Hub Updates
After successful builds, check:
- https://hub.docker.com/r/bbotella/recetas-tia-carmen
- New tags should appear automatically
- Repository description should match README.md

## 🔍 Troubleshooting

### Common Issues

**Build fails with authentication error:**
- Check that `DOCKER_HUB_ACCESS_TOKEN` secret is set correctly
- Ensure Docker Hub access token has correct permissions
- Token might have expired (they last 1 year by default)

**Multi-architecture build fails:**
- This is usually temporary - retry the action
- Check Docker Hub status page for outages

**Image not updating on Docker Hub:**
- Check the Actions tab for errors
- Verify the workflow completed successfully
- May take a few minutes to appear on Docker Hub

### Manual Trigger
If you need to rebuild without pushing code:
1. Go to **Actions** tab
2. Select **Build and Push Docker Image**
3. Click **Run workflow**
4. Select branch and click **Run workflow**

## 🛡️ Security Notes

- Never commit Docker Hub passwords/tokens to code
- Use repository secrets for sensitive data
- Access tokens are more secure than passwords
- Tokens can be revoked if compromised

## 📊 Build Information

Each build will:
- Take ~5-10 minutes for multi-architecture
- Use ~2-3 GB of GitHub Actions minutes
- Generate ~200MB compressed image
- Support both x86_64 and ARM64 architectures

---

Your repository is now set up for automatic Docker deployments! 🚀