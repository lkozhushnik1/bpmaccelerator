// Storage Account module

param name string
param location string
param managedIdentityPrincipalId string

var containers = [
  'process-artifacts'
  'agent-outputs'
  'deployment-manifests'
]

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: name
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    accessTier: 'Hot'
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  parent: storageAccount
  name: 'default'
}

resource blobContainers 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = [
  for container in containers: {
    parent: blobService
    name: container
    properties: {
      publicAccess: 'None'
    }
  }
]

// Grant managed identity Storage Blob Data Contributor role
var blobContributorRole = 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
resource storageRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, managedIdentityPrincipalId, blobContributorRole)
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', blobContributorRole)
    principalId: managedIdentityPrincipalId
    principalType: 'ServicePrincipal'
  }
}

output name string = storageAccount.name
output id string = storageAccount.id
