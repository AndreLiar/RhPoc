# HR Assistant Deployment

This repository contains the HR Assistant AI application with secure Kubernetes deployment to the OpsTurn360 platform.

## Status
- ✅ Kubernetes manifests configured
- ✅ GitHub Actions CI/CD pipeline ready  
- ✅ Azure AI services integration
- ✅ Secure secrets management
- ✅ AKS cluster permissions configured

## Deployment
The application deploys automatically on push to main branch.


# ACR Pull Permission Fixed

The AKS cluster can now pull images from Azure Container Registry.

- Fixed: 401 Unauthorized error when pulling images
- Granted: AcrPull role to AKS kubelet identity
- Status: Ready for deployment

Mon Nov 24 17:27:05 CET 2025

