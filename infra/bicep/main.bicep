// BPM Accelerator — main Bicep deployment entry point
// Deploys: Log Analytics, App Insights, Key Vault, Storage,
//          Managed Identity, Container App Environment, Web + API Container Apps
// Optional: Azure AI Foundry workspace (set deployFoundry=true)

targetScope = 'resourceGroup'

@description('Short environment identifier (dev, staging, prod)')
@allowed(['dev', 'staging', 'prod'])
param environment string = 'dev'

@description('Azure region for all resources')
param location string = resourceGroup().location

@description('Base name for resource naming (e.g. bpmacc)')
@minLength(3)
@maxLength(12)
param baseName string = 'bpmacc'

@description('Container image for the API app')
param apiImage string = 'mcr.microsoft.com/azuredocs/aci-helloworld:latest'

@description('Container image for the web app')
param webImage string = 'mcr.microsoft.com/azuredocs/aci-helloworld:latest'

@description('Deploy Azure AI Foundry workspace (Phase 2+)')
param deployFoundry bool = false

var suffix = '${baseName}-${environment}'

// ── Log Analytics Workspace ──────────────────────────────────────────────────
module logAnalytics './modules/log-analytics.bicep' = {
  name: 'logAnalytics'
  params: {
    name: 'law-${suffix}'
    location: location
    retentionDays: environment == 'prod' ? 90 : 30
  }
}

// ── Application Insights ─────────────────────────────────────────────────────
module appInsights './modules/app-insights.bicep' = {
  name: 'appInsights'
  params: {
    name: 'appi-${suffix}'
    location: location
    logAnalyticsWorkspaceId: logAnalytics.outputs.workspaceId
  }
}

// ── Managed Identity ─────────────────────────────────────────────────────────
module managedIdentity './modules/managed-identity.bicep' = {
  name: 'managedIdentity'
  params: {
    name: 'id-${suffix}'
    location: location
  }
}

// ── Key Vault ─────────────────────────────────────────────────────────────────
module keyVault './modules/key-vault.bicep' = {
  name: 'keyVault'
  params: {
    name: 'kv-${suffix}'
    location: location
    managedIdentityPrincipalId: managedIdentity.outputs.principalId
  }
}

// ── Storage Account ───────────────────────────────────────────────────────────
module storage './modules/storage.bicep' = {
  name: 'storage'
  params: {
    name: 'st${replace(suffix, '-', '')}001'
    location: location
    managedIdentityPrincipalId: managedIdentity.outputs.principalId
  }
}

// ── Container App Environment ─────────────────────────────────────────────────
module containerAppEnv './modules/container-app-env.bicep' = {
  name: 'containerAppEnv'
  params: {
    name: 'cae-${suffix}'
    location: location
    logAnalyticsWorkspaceId: logAnalytics.outputs.workspaceId
  }
}

// ── API Container App ──────────────────────────────────────────────────────────
module apiApp './modules/container-app.bicep' = {
  name: 'apiContainerApp'
  params: {
    name: 'ca-api-${suffix}'
    location: location
    containerAppEnvId: containerAppEnv.outputs.envId
    managedIdentityId: managedIdentity.outputs.id
    image: apiImage
    targetPort: 8000
    minReplicas: environment == 'prod' ? 2 : 1
    maxReplicas: environment == 'prod' ? 10 : 3
    env: [
      { name: 'LOG_LEVEL', value: environment == 'prod' ? 'WARNING' : 'INFO' }
      { name: 'KEY_VAULT_NAME', value: 'kv-${suffix}' }
      { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: appInsights.outputs.connectionString }
    ]
  }
}

// ── Web Container App ──────────────────────────────────────────────────────────
module webApp './modules/container-app.bicep' = {
  name: 'webContainerApp'
  params: {
    name: 'ca-web-${suffix}'
    location: location
    containerAppEnvId: containerAppEnv.outputs.envId
    managedIdentityId: managedIdentity.outputs.id
    image: webImage
    targetPort: 3000
    minReplicas: environment == 'prod' ? 2 : 1
    maxReplicas: environment == 'prod' ? 10 : 3
    env: [
      { name: 'NEXT_PUBLIC_API_URL', value: 'https://${apiApp.outputs.fqdn}' }
    ]
  }
}

// ── Outputs ───────────────────────────────────────────────────────────────────
output webAppUrl string = 'https://${webApp.outputs.fqdn}'
output apiUrl string = 'https://${apiApp.outputs.fqdn}'
output keyVaultName string = keyVault.outputs.name
output storageAccountName string = storage.outputs.name
output managedIdentityClientId string = managedIdentity.outputs.clientId
