'use client'

interface ContainerApp {
  name: string
  image: string
  cpu: number
  memory: string
  ingress?: { external: boolean; target_port: number }
}

interface StorageAccount { name: string; sku: string; containers: string[] }
interface KeyVault { name: string; sku: string }
interface LogAnalytics { name: string; retention_days: number }
interface AppInsights { name: string }
interface ManagedIdentity { name: string }
interface AIFoundry { workspace_name: string; model_deployments: { name: string; model: string; capacity: number }[] }

interface Resources {
  container_apps?: ContainerApp[]
  storage_account?: StorageAccount
  key_vault?: KeyVault
  log_analytics?: LogAnalytics
  application_insights?: AppInsights
  managed_identity?: ManagedIdentity
  ai_foundry?: AIFoundry
}

export function DeploymentManifestPreview({
  manifest,
}: {
  manifest: Record<string, unknown>
}) {
  const resources = (manifest?.resources as Resources) ?? {}
  const env = manifest?.environment as string
  const region = manifest?.azure_region as string
  const rg = manifest?.resource_group as string
  const outputs = (manifest?.outputs as Record<string, string>) ?? {}

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h3 className="font-semibold text-gray-900">Deployment Manifest</h3>
          <p className="text-sm text-gray-500">
            Azure resource specification · Environment: {env} · Region: {region}
          </p>
        </div>
        <div className="text-xs text-amber-600 bg-amber-50 border border-amber-200 px-3 py-1.5 rounded-lg">
          📌 Bicep generation coming in Phase 3
        </div>
      </div>

      {/* Resource Group */}
      <div className="rounded-lg bg-blue-50 border border-blue-200 px-4 py-3">
        <p className="text-sm font-medium text-blue-900">Resource Group</p>
        <p className="text-sm text-blue-700 font-mono mt-0.5">{rg}</p>
      </div>

      {/* Container Apps */}
      {resources.container_apps && resources.container_apps.length > 0 && (
        <ResourceSection title="🐋 Container Apps" count={resources.container_apps.length}>
          {resources.container_apps.map((app) => (
            <ResourceCard key={app.name} name={app.name}>
              <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-xs text-gray-600">
                <span><b>Image:</b> {app.image}</span>
                <span><b>CPU:</b> {app.cpu} · <b>Memory:</b> {app.memory}</span>
                {app.ingress && (
                  <span><b>Port:</b> {app.ingress.target_port} ({app.ingress.external ? 'external' : 'internal'})</span>
                )}
              </div>
            </ResourceCard>
          ))}
        </ResourceSection>
      )}

      {/* Other resources */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {resources.storage_account && (
          <ResourceCard name={resources.storage_account.name} badge="Storage Account">
            <p className="text-xs text-gray-600">SKU: {resources.storage_account.sku}</p>
            <p className="text-xs text-gray-600">Containers: {resources.storage_account.containers.join(', ')}</p>
          </ResourceCard>
        )}
        {resources.key_vault && (
          <ResourceCard name={resources.key_vault.name} badge="Key Vault">
            <p className="text-xs text-gray-600">SKU: {resources.key_vault.sku}</p>
          </ResourceCard>
        )}
        {resources.log_analytics && (
          <ResourceCard name={resources.log_analytics.name} badge="Log Analytics">
            <p className="text-xs text-gray-600">Retention: {resources.log_analytics.retention_days} days</p>
          </ResourceCard>
        )}
        {resources.application_insights && (
          <ResourceCard name={resources.application_insights.name} badge="App Insights" />
        )}
        {resources.managed_identity && (
          <ResourceCard name={resources.managed_identity.name} badge="Managed Identity" />
        )}
        {resources.ai_foundry && (
          <ResourceCard name={resources.ai_foundry.workspace_name} badge="AI Foundry">
            <div className="flex flex-wrap gap-1 mt-1">
              {resources.ai_foundry.model_deployments.map((m) => (
                <span key={m.name} className="text-xs bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded border border-indigo-200">
                  {m.model}
                </span>
              ))}
            </div>
          </ResourceCard>
        )}
      </div>

      {/* Outputs */}
      {Object.keys(outputs).length > 0 && (
        <section className="space-y-2">
          <h4 className="text-sm font-medium text-gray-700">Outputs</h4>
          <div className="rounded-lg border border-gray-200 divide-y divide-gray-100">
            {Object.entries(outputs).map(([k, v]) => (
              <div key={k} className="flex items-center justify-between px-4 py-2 text-sm">
                <span className="font-medium text-gray-700 font-mono">{k}</span>
                <span className="text-gray-600 font-mono text-xs">{v}</span>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}

function ResourceSection({
  title,
  count,
  children,
}: {
  title: string
  count: number
  children: React.ReactNode
}) {
  return (
    <section className="space-y-2">
      <h4 className="text-sm font-medium text-gray-700">
        {title}{' '}
        <span className="text-gray-400 font-normal">({count})</span>
      </h4>
      <div className="space-y-2">{children}</div>
    </section>
  )
}

function ResourceCard({
  name,
  badge,
  children,
}: {
  name: string
  badge?: string
  children?: React.ReactNode
}) {
  return (
    <div className="rounded-lg border border-gray-200 px-4 py-3 space-y-1">
      <div className="flex items-center gap-2 flex-wrap">
        <span className="font-medium text-sm text-gray-900 font-mono">{name}</span>
        {badge && (
          <span className="text-xs px-2 py-0.5 rounded bg-gray-100 text-gray-600">{badge}</span>
        )}
      </div>
      {children}
    </div>
  )
}
