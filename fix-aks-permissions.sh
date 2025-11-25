
# Fix AKS RBAC Permissions for GitHub Actions Service Principal

# 1. Get the service principal ID from your AZURE_CREDENTIALS secret
# Extract the clientId from your GitHub secret (you'll need to do this manually)
SP_CLIENT_ID="42a852a7-af59-4b02-a305-f929f24f5f11"

# 2. Grant the service principal proper AKS permissions
az role assignment create \
  --assignee $SP_CLIENT_ID \
  --role "Azure Kubernetes Service Cluster User Role" \
  --scope /subscriptions/e75e283f-2720-4ae5-8a7b-da0b8d4f6c11/resourceGroups/rg-gap-dev/providers/Microsoft.ContainerService/managedClusters/aks-gap-dev

# 3. Grant cluster admin permissions (for deployment operations)
az role assignment create \
  --assignee $SP_CLIENT_ID \
  --role "Azure Kubernetes Service Cluster Admin Role" \
  --scope /subscriptions/e75e283f-2720-4ae5-8a7b-da0b8d4f6c11/resourceGroups/rg-gap-dev/providers/Microsoft.ContainerService/managedClusters/aks-gap-dev

echo "✅ Service principal permissions updated!"
echo "Now re-run your GitHub Actions deployment."

